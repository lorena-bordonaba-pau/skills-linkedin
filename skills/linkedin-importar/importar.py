#!/usr/bin/env python3
"""Importa lo que LinkedIn deja descargar y lo deja listo para el equipo.

Dos fuentes:
  - La exportación de tus datos (ZIP o CSV): Shares.csv con tus posts y
    Comments.csv con tus comentarios. Del ZIP solo se abren esos dos ficheros:
    mensajes, contactos e invitaciones no se leen nunca.
  - La exportación de analíticas (XLSX): de creador (perfil personal) o de
    página de empresa. Se buscan tablas con URL, fecha, impresiones e
    interacciones.

Uso:
  python3 importar.py inspeccionar RUTA [RUTA ...]
  python3 importar.py importar RUTA [RUTA ...] [--salida linkedin/datos]

Solo biblioteca estándar. Los nombres de columna cambian con el idioma de la
cuenta, así que se detectan por palabras clave en inglés y en español; lo que no
se reconoce se informa, no se adivina.
"""

import argparse
import csv
import io
import re
import statistics
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path

# Ficheros del ZIP de datos que se pueden abrir. Todo lo demás se ignora.
PERMITIDOS = {"shares.csv", "comments.csv"}

CLAVES = {
    "url": ["sharelink", "post url", "url de la publicacion", "url", "link", "enlace"],
    "fecha": ["date", "fecha", "publish", "publicacion", "created"],
    "texto": ["sharecommentary", "commentary", "message", "texto", "contenido"],
    "impresiones": ["impression", "impresion"],
    "interacciones": ["engagement", "interaccion"],
    "alcance": ["members reached", "miembros alcanzados", "reach", "alcance"],
    "media": ["mediaurl", "media", "multimedia"],
}

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "rel": "http://schemas.openxmlformats.org/package/2006/relationships"}


