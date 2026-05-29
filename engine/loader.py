import json
from pathlib import Path

PROFILES_DIR = Path(__file__).parent.parent / "profiles"
DERIVADOS_DIR = Path(__file__).parent.parent / "derivados"
OUTPUT_DIR = Path(__file__).parent.parent / "output"


def load_maestro(persona_id: str) -> dict:
    path = PROFILES_DIR / f"{persona_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Perfil maestro no encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_derivado(persona_id: str, derivado_id: str) -> dict:
    path = DERIVADOS_DIR / persona_id / f"{derivado_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Derivado no encontrado: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_perfiles() -> list[str]:
    return [
        p.stem
        for p in PROFILES_DIR.glob("*.json")
        if not p.stem.startswith("_")
    ]


def list_derivados(persona_id: str) -> list[str]:
    dir_path = DERIVADOS_DIR / persona_id
    if not dir_path.exists():
        return []
    return [p.stem for p in dir_path.glob("*.json")]


def filtrar_experiencia(maestro: dict, config: dict) -> list[dict]:
    incluir = set(config.get("experiencias_incluir", []))
    ocultar = set(config.get("experiencias_ocultar", []))
    if incluir:
        return [e for e in maestro["experiencia"] if e["id"] in incluir]
    if ocultar:
        return [e for e in maestro["experiencia"] if e["id"] not in ocultar]
    return maestro["experiencia"]


def filtrar_habilidades(maestro: dict, config: dict) -> dict:
    destacar = set(config.get("habilidades_destacar", []))
    habilidades = maestro.get("habilidades", {})
    if not destacar:
        return habilidades
    filtradas = {}
    for cat_key, cat_data in habilidades.items():
        items = [i for i in cat_data["items"] if i in destacar]
        if items:
            filtradas[cat_key] = {**cat_data, "items": items}
    return filtradas


def build_cv_data(persona_id: str, derivado_id: str) -> dict:
    maestro = load_maestro(persona_id)
    derivado = load_derivado(persona_id, derivado_id)
    config = derivado["config"]

    return {
        "persona": maestro["persona"],
        "objetivo_laboral": config.get("objetivo_laboral", ""),
        "perfil_profesional": config.get("perfil_profesional", ""),
        "experiencia": filtrar_experiencia(maestro, config),
        "educacion": maestro.get("educacion", []),
        "habilidades": filtrar_habilidades(maestro, config),
        "idiomas": maestro.get("idiomas", []),
        "disponibilidad": config.get("disponibilidad_custom", maestro["persona"].get("disponibilidad_base", "")),
        "referencias": maestro.get("referencias", "Disponibles bajo solicitud"),
        "layout": config.get("layout", "single_col"),
        "paleta": config.get("paleta", "azul_acero"),
    }
