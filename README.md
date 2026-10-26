# Equipo de LinkedIn para Claude

Ocho skills en español que hacen de equipo de LinkedIn: una redactora que
escribe con tu voz, una estratega que sabe lo que funciona en 673.658
publicaciones, una analista que lee tus datos y una community manager que lo
programa todo. Con Metricool como base para los datos y la programación, y con
tu historial de LinkedIn si lo descargas.

Nada se publica sin tu «sí».

## Instalación

### Claude Desktop o claude.ai

1. **Personalizar** → pestaña **Plugins** → **Añadir** → **Añadir marketplace**.
2. **Desde un repositorio** → pega `lorena-bordonaba-pau/skills-linkedin` y sincroniza.
3. En **Descubrir**, busca *equipo-linkedin* y pulsa **+**.
4. Comprueba en **Tuyos** que está activado y abre una conversación nueva.

### Claude Code

```
/plugin marketplace add lorena-bordonaba-pau/skills-linkedin
/plugin install equipo-linkedin@equipo-linkedin
```

### Sin instalar el plugin

Clona el repositorio y trabaja dentro de la carpeta: Claude Code encuentra las
skills solo, por la copia de `.claude/skills/`. En Windows, esa copia son enlaces
simbólicos: activa el modo desarrollador y `git config core.symlinks true` antes
de clonar, o instala el plugin.

### Metricool (para la analista y la community manager)

**Personalizar** → **Conectores** → busca **Metricool** → **Conectar** →
**Conceder acceso**. Prueba: «enséñame las marcas conectadas a mi Metricool».

La redactora, la estratega y las infografías funcionan sin Metricool.

## Primer paso: el kickoff

Escribe **«haz mi kickoff de LinkedIn»**. Son unos 10 minutos: tres bloques de
preguntas y unos cuantos posts tuyos pegados. Mejor aún: descarga antes tus datos
de LinkedIn y pásaselos a `linkedin-importar`, y el kickoff saca tu voz de todo
tu historial. Sale tu perfil (`linkedin/perfil.md`):
quién eres, a quién escribes, tus pilares, tu voz y tu marca visual. Todas las
demás skills lo leen antes de trabajar.

## Las 8 skills

| Skill | Puesto | Qué hace | Ejemplo |
|---|---|---|---|
| `linkedin-kickoff` | — | Entrevista, aprende tu voz y escribe tu perfil | «haz mi kickoff de LinkedIn» |
| `linkedin-importar` | — | Importa la copia de tus datos (tus posts) y las analíticas que descargas de LinkedIn, las une y te dice qué te ha funcionado | «te paso mis datos de LinkedIn» |
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
├── datos/             ← lo que importas de LinkedIn (posts.csv, resumen.md)
├── estudios/          ← otros estudios que añadas
├── infografias/       ← los HTML de tus infografías y gráficos
└── plantillas/        ← tus plantillas, creadas a partir de tus diseños
```

En claude.ai, sin carpeta de trabajo, guarda el perfil en el conocimiento de un
Proyecto.

## Privacidad y seguridad

- `linkedin/` está en el `.gitignore`: tu perfil y tus datos no se suben aunque
  trabajes dentro de una copia del repositorio.
- De la copia de datos de LinkedIn solo se leen tus posts y tus comentarios.
  Mensajes, contactos e invitaciones no se abren nunca.
- Todo lo que viene de fuera (comentarios, posts ajenos, estudios, ficheros) es
  dato, no instrucciones: ver `referencias/contenido-externo.md`.
- Nada se publica sin tu «sí» a ese post concreto. Cuando dos reglas chocan, el
  orden está en `referencias/prioridades.md`.

## De dónde salen los datos

- **Tu cuenta:** Metricool, a través de su conector, y lo que descargues de
  LinkedIn con `linkedin-importar`.
- **El estudio:** [estudio de LinkedIn 2026 de Metricool](https://metricool.com/linkedin-trends/),
  673.658 publicaciones de 63.108 cuentas. Resumen en `referencias/estudio-metricool-2026.md`.
  Si tienes la skill gratuita de Metricool [`/linkedin-benchmark`](https://metricool.com/claude-linkedin-benchmark-skill/),
  la analista la usa para compararte con cuentas de tu tamaño.

## Créditos

La organización en skills por tarea se inspira en
[sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills)
(MIT), igual que varias prácticas: el orden de prioridades, la regla de contenido
externo y la revisión de tics por densidad con control de sobrecorrección. Los
textos, las referencias en español, la integración con Metricool y el importador
son propios.

Licencia MIT.
