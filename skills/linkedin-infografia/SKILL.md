---
name: linkedin-infografia
description: Diseña la imagen de un post de LinkedIn con la marca de la persona, en cuatro estilos (boceto a mano para explicar conceptos, listado tipo Notion, captura de pantalla en 16:9 para herramientas y novedades, y datos o gráficos) o en sus propias plantillas, que crea a partir de capturas de diseños suyos. Maqueta en HTML (1080×1350, o 1920×1080 la captura) y lo deja listo para exportar y programar en Metricool. Úsala cuando alguien diga «hazme una infografía», «hazme un gráfico», «explica esto con un dibujo», «hazme un listado», «hazme una captura de esta herramienta», «crea una plantilla con mi estilo», «te paso mis diseños».
---

# Infografías y gráficos para LinkedIn

Una sola imagen por post. Según el estudio de LinkedIn 2026 de Metricool, la
imagen individual es el formato que más comentarios genera: 2,80 por post
(`../../referencias/estudio-metricool-2026.md`).

## Los estilos

| Estilo | Para qué | Plantilla |
|---|---|---|
| **1 · Boceto** | Explicar un concepto: un proceso, un ciclo, un viaje, un embudo, una escalera, un antes/después | `plantilla-boceto.html` |
| **2 · Listado** | Una lista con categorías: herramientas, recursos, plantillas, pasos | `plantilla-listado.html` |
| **3 · Captura** | Una herramienta o una novedad: solo la captura de pantalla, en 16:9 (1920×1080) | `plantilla-captura.html` |
| **4 · Datos** | Una cifra grande o un gráfico de barras o de evolución | `plantilla-datos.html` |
| **Tus plantillas** | Las que se crean con los diseños de la persona | `linkedin/plantillas/*.html` |

Si la persona no dice el estilo, se elige por el contenido con esta tabla y se
explica en una línea por qué. Si tiene plantillas propias que encajan, van primero.

## Antes de diseñar

1. Lee `linkedin/perfil.md`: voz (sección 6) y marca visual (sección 8, con la
   lista de sus plantillas). Si no hay marca visual, usa la plantilla tal cual y
   avisa.
2. Material: un post de la redactora, un tema, una herramienta o unos datos. Si es
   un tema suelto, pide antes el post a `linkedin-redactora`: la imagen y el post
   salen de la misma idea y no repiten lo mismo.

## Cómo se hace

1. **Boceto en texto** (enséñalo antes de maquetar): estilo, titular, contenido y
   fuente de cada dato.
2. **Maquetación.** Copia la plantilla del estilo a
   `linkedin/infografias/<fecha>-<tema>.html` y cambia el contenido. Ajusta las
   variables de `:root` a la marca del perfil y `--firma` a su nombre y usuario.
3. **Por estilo:**
   - **Boceto:** reutiliza las piezas dibujadas de `<defs>` (monigote, bombilla,
     hoja, lápiz, pila de documentos, gráfico, lupa, calendario, reloj, nube de
     pensamiento, portátil, llave, flecha) y recolócalas para el concepto. Entre 6
     y 12 elementos con etiqueta a mano, flechas que se lean en un solo sentido y
     un título subrayado. Tinta negra sobre papel; como mucho un color de acento
     para una sola cosa. Si hace falta una pieza que no existe (un muro, una
     montaña con bandera, una escalera, un sobre, una ventana de navegador), se
     dibuja con el mismo trazo y se añade a `<defs>`.
   - **Listado:** de 6 a 14 filas. Cada fila: emoji, texto corto y una etiqueta.
     De 2 a 4 categorías, cada una con su color pastel. Las pestañas de arriba son
     las categorías.
   - **Captura:** solo la captura de pantalla real, sin marco, titular ni
     anotaciones, en 16:9 (1920×1080). Si hay herramienta de capturas o navegador,
     se hace de la web oficial con la ventana a 1920×1080 y no hace falta
     plantilla. Si la persona pasa una captura con otra proporción,
     `plantilla-captura.html` la encaja en 16:9 recortando por abajo. Lo que haya
     que explicar va en el texto del post.
   - **Datos:** el largo de cada barra, proporcional a su valor; cada valor con su
     número escrito; el eje empieza en cero.
4. **Revisa la imagen antes de entregarla:** si hay herramienta de capturas,
   hazla y mírala. Nada se solapa, nada se sale del marco, todo se lee en el móvil.
5. **Exportar a PNG** a 1080×1350 (la captura, a 1920×1080): captura del bloque con la herramienta de
   capturas si la hay; si no, abrir el HTML en el navegador y hacer la captura a
   mano.
6. **Publicar:** pasa el texto del post y la imagen a `linkedin-community-manager`.
   Para programarla por Metricool, la imagen necesita URL pública o un enlace de
   Drive/Dropbox.

## Crear plantillas con tus diseños

Cuando la persona sube capturas de diseños suyos (o de un estilo que le gusta):

1. **Pide de 1 a 5 imágenes** del mismo estilo y para qué tipo de post las usa.
2. **Analiza y enseña lo que ves**, en concreto:
   - Colores (en hexadecimal, aproximados) y para qué se usa cada uno.
   - Tipografía: la de Google Fonts más parecida para títulos y para texto.
   - Composición: márgenes, dónde va el titular, cuántos bloques, alineación.
   - Elementos que se repiten: iconos, emojis, marcos, flechas, etiquetas, fondos.
   - Tono: a mano, corporativo, minimalista, de revista…
3. **Pregunta solo lo que no se ve** (nombre de la plantilla, si lleva logo).
4. **Construye la plantilla** en `linkedin/plantillas/<nombre>.html`, con la
   misma estructura que las de esta carpeta: lienzo de 1080×1350, variables de
   marca en `:root`, piezas reutilizables y un ejemplo rellenado con un tema suyo.
5. **Compárala con sus capturas** (haz una captura si se puede) y ajusta hasta
   que la persona diga que se parece.
6. **Regístrala** en `linkedin/perfil.md`, sección 8: nombre, para qué sirve y
   la ruta. Desde ese momento es un estilo más.

Se copia el **estilo**, no el contenido: si las capturas son de otra persona o de
otra marca, no se reproducen sus textos, logos ni ilustraciones.

## Reglas

- El titular dice la conclusión («Los carruseles tienen más del doble de
  impresiones»), no el tema («Impresiones por formato»).
- Ningún número sin fuente: tu cuenta (Metricool) o el estudio, escrita en la
  imagen.
- Nada de datos inventados para que el gráfico quede bonito. Si faltan valores,
  se piden.
- Revisa los tics de `../../referencias/tics-ia-es.md` también aquí.
- No se usan logos de otras marcas sin permiso (en el estilo captura, la captura
  de la web de la herramienta es la propia fuente).
- En la captura no se ve nada privado: datos de clientes, correos, otras pestañas.
