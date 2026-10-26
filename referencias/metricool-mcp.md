# Cómo usar el MCP de Metricool

Las skills que tocan datos o programan usan el conector de Metricool en Claude
(Personalizar → Conectores → Metricool → conceder acceso). Prueba de que funciona:
«enséñame las marcas conectadas a mi Metricool».

Si el conector no está, la skill lo dice y sigue con lo que se pueda hacer a mano
(pegar textos, pegar cifras). Nunca se inventan datos de una cuenta.

## Herramientas

Los nombres pueden llevar un prefijo según el cliente; se busca la que termina así.

| Herramienta | Para qué | Datos clave |
|---|---|---|
| `getBrandSettings` | Lista de marcas de la cuenta | `blogId`/`brandId` de cada marca, sus redes conectadas y su **zona horaria**. Siempre lo primero |
| `getAnalyticsAvailableMetrics` | Qué métricas existen | `network: "linkedin"` y `connector: "posts"` (o sin connector para verlas todas). Devuelve los IDs que pide la siguiente |
| `getAnalyticsDataByMetrics` | Los datos | `brandId`, `from`, `to` (ISO 8601) y la lista de IDs de métricas |
| `getBestTimeToPostByNetwork` | Mejores horas | `brandId`, `fromDate`, `toDate` (máx. una semana), `timezone`, `socialNetwork: "linkedin"`. Cuanto más alto el valor, mejor |
| `getScheduledPosts` | Lo que ya está programado | `brandId`, `fromDate`, `toDate`, `timezone` |
| `createScheduledPost` | Programar un post | `blogId`, `date` y `info` (abajo). Devuelve `plannerUrl` |
| `createScheduledPostForReview` | Programar y mandar a aprobación | Igual que el anterior + `reviewers` (emails) y `approvalSystem` (`any`, `all`, `optional`). Requiere plan con equipo |

## El campo `info` de un post de LinkedIn

```json
{
  "text": "Texto del post",
  "providers": [{"network": "linkedin"}],
  "publicationDate": {"dateTime": "2026-11-03T09:30:00", "timezone": "Europe/Madrid"},
  "firstCommentText": "Enlace o comentario inicial",
  "media": [],
  "autoPublish": true,
  "draft": false,
  "linkedinData": {"type": "post", "previewIncluded": true}
}
```

- **Enlace en un perfil personal:** va en `firstCommentText`, no en el texto.
- **Infografía o gráfico:** `media` con la URL pública de la imagen.
- **Encuesta:** `"type": "poll"` y `"poll": {"question": "…", "options":
  [{"text": "…"}, {"text": "…"}], "settings": {"duration": "THREE_DAYS"}}`
  (`ONE_DAY`, `THREE_DAYS`, `SEVEN_DAYS`, `FOURTEEN_DAYS`).
- **Borrador sin publicar:** `"draft": true`.
- **`media`** acepta URLs públicas; Google Drive y Dropbox se suben solos (Drive,
  si está vinculado en Metricool).
- La fecha no puede ser pasada.

## Lo que el MCP no hace

- No lee los comentarios de los posts: para responderlos, se pegan.
- No publica nada sin `createScheduledPost`. Las skills de este plugin piden un
  «sí» explícito antes de llamarla, siempre.
