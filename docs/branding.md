# Branding de SDAF Core

> [!NOTE]
> HOWTO de identidad visual del **core**. No sustituye el [handbook](../handbook/README.md).
> Sala de muestras: [assets/sdaf-core-icon-preview.html](assets/sdaf-core-icon-preview.html).

## En esta página

- [Concepto](#concepto)
- [Mark canónico (V1)](#mark-canónico-v1)
- [Lockups](#lockups)
- [Paleta](#paleta)
- [Simbología](#simbología)
- [Motion](#motion)
- [Artefactos](#artefactos)
- [No hacer](#no-hacer)

## Concepto

Híbrido **«Núcleo–portal–spec»**, fusión de tres metáforas:

| Origen | Metáfora | En el mark |
|--------|----------|------------|
| A | Núcleo + órbita | Hexágono + arco abierto |
| B | Spec → construcción | Placa con pliegue + chevron |
| C | Puerta / gate | Portal (arco interior) |

El mark **no lleva texto**. La palabra **SDAF** vive solo en lockups (A/B) o en títulos de UI.

**Canónico:** V1 (arco + portal + placa + pliegue + chevron).  
**Referencia (no canónicos):** V2 austero y V3 máxima austeridad, visibles en el preview para comparar legibilidad a 16 px.

## Mark canónico (V1)

| | |
|--|--|
| Archivo color | [assets/sdaf-core-icon.svg](assets/sdaf-core-icon.svg) |
| Archivo mono | [assets/sdaf-core-icon-mono.svg](assets/sdaf-core-icon-mono.svg) |
| viewBox | `512×512`, diseño centrado, margen de seguridad ~10 % |
| Escala crítica | Debe leerse a **16×16** (favicon). Si un detalle desaparece ahí, no añadir más |

**Uso del mark solo:** favicon, icono de app, avatar, PWA, badges ≤64 px.

**Monocromo:** un solo trazo con `currentColor` (barras de estado, fondos variables).

## Lockups

Misma geometría V1; el wordmark **SDAF** no se mete en el SVG del icono de app.

| Variante | Archivo | Cuándo |
|----------|---------|--------|
| **C · Solo mark** | `sdaf-core-icon.svg` / `-mono.svg` | App, favicon, avatar |
| **B · Horizontal** | [sdaf-core-lockup-horizontal.svg](assets/sdaf-core-lockup-horizontal.svg) | Nav, cabeceras, README, docs |
| **A · Apilado** | [sdaf-core-lockup-stacked.svg](assets/sdaf-core-lockup-stacked.svg) | Hero, splash, portadas, espacios altos |

**Regla de layout:** en columnas estrechas o móvil, **B → A** (apilar). No inventar un tercer layout ad hoc.

**Wordmark tipográfico (cuando se compone en UI, no en el SVG):**

- Familia: sans geométrica del sistema (`Segoe UI`, system-ui, etc.)
- Peso medium/semibold, mayúsculas, tracking amplio (~0,18–0,22 em)
- Color: `--sdaf-ink` sobre claro; `--sdaf-paper` (o equivalente claro) sobre oscuro
- Evitar añadir «Core» dentro del lockup; «Core» puede ir como subtítulo de producto aparte

## Paleta

Máximo **tres** colores, definidos como variables CSS en los SVG:

| Variable | Hex | Rol |
|----------|-----|-----|
| `--sdaf-brand` | `#2d6a4f` | Hexágono / acento institucional |
| `--sdaf-ink` | `#14261c` | Arco, placa, texto sobre claro |
| `--sdaf-paper` | `#f4f7f5` | Portal, pliegue, chevron, texto sobre oscuro |

Sobre fondo oscuro, el arco puede aclararse (p. ej. `#9fbfb0`) solo para contraste; no cuenta como cuarto color de marca en el mark de app.

## Simbología

| Forma | Significado |
|-------|-------------|
| **Hexágono** | Núcleo (Core): constitución reutilizable del método |
| **Arco abierto** | Órbita (adopción en capas) + umbral de gobernanza; abierto abajo = paso, no candado |
| **Portal** | Gate: control del método (no hay implementación sin gate) |
| **Placa + pliegue** | Spec: especificación como verdad operativa |
| **Chevron** | Construcción: código derivado de la spec |
| **Wordmark «SDAF»** | Nombre de marca; solo en lockup o UI |

## Motion

Animación **build → hold**: arco → hexágono → portal → placa/pliegue → chevron → estado estático = V1.

| | |
|--|--|
| SVG (nítido, play once) | [assets/sdaf-core-icon-build.svg](assets/sdaf-core-icon-build.svg) |
| GIF (README / embeds) | [assets/sdaf-core-icon-build.gif](assets/sdaf-core-icon-build.gif) |
| Duración orientativa | ~1,4 s de construcción + hold (≥1 s); GIF ~4 s en loop |
| Accesibilidad | Respetar `prefers-reduced-motion` (mostrar V1 estático) |

**No usar** motion como favicon ni icono de sistema.

Ejemplo README:

```markdown
![SDAF Core](docs/assets/sdaf-core-icon-build.gif)
```

## Artefactos

| Archivo | Rol |
|---------|-----|
| [sdaf-core-icon.svg](assets/sdaf-core-icon.svg) | Mark color (C); logo y favicon del sitio docs |
| [sdaf-core-icon.png](assets/sdaf-core-icon.png) | Raster 512×512 (avatar GitHub / previews) |
| [sdaf-core-icon-mono.svg](assets/sdaf-core-icon-mono.svg) | Mark monocromo |
| [sdaf-core-lockup-horizontal.svg](assets/sdaf-core-lockup-horizontal.svg) | Lockup B |
| [sdaf-core-lockup-stacked.svg](assets/sdaf-core-lockup-stacked.svg) | Lockup A |
| [sdaf-core-icon-build.svg](assets/sdaf-core-icon-build.svg) | Motion SVG |
| [sdaf-core-icon-build.gif](assets/sdaf-core-icon-build.gif) | Motion GIF |
| [sdaf-core-icon-preview.html](assets/sdaf-core-icon-preview.html) | Preview interactivo |
| [stylesheets/branding.css](stylesheets/branding.css) | Variables de paleta en MkDocs Material |

Geometría del arco: debe caber en el viewBox con el trazo (el radio queda por debajo del tope superior del lienzo; no recortar el círculo).

## Dónde se aplica en este repo

| Superficie | Variante |
|------------|----------|
| [README.md](../README.md) | GIF build (motion) + enlace a esta guía |
| [docs/README.md](README.md) | Lockup horizontal (B) |
| Sitio MkDocs | Logo + favicon = mark C; paleta vía `branding.css` |
| Avatar / social (manual) | PNG 512 (`sdaf-core-icon.png`) en ajustes del repo en GitHub |

## No hacer

- Meter «SDAF» (ni otras letras) dentro del SVG de app/favicon.
- Sustituir V1 por V2/V3 en producción sin decisión explícita.
- Añadir un cuarto color al mark, filtros costosos o imágenes embebidas.
- Deformar, rotar arbitrariamente o recortar el margen de seguridad.
- Usar el GIF/SVG animado donde se espera un icono estático de sistema.
- Redibujar el mark «a ojo» en otro archivo: partir siempre de los SVG de `docs/assets/`.

## Relacionado

| | Destino | Por qué |
|--|---------|---------|
| 🛠️ | [README de docs](README.md) | Índice HOWTO del core |
| 🧭 | [mapa-navegacion.md](mapa-navegacion.md) | Vocabulario visual del método |
| 🧭 | [README del core](../README.md) | Tres puertas de entrada |
| 🖼️ | [sdaf-core-icon-preview.html](assets/sdaf-core-icon-preview.html) | Comparar V1/V2/V3, lockups y motion |
