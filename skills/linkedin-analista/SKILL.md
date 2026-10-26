---
name: linkedin-analista
description: Lee los datos reales de LinkedIn desde Metricool (últimos 7 o 30 días, por cuenta y por formato), encuentra qué posts tiraron y cuáles no, y lo compara con el estudio de LinkedIn 2026 de Metricool. Deja el informe en linkedin/historial.md. Úsala cuando alguien diga «cómo va mi LinkedIn», «qué ha funcionado este mes», «analiza mis posts», «compárame con el estudio», «qué dejo de publicar».
---

# Analista de LinkedIn

Necesita el conector de Metricool (`../../referencias/metricool-mcp.md`). Sin él,
la persona puede pegar sus cifras a mano; la analista **nunca** se inventa un dato
de la cuenta.

## Pasos

1. **Cuentas.** `getBrandSettings`. Usa las marcas del perfil (`linkedin/perfil.md`)
   o pregunta cuáles. Anota la zona horaria.
2. **Métricas disponibles.** `getAnalyticsAvailableMetrics` con
   `network: "linkedin"` y `connector: "posts"`. Elige las que haya de:
   impresiones, interacciones o engagement, comentarios, clics y compartidos, y el
   tipo de post si viene. No supongas los IDs: salen de esta llamada.
3. **Datos.** `getAnalyticsDataByMetrics` con el periodo pedido (por defecto, los
   últimos 30 días; en la reunión semanal, 7) y las métricas elegidas.
4. **Tabla por formato** (texto, imagen, carrusel/documento, vídeo, encuesta):
   número de posts, impresiones medias, engagement medio, comentarios medios.
5. **Los 3 mejores y los 3 peores posts**, con fecha, formato y las cifras que
   expliquen por qué destacan.
6. **Comparación con el estudio** (`../../referencias/estudio-metricool-2026.md`):
   solo métricas que se midan igual, y con el tipo de cuenta correcto (perfil
   personal o página de empresa). Si Metricool ha instalado su skill
   `/linkedin-benchmark`, ofrécela: compara con cuentas del mismo tamaño, que es
   una comparación más justa que la media del estudio.

## Entrega

- La tabla por formato.
- **Qué repetir, qué dejar, qué probar**: tres líneas, cada una con su dato.
- Si hay dos cuentas, el mismo bloque para cada una.

Con el visto bueno, añade el informe al principio de `linkedin/historial.md` con
la fecha y el periodo. Es lo que leerá la estratega.

## Reglas de lectura

- **Pocos posts, poca conclusión.** Con menos de 3 posts de un formato, se dice
  que la muestra es pequeña y no se saca regla.
- **Correlación no es causa.** «Los carruseles tuvieron más impresiones» es un
  dato; «tuvieron más impresiones porque eran carruseles» no se ha medido.
- **Los posts recientes** (menos de 48 horas) aún no tienen todas sus impresiones:
  según el estudio, la mitad llega en las primeras 48 horas. Se marcan aparte.
- Cada cifra dice de dónde sale: Metricool (tu cuenta) o el estudio.
