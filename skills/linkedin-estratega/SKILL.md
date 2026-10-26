---
name: linkedin-estratega
description: Decide qué publicar en LinkedIn y cuándo. Cruza el estudio de LinkedIn 2026 de Metricool (673.658 publicaciones) con el perfil y, si los hay, con los datos reales de la cuenta, y entrega un plan semanal con pilar, formato, gancho y hora de cada post. También convierte otro estudio o documento en reglas propias. Úsala cuando alguien diga «qué publico esta semana», «hazme un plan de LinkedIn», «qué formato me conviene», «qué dice el estudio de Metricool», «convierte este estudio en reglas».
---

# Estratega de LinkedIn

La estratega no copia lo que funciona en general: lo cruza con lo que ya le
funciona a esta persona. Lo que funciona en el estudio **y** en su cuenta es su
formato.

## Fuentes, en este orden

1. `linkedin/perfil.md`: objetivo, pilares, cuentas, posts por semana que puede
   sostener. Si no existe, ofrece `linkedin-kickoff`.
2. El último informe de la analista en `linkedin/historial.md`, si existe. Si no
   hay ninguno y el conector de Metricool está disponible, ofrece lanzar
   `linkedin-analista` primero: con datos propios el plan es mucho mejor.
3. `../../referencias/estudio-metricool-2026.md`.
4. Estudios que haya añadido la persona en `linkedin/estudios/`.

## Plan semanal

1. **Cuántos posts.** Los que diga el perfil. Si no lo dice, pregunta. Como
   referencia, el estudio da una media de 3,05 posts por semana en perfiles
   personales y 2,34 en páginas de empresa.
2. **Reparto por pilares**, para que ninguno se quede vacío dos semanas seguidas.
3. **Formato de cada post**, entre los que produce el equipo: texto, texto con
   infografía o gráfico (`linkedin-infografia`) y encuesta. Razonado:
   - Lo que mejor le funciona a la cuenta según la analista, primero.
   - Si no hay datos propios, el estudio: la imagen individual es la que más
     comentarios genera (2,80 por post, frente a 1,75 del texto); las encuestas,
     para temas que dividen al sector.
   - Un formato nuevo por semana como mucho, para poder medirlo.
4. **Día y hora.** Con Metricool: `getBestTimeToPostByNetwork` para LinkedIn y la
   semana del plan (ver `../../referencias/metricool-mcp.md`). Sin Metricool: la
   franja de 9:00 a 12:00 del estudio, avisando de que es una media general.
5. **Gancho previsto** para cada post (tipo de `../../referencias/ganchos-es.md`).
6. **Dos cuentas:** si hay perfil personal y página de empresa, que no publiquen
   lo mismo el mismo día. El perfil, para conversar; la página, para alcance (y
   ahí sí van enlaces: +51% de impresiones en el estudio).

## Entrega

Una tabla y nada más:

| Día | Hora | Cuenta | Pilar | Formato | Tema | Gancho (tipo) | Por qué |
|---|---|---|---|---|---|---|---|

Debajo, en 2-3 líneas, qué se está probando esta semana. Con el visto bueno,
guárdalo en `linkedin/plan-semana.md` (sustituye el anterior; el viejo pasa al
final de `linkedin/historial.md`).

## Convertir un estudio en reglas

Si la persona pasa un estudio o un informe (PDF, enlace o texto):

1. Extrae solo los datos con cifra, qué miden y sobre qué muestra.
2. Apunta quién lo ha hecho, las fechas y los límites.
3. Guárdalo en `linkedin/estudios/<nombre>.md` con el mismo formato que
   `estudio-metricool-2026.md`.
4. Si contradice a otro estudio, no elijas tú: enseña los dos datos.

## Reglas

- Cada cifra del plan dice de dónde sale: tu cuenta, el estudio de Metricool u
  otro estudio.
- Un dato de un estudio es una media de miles de cuentas, no una predicción para
  esta. Si choca con los datos de la cuenta, mandan los de la cuenta.
