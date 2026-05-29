# CV Forge

Generador de CVs con patron maestro/derivado. Un perfil maestro con toda tu experiencia profesional → infinitas versiones adaptadas a cada postulacion.

## Como funciona

```
profiles/tu_nombre.json        ← MAESTRO (toda tu experiencia en JSON)
       │
       ├── derivados/tu_nombre/dev_junior.json    → output/PDF
       ├── derivados/tu_nombre/ventas_retail.json  → output/PDF
       └── derivados/tu_nombre/creativo.json       → output/PDF
```

1. **Maestro JSON** — Toda tu experiencia laboral, educacion, habilidades en un solo archivo
2. **Derivado JSON** — Filtros + objetivo laboral: que experiencia mostrar, que perfil enfatizar
3. **`generate.py`** — Combina maestro + derivado → PDF con ReportLab

## Caracteristicas

- **Text wrapping automatico** — Todo texto largo se ajusta dentro de los margenes sin cortarse
- **Layout two-column** — Sidebar (perfil, habilidades, educacion) + columna principal (experiencia)
- **5 paletas de color** — Azul acero, cyan, verde tech, violeta creativo, gris profesional
- **Footer automatico** — Pie de pagina personalizable
- **Emojis en header** — Iconos de contacto (telefono, email)
- **Multiplataforma** — Fuentes Noto Sans (libres), funciona en Windows/Mac/Linux

## Instalacion

```bash
git clone https://github.com/vpino/cv-forge.git
cd cv-forge
pip install -r requirements.txt
```

### Fuentes

CV Forge usa Noto Sans (libre, multiplataforma). Las fuentes ya estan incluidas en `fonts/`:

- `NotoSans-Regular.ttf`
- `NotoSans-Bold.ttf`
- `NotoSans-Italic.ttf`
- `NotoSans-SemiBold.ttf`

## Uso

```bash
# Listar perfiles disponibles
python generate.py

# Listar derivados de un perfil
python generate.py demo

# Generar PDF
python generate.py demo fullstack_dev
```

## Crear tu perfil

1. Copia `profiles/_TEMPLATE.json` → `profiles/tu_nombre.json`
2. Llena con tu experiencia completa (este es tu maestro)
3. Crea derivados en `derivados/tu_nombre/` para cada tipo de postulacion

### Ejemplo de derivado

```json
{
  "_meta": { "version": "3.0", "type": "derivado", "persona_id": "tu_nombre", "derivado_id": "ventas_retail" },
  "config": {
    "nombre": "Vendedor Retail",
    "objetivo_laboral": "Vendedor Polifuncional Retail",
    "perfil_profesional": "Tu perfil adaptado a este rol...",
    "experiencias_incluir": ["empresa1_2025", "empresa2_2023"],
    "experiencias_ocultar": ["empresa3_2020"],
    "habilidades_destacar": ["Atencion al cliente", "Gestion de caja"],
    "layout": "two_col_sidebar",
    "paleta": "azul_acero"
  }
}
```

## Layouts

| Layout | Descripcion |
|--------|-------------|
| `single_col` | Una columna, experiencia arriba, habilidades abajo |
| `two_col_sidebar` | Sidebar 30% (perfil, habilidades, educacion, idiomas) + columna 70% (experiencia) |

## Paletas de color

| Paleta | Uso | Preview |
|--------|-----|---------|
| `azul_acero` | Profesional, general | Titulos azul oscuro, sidebar gris claro |
| `cyan_krgn` | Tech, energia | Titulos cyan, sidebar celeste claro |
| `verde_tech` | Desarrollo de software | Titulos verde oscuro, sidebar verde claro |
| `violeta_creativo` | Roles creativos | Titulos violeta, sidebar lavanda |
| `gris_profesional` | Corporativo, formal | Titulos negro, sidebar gris |

## Arquitectura

```
engine/
├── loader.py       # Carga maestros, derivados, filtra experiencia/habilidades
├── pdf_builder.py  # Genera PDF con ReportLab (text wrapping, two-col, footer)
└── styles.py       # 5 paletas, fuentes Noto Sans, tamanos, espaciados

fonts/
├── NotoSans-Regular.ttf
├── NotoSans-Bold.ttf
├── NotoSans-Italic.ttf
└── NotoSans-SemiBold.ttf
```

## Stack

- **Python 3.11+**
- **ReportLab** — Generacion de PDFs
- **JSON** — Base de datos (sin dependencias externas)

## Changelog

### v3.1 — Junio 2026
- Text wrapping automatico en todas las secciones
- Footer personalizable
- Sidebar optimizado a 30% para mas espacio en experiencia
- 5 paletas de color (cyan_krgn nueva)
- Font sizes e interlineado ajustados para maxima densidad legible
- Emojis restaurados en header
- Fuentes Noto Sans incluidas en el repo

### v3.0 — Mayo 2026
- Version inicial: maestro/derivado, single_col, two_col_sidebar
- Paleta azul_acero
- ReportLab PDF generation

## Licencia

MIT — Usa, modifica, comparte.

## Autor

Victor Pino — [GitHub](https://github.com/vpino)
