import pytest
import json
import tempfile
import os
from pathlib import Path

from engine.loader import (
    load_maestro,
    load_derivado,
    list_perfiles,
    list_derivados,
    filtrar_experiencia,
    filtrar_habilidades,
    build_cv_data,
)


@pytest.fixture
def demo_profile(tmp_path):
    profiles = tmp_path / "profiles"
    profiles.mkdir()
    data = {
        "_meta": {"version": "3.0", "type": "maestro", "persona_id": "test"},
        "persona": {
            "nombre_completo": "Test User",
            "contacto": {"telefono": "+56 9 1234", "email": "test@test.com"},
            "ubicacion": "Santiago",
            "disponibilidad_base": "Inmediata"
        },
        "experiencia": [
            {"id": "job_a", "cargo": "Dev", "empresa": "Corp A", "area": "tech",
             "periodo": {"inicio": "2025-01", "fin": "presente"}, "duracion_texto": "2025 - Presente",
             "responsabilidades": ["Coding"], "logros": ["Shipped"], "habilidades": ["Python"]},
            {"id": "job_b", "cargo": "Vendedor", "empresa": "Shop B", "area": "retail",
             "periodo": {"inicio": "2023-01", "fin": "2024-12"}, "duracion_texto": "2 años",
             "responsabilidades": ["Selling"], "habilidades": ["Ventas"]},
        ],
        "educacion": [{"id": "uni", "titulo": "CS", "institucion": "Uni", "periodo": "2020", "estado": "completa"}],
        "habilidades": {
            "tech": {"emoji": "DEV", "nombre": "Desarrollo", "items": ["Python", "Git"]},
            "soft": {"emoji": "SOFT", "nombre": "Blandas", "items": ["Comunicacion", "Trabajo en equipo"]},
        },
        "idiomas": [{"idioma": "Espanol", "nivel": "Nativo"}],
        "referencias": "Disponibles"
    }
    (profiles / "test.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return tmp_path


@pytest.fixture
def demo_derivado(tmp_path):
    derivados = tmp_path / "derivados" / "test"
    derivados.mkdir(parents=True)
    data = {
        "_meta": {"version": "3.0", "type": "derivado", "persona_id": "test", "derivado_id": "dev_jr"},
        "config": {
            "nombre": "Dev Junior",
            "objetivo_laboral": "Python Developer",
            "perfil_profesional": "Junior dev with retail background",
            "experiencias_incluir": ["job_a"],
            "habilidades_destacar": ["Python", "Git"],
            "layout": "two_col_sidebar",
            "paleta": "azul_acero"
        }
    }
    (derivados / "dev_jr.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return tmp_path


class TestListPerfiles:
    def test_lists_profiles(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        result = list_perfiles()
        assert "test" in result
        assert "_TEMPLATE" not in result

    def test_empty_dir(self, tmp_path, monkeypatch):
        import engine.loader as loader
        empty = tmp_path / "profiles"
        empty.mkdir()
        monkeypatch.setattr(loader, "PROFILES_DIR", empty)
        assert list_perfiles() == []


class TestListDerivados:
    def test_lists_derivados(self, demo_derivado, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "DERIVADOS_DIR", demo_derivado / "derivados")
        result = list_derivados("test")
        assert "dev_jr" in result

    def test_no_derivados(self, tmp_path, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "DERIVADOS_DIR", tmp_path / "derivados")
        assert list_derivados("nonexistent") == []


class TestLoadMaestro:
    def test_loads_valid(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        data = load_maestro("test")
        assert data["persona"]["nombre_completo"] == "Test User"
        assert len(data["experiencia"]) == 2

    def test_raises_on_missing(self, tmp_path, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", tmp_path / "profiles")
        (tmp_path / "profiles").mkdir()
        with pytest.raises(FileNotFoundError):
            load_maestro("ghost")


class TestLoadDerivado:
    def test_loads_valid(self, demo_derivado, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "DERIVADOS_DIR", demo_derivado / "derivados")
        data = load_derivado("test", "dev_jr")
        assert data["config"]["objetivo_laboral"] == "Python Developer"


class TestFiltrarExperiencia:
    def test_incluir(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        maestro = load_maestro("test")
        config = {"experiencias_incluir": ["job_a"]}
        result = filtrar_experiencia(maestro, config)
        assert len(result) == 1
        assert result[0]["id"] == "job_a"

    def test_ocultar(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        maestro = load_maestro("test")
        config = {"experiencias_ocultar": ["job_b"]}
        result = filtrar_experiencia(maestro, config)
        assert len(result) == 1
        assert result[0]["id"] == "job_a"

    def test_no_filter(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        maestro = load_maestro("test")
        result = filtrar_experiencia(maestro, {})
        assert len(result) == 2


class TestFiltrarHabilidades:
    def test_destacar(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        maestro = load_maestro("test")
        config = {"habilidades_destacar": ["Python"]}
        result = filtrar_habilidades(maestro, config)
        assert "tech" in result
        assert "Python" in result["tech"]["items"]
        assert "Git" not in result["tech"]["items"]

    def test_no_filter(self, demo_profile, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        maestro = load_maestro("test")
        result = filtrar_habilidades(maestro, {})
        assert len(result["tech"]["items"]) == 2


class TestBuildCVData:
    def test_full_build(self, demo_profile, demo_derivado, monkeypatch):
        import engine.loader as loader
        monkeypatch.setattr(loader, "PROFILES_DIR", demo_profile / "profiles")
        monkeypatch.setattr(loader, "DERIVADOS_DIR", demo_derivado / "derivados")
        data = build_cv_data("test", "dev_jr")
        assert data["persona"]["nombre_completo"] == "Test User"
        assert data["objetivo_laboral"] == "Python Developer"
        assert len(data["experiencia"]) == 1
        assert data["layout"] == "two_col_sidebar"
        assert data["paleta"] == "azul_acero"