def norm(texto):
    s = unicodedata.normalize("NFKD", str(texto or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def tipo_columna(cabecera):
    c = norm(cabecera)
    # Una cabecera es corta y no es un dato: ni URL, ni número, ni frase larga.
    if not c or len(c) > 40 or "http" in c or "www." in c or re.fullmatch(r"[\d\s.,:/%-]+", c):
        return None
    for tipo in ("texto", "impresiones", "interacciones", "alcance", "media", "url", "fecha"):
        if any(k in c for k in CLAVES[tipo]):
            return tipo
    return None


# ---------- lectura ----------

def leer_csv(datos):
    texto = datos.decode("utf-8-sig", errors="replace")
    return [fila for fila in csv.reader(io.StringIO(texto))]


def leer_xlsx(datos):
    """Devuelve {nombre_hoja: [[celda, ...], ...]} sin dependencias."""
    z = zipfile.ZipFile(io.BytesIO(datos))
    compartidas = []
    if "xl/sharedStrings.xml" in z.namelist():
        raiz = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in raiz.findall("m:si", NS):
            compartidas.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
    libro = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    destino = {r.get("Id"): r.get("Target") for r in rels.findall("rel:Relationship", NS)}
    hojas = {}
    for hoja in libro.find("m:sheets", NS):
        objetivo = destino[hoja.get(f"{{{NS['r']}}}id")].lstrip("/")
        ruta = objetivo if objetivo.startswith("xl/") else "xl/" + objetivo
        raiz = ET.fromstring(z.read(ruta))
        filas = []
        for fila in raiz.iter(f"{{{NS['m']}}}row"):
            celdas = {}
            for c in fila.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)", c.get("r", "A")).group(1)
                col = 0
                for letra in ref:
                    col = col * 26 + ord(letra) - 64
                tipo, v = c.get("t"), c.find("m:v", NS)
                if tipo == "s" and v is not None:
                    valor = compartidas[int(v.text)]
                elif tipo == "inlineStr":
                    valor = "".join(t.text or "" for t in c.iter(f"{{{NS['m']}}}t"))
                else:
                    valor = v.text if v is not None else ""
                celdas[col - 1] = valor
            if celdas:
                ancho = max(celdas) + 1
                filas.append([celdas.get(i, "") for i in range(ancho)])
            else:
                filas.append([])
        hojas[hoja.get("name")] = filas
    return hojas


def cargar(ruta):
    """Devuelve una lista de (origen, filas) de los ficheros permitidos."""
    p = Path(ruta)
    datos = p.read_bytes()
    nombre = p.name.lower()
    if nombre.endswith(".xlsx") or nombre.endswith(".xls") and datos[:2] == b"PK":
        return [(f"{p.name} · {h}", filas) for h, filas in leer_xlsx(datos).items()]
    if nombre.endswith(".xls"):
        sys.exit(f"{p.name}: es un .xls antiguo. Ábrelo y guárdalo como .xlsx o .csv.")
    if nombre.endswith(".csv"):
        return [(p.name, leer_csv(datos))]
    if nombre.endswith(".zip"):
        z = zipfile.ZipFile(io.BytesIO(datos))
        salida = []
        for n in z.namelist():
            base = n.rsplit("/", 1)[-1].lower()
            if base in PERMITIDOS:
                salida.append((f"{p.name} · {base}", leer_csv(z.read(n))))
        if not salida:
            print(f"{p.name}: no trae Shares.csv ni Comments.csv. Al pedir la copia de "
                  "tus datos, marca las publicaciones.", file=sys.stderr)
        return salida
    sys.exit(f"{p.name}: formato no reconocido (usa .zip, .csv o .xlsx).")


# ---------- tablas ----------

def tablas(filas):
    """Busca tablas dentro de una hoja. Una cabecera es una fila con al menos dos
    columnas reconocibles; si en la misma fila hay grupos separados por celdas
    vacías, cada grupo es una tabla distinta (las analíticas ponen tablas lado
    a lado)."""
    encontradas = []
    for i, fila in enumerate(filas):
        tipos = [tipo_columna(c) for c in fila]
        if sum(1 for t in tipos if t) < 2:
            continue
        grupos, actual = [], []
        for j, c in enumerate(fila):
            if str(c).strip():
                actual.append(j)
            elif actual:
                grupos.append(actual)
                actual = []
        if actual:
            grupos.append(actual)
        for g in grupos:
            mapa = {}
            for j in g:
                t = tipo_columna(fila[j])
                if t and t not in mapa:
                    mapa[t] = j
            if len(mapa) < 2 or not ({"url", "texto"} & mapa.keys()):
                continue
            registros = []
            for siguiente in filas[i + 1:]:
                if not any(str(siguiente[j]).strip() for j in g if j < len(siguiente)):
                    break
                if sum(1 for j in g if j < len(siguiente) and tipo_columna(siguiente[j])) >= 2:
                    break  # empieza otra cabecera
                registros.append({t: (siguiente[j] if j < len(siguiente) else "") for t, j in mapa.items()})
            encontradas.append({"cabeceras": [fila[j] for j in g], "mapa": mapa,
                                "nombres": {t: fila[j] for t, j in mapa.items()}, "filas": registros})
    return encontradas


def dia_primero(valores):
    """True si las fechas con barras van día/mes (alguna empieza por más de 12)."""
    for v in valores:
        m = re.match(r"\s*(\d{1,2})/(\d{1,2})/", str(v or ""))
        if m and int(m.group(1)) > 12:
            return True
    return False


def a_fecha(valor, dia_mes=False):
    v = str(valor or "").strip()
    if not v:
        return None
    if re.fullmatch(r"\d+(\.\d+)?", v):  # número de serie de Excel
        try:
            from datetime import timedelta
            return (datetime(1899, 12, 30) + timedelta(days=float(v))).date()
        except (OverflowError, ValueError):
            return None
    v = v.replace("T", " ").split(".")[0].split("+")[0].strip()
    barras = ("%d/%m/%Y %H:%M", "%d/%m/%Y", "%d/%m/%y") if dia_mes else ("%m/%d/%Y %H:%M", "%m/%d/%Y", "%m/%d/%y")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d") + barras:
        try:
            return datetime.strptime(v, fmt).date()
        except ValueError:
            continue
    return None


def a_numero(valor):
    v = re.sub(r"[^\d,.\-]", "", str(valor or ""))
    if not v:
        return None
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".") if v.rfind(",") > v.rfind(".") else v.replace(",", "")
    elif "," in v:
        v = v.replace(",", "") if re.search(r",\d{3}$", v) else v.replace(",", ".")
    elif re.search(r"\.\d{3}$", v) and v.count(".") >= 1 and len(v.split(".")[-1]) == 3:
        v = v.replace(".", "")
    try:
        return float(v)
    except ValueError:
        return None


def id_post(url):
    m = re.search(r"(\d{15,})", str(url or ""))
    return m.group(1) if m else None


# ---------- comandos ----------

