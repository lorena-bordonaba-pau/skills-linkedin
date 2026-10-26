# Equipo de LinkedIn para Claude

Siete skills en español que hacen de equipo de LinkedIn: una redactora que
escribe con tu voz, una estratega que sabe lo que funciona en 673.658
publicaciones, una analista que lee tus datos y una community manager que lo
programa todo. Con Metricool como base para los datos y la programación.

Nada se publica sin tu «sí».

## Instalación

### Claude Desktop o claude.ai

1. **Personalizar** → pestaña **Plugins** → **Añadir** → **Añadir marketplace**.
2. **Desde un repositorio** → pega `<usuario>/equipo-linkedin` y sincroniza.
3. En **Descubrir**, busca *equipo-linkedin* y pulsa **+**.
4. Comprueba en **Tuyos** que está activado y abre una conversación nueva.

### Claude Code

```
/plugin marketplace add <usuario>/equipo-linkedin
/plugin install equipo-linkedin@equipo-linkedin
```

### Metricool (para la analista y la community manager)

**Personalizar** → **Conectores** → busca **Metricool** → **Conectar** →
**Conceder acceso**. Prueba: «enséñame las marcas conectadas a mi Metricool».

La redactora, la estratega y las infografías funcionan sin Metricool.

## Primer paso: el kickoff

Escribe **«haz mi kickoff de LinkedIn»**. Son unos 10 minutos: tres bloques de
preguntas y unos cuantos posts tuyos pegados. Sale tu perfil (`linkedin/perfil.md`):
quién eres, a quién escribes, tus pilares, tu voz y tu marca visual. Todas las
demás skills lo leen antes de trabajar.

## Las 7 skills

| Skill | Puesto | Qué hace | Ejemplo |
|---|---|---|---|
| `linkedin-kickoff` | — | Entrevista, aprende tu voz y escribe tu perfil | «haz mi kickoff de LinkedIn» |
| `linkedin-redactora` | Redactora | Posts con tu voz, dos ganchos, sin tics de IA | «escríbeme un post sobre…» |
| `linkedin-estratega` | Estratega | Plan semanal con el estudio de Metricool y tus datos | «qué publico esta semana» |
| `linkedin-analista` | Analista | Tus datos de Metricool por formato, comparados con el estudio | «cómo va mi LinkedIn» |
| `linkedin-community-manager` | Community manager | Programa en Metricool a tu mejor hora y te ayuda con los comentarios | «prográmalo el martes» |
| `linkedin-infografia` | Diseño | La imagen del post en 4 estilos (boceto a mano, listado, captura en 16:9, datos) o en plantillas creadas con tus diseños | «hazme una infografía de esto», «crea una plantilla con mis diseños» |
| `linkedin-reunion-semanal` | Todo el equipo | La reunión de los lunes: analiza, planifica, escribe y programa | «reunión de LinkedIn» |

## Dónde se guarda todo

En la carpeta `linkedin/` de tu carpeta de trabajo:

```
linkedin/
├── perfil.md          ← lo escribe el kickoff
├── plan-semana.md     ← la estratega
├── historial.md       ← la analista (un informe por semana)
├── estudios/          ← otros estudios que añadas
├── infografias/       ← los HTML de tus infografías y gráficos
└── plantillas/        ← tus plantillas, creadas a partir de tus diseños
```

En claude.ai, sin carpeta de trabajo, guarda el perfil en el conocimiento de un
Proyecto.

## De dónde salen los datos

- **Tu cuenta:** Metricool, a través de su conector.
- **El estudio:** [estudio de LinkedIn 2026 de Metricool](https://metricool.com/linkedin-trends/),
  673.658 publicaciones de 63.108 cuentas. Resumen en `referencias/estudio-metricool-2026.md`.
  Si tienes la skill gratuita de Metricool [`/linkedin-benchmark`](https://metricool.com/claude-linkedin-benchmark-skill/),
  la analista la usa para compararte con cuentas de tu tamaño.

## Créditos

La organización en skills por tarea se inspira en
[sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills)
(MIT). Los textos, las referencias en español y la integración con Metricool son
propios.

Licencia MIT.
