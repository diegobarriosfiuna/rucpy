"""rucpy — validación y cálculo del dígito verificador del RUC paraguayo."""

from .core import (
    ResultadoRuc,
    RucInvalidoError,
    calcular_dv,
    es_valido,
    formatear,
    normalizar,
    separar,
    validar,
)

__version__ = "0.1.0"

__all__ = [
    "ResultadoRuc",
    "RucInvalidoError",
    "__version__",
    "calcular_dv",
    "es_valido",
    "formatear",
    "normalizar",
    "separar",
    "validar",
]