def inspeccionar(rutas):
    for ruta in rutas:
        for origen, filas in cargar(ruta):
            print(f"\n=== {origen}: {len(filas)} filas")
            encontradas = tablas(filas)
            if not encontradas:
                print("  Sin tablas reconocibles. Primeras filas:")
                for fila in filas[:8]:
                    print("   ", [str(c)[:40] for c in fila][:10])
                continue
            for t in encontradas:
                print(f"  Tabla con {len(t['filas'])} filas")
                print(f"    Cabeceras: {t['cabeceras']}")
                print("    Reconocidas: " + ", ".join(f"{k} ← «{n}»" for k, n in t["nombres"].items()))
                if t["filas"]:
                    ejemplo = {k: str(v)[:60] for k, v in t["filas"][0].items()}
                    print(f"    Ejemplo: {ejemplo}")


def importar(rutas, salida):
    posts, metricas, comentarios = [], [], []
    for ruta in rutas:
        for origen, filas in cargar(ruta):
            for t in tablas(filas):
                es_comentarios = "comments.csv" in origen.lower()
                dia_mes = dia_primero(r.get("fecha") for r in t["filas"])
                for r in t["filas"]:
                    reg = {
                        "fecha": a_fecha(r.get("fecha"), dia_mes),
                        "url": str(r.get("url") or "").strip(),
                        "texto": str(r.get("texto") or "").strip(),
                        "impresiones": a_numero(r.get("impresiones")),
                        "interacciones": a_numero(r.get("interacciones")),
                        "media": bool(str(r.get("media") or "").strip()),
                        "origen": origen,
                    }
                    if es_comentarios:
                        comentarios.append(reg)
                    elif reg["texto"]:
                        posts.append(reg)
                    elif reg["impresiones"] is not None or reg["interacciones"] is not None:
                        metricas.append(reg)

    # Métricas duplicadas (las analíticas repiten posts en varias tablas): una por URL
    unicas = {}
    for m in metricas:
        clave = id_post(m["url"]) or m["url"]
        previa = unicas.get(clave)
        if previa is None:
            unicas[clave] = m
        else:
            for k in ("impresiones", "interacciones", "fecha"):
                if previa.get(k) is None and m.get(k) is not None:
                    previa[k] = m[k]
    metricas = list(unicas.values())

    # Unir textos y métricas: primero por ID de la URL, si no, por fecha cuando solo hay un post ese día
    por_id = {id_post(m["url"]): m for m in metricas if id_post(m["url"])}
    por_dia = {}
    for m in metricas:
        if m["fecha"]:
            por_dia.setdefault(m["fecha"], []).append(m)
    usadas, unidos = set(), 0
    for p in posts:
        m = por_id.get(id_post(p["url"]))
        if m is None and p["fecha"] and len(por_dia.get(p["fecha"], [])) == 1:
            m = por_dia[p["fecha"]][0]
        if m is not None and id(m) not in usadas:
            p["impresiones"], p["interacciones"] = m["impresiones"], m["interacciones"]
            usadas.add(id(m))
            unidos += 1
    solo_metricas = [m for m in metricas if id(m) not in usadas]

    for p in posts:
        t = p["texto"]
        p["caracteres"] = len(t)
        p["enlace_en_texto"] = bool(re.search(r"https?://|www\.", t))
        p["termina_en_pregunta"] = t.rstrip().endswith("?")
        p["hashtags"] = len(re.findall(r"#\w+", t))
        p["empieza_con_pregunta"] = bool(re.match(r"\s*¿|[^\n]{0,140}\?", t.split("\n", 1)[0]))
        p["engagement"] = (p["interacciones"] / p["impresiones"]
                           if p.get("impresiones") and p.get("interacciones") is not None else None)

    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    campos = ["fecha", "url", "texto", "caracteres", "media", "enlace_en_texto", "empieza_con_pregunta",
              "termina_en_pregunta", "hashtags", "impresiones", "interacciones", "engagement", "origen"]
    todos = sorted(posts + solo_metricas, key=lambda r: str(r.get("fecha") or ""), reverse=True)
    with open(salida / "posts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for r in todos:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in campos})
    if comentarios:
        with open(salida / "comentarios.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["fecha", "url", "texto"], extrasaction="ignore")
            w.writeheader()
            for r in comentarios:
                w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in ("fecha", "url", "texto")})

    resumen = resumir(posts, solo_metricas, comentarios, unidos)
    (salida / "resumen.md").write_text(resumen, encoding="utf-8")
    print(resumen)
    print(f"\nGuardado en {salida}/ (posts.csv, resumen.md"
          + (", comentarios.csv" if comentarios else "") + ")")


DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def mediana(valores):
    v = [x for x in valores if x is not None]
    return round(statistics.median(v), 4) if v else None


def miles(n):
    return f"{n:,.0f}".replace(",", ".")


def comparar(posts, clave, etiqueta_si, etiqueta_no):
    con = [p for p in posts if p[clave] and p.get("impresiones") is not None]
    sin = [p for p in posts if not p[clave] and p.get("impresiones") is not None]
    if len(con) < 3 or len(sin) < 3:
        return f"| {etiqueta_si} | {len(con)} | muestra pequeña, sin conclusión | {len(sin)} ({etiqueta_no}) |"
    return (f"| {etiqueta_si} | {len(con)} | {miles(mediana([p['impresiones'] for p in con]))} | "
            f"{miles(mediana([p['impresiones'] for p in sin]))} ({etiqueta_no}, {len(sin)} posts) |")


def resumir(posts, solo_metricas, comentarios, unidos):
    l = ["# Tus datos de LinkedIn", "",
         f"Importado el {datetime.now():%Y-%m-%d}. Fuente: la exportación de LinkedIn de la propia cuenta.", ""]
    fechas = sorted(p["fecha"] for p in posts if p["fecha"])
    l.append("## Posts")
    l.append(f"- Posts con texto: {len(posts)}"
             + (f", del {fechas[0]} al {fechas[-1]}" if fechas else ""))
    if len(fechas) >= 2:
        semanas = max(1, (fechas[-1] - fechas[0]).days / 7)
        l.append(f"- Ritmo: {len(fechas) / semanas:.1f} posts por semana de media".replace(".", ","))
    if fechas:
        dias = Counter(DIAS[f.weekday()] for f in fechas)
        l.append("- Días en que más publicas: " + ", ".join(f"{d} ({n})" for d, n in dias.most_common(3)))
    if posts:
        l.append(f"- Largo mediano: {mediana([p['caracteres'] for p in posts]):.0f} caracteres")
        l.append(f"- Con enlace en el texto: {sum(p['enlace_en_texto'] for p in posts)}")
        l.append(f"- Abren con pregunta: {sum(p['empieza_con_pregunta'] for p in posts)}")
        l.append(f"- Cierran con pregunta: {sum(p['termina_en_pregunta'] for p in posts)}")
    l.append(f"- Posts con métricas unidas al texto: {unidos}")
    if solo_metricas:
        l.append(f"- Posts con métricas pero sin texto (encuestas, documentos o fuera del rango "
                 f"de la exportación de datos): {len(solo_metricas)}")
    if comentarios:
        l.append(f"- Comentarios tuyos: {len(comentarios)}")

    con_metricas = [p for p in posts if p.get("impresiones") is not None]
    if con_metricas:
        l += ["", "## ¿Se cumple en tu cuenta lo que dice el estudio?", "",
              "Impresiones medianas. Con menos de 3 posts en un grupo no se saca conclusión.", "",
              "| Grupo | Posts | Impresiones medianas | Resto |", "|---|---|---|---|",
              comparar(posts, "enlace_en_texto", "Con enlace en el texto", "sin enlace"),
              comparar(posts, "termina_en_pregunta", "Cierran con pregunta", "sin pregunta"),
              comparar(posts, "empieza_con_pregunta", "Abren con pregunta", "sin pregunta"),
              comparar(posts, "media", "Con imagen o vídeo", "solo texto"), ""]
        top = sorted(con_metricas, key=lambda p: p["impresiones"], reverse=True)
        l.append("## Los 5 con más impresiones")
        corto = lambda t: " ".join(t.split())[:90]
        for p in top[:5]:
            l.append(f"- {p['fecha']} · {miles(p['impresiones'])} impresiones · «{corto(p['texto'])}»")
        l.append("")
        l.append("## Los 5 con menos impresiones")
        for p in top[-5:][::-1]:
            l.append(f"- {p['fecha']} · {miles(p['impresiones'])} impresiones · «{corto(p['texto'])}»")
    return "\n".join(l) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)
    a = sub.add_parser("inspeccionar")
    a.add_argument("rutas", nargs="+")
    b = sub.add_parser("importar")
    b.add_argument("rutas", nargs="+")
    b.add_argument("--salida", default="linkedin/datos")
    args = ap.parse_args()
    if args.comando == "inspeccionar":
        inspeccionar(args.rutas)
    else:
        importar(args.rutas, args.salida)


if __name__ == "__main__":
    main()
