#!/usr/bin/env python3
"""KRGN CV System v3.0 - Generador de CVs

Uso:
    python generate.py                          # Listar perfiles disponibles
    python generate.py victor_pino              # Listar derivados de Victor
    python generate.py victor_pino walmart      # Generar PDF
    python generate.py nina_echenique retail_moda  # Generar PDF Nina
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from engine.loader import list_perfiles, list_derivados, load_maestro
from engine.pdf_builder import generate_pdf, _register_fonts


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("KRGN CV System v3.0")
        print("=" * 40)
        print("\nPerfiles disponibles:")
        for p in list_perfiles():
            maestro = load_maestro(p)
            nombre = maestro["persona"].get("nombre_completo", p)
            nombre_corto = maestro["persona"].get("nombre_corto", "")
            derivados = list_derivados(p)
            print(f"  {p}: {nombre} ({nombre_corto})")
            if derivados:
                print(f"    Derivados: {', '.join(derivados)}")
            else:
                print("    Sin derivados")
        print(f"\nUso: python generate.py <persona_id> <derivado_id>")
        return

    persona_id = args[0]

    if len(args) == 1:
        derivados = list_derivados(persona_id)
        if not derivados:
            print(f"Sin derivados para '{persona_id}'. Crear uno en derivados/{persona_id}/")
            return
        maestro = load_maestro(persona_id)
        nombre = maestro["persona"].get("nombre_completo", persona_id)
        print(f"Derivados de {nombre}:")
        for d in derivados:
            derivado = load_derivado_maestro(persona_id, d)
            config = derivado.get("config", {})
            print(f"  {d}: {config.get('objetivo_laboral', 'sin objetivo')}")
        print(f"\nGenerar: python generate.py {persona_id} <derivado_id>")
        return

    derivado_id = args[1]
    print(f"Generando CV: {persona_id}/{derivado_id}...")

    try:
        _register_fonts()
        path = generate_pdf(persona_id, derivado_id)
        print(f"PDF generado: {path}")
        print(f"Tamaño: {path.stat().st_size / 1024:.1f} KB")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error generando PDF: {e}")


def load_derivado_maestro(persona_id, derivado_id):
    from engine.loader import load_derivado
    return load_derivado(persona_id, derivado_id)


if __name__ == "__main__":
    main()
