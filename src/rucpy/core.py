"""Cálculo y validación del dígito verificador (DV) del RUC paraguayo.

El algoritmo es el módulo 11 publicado por la SET (DNIT): se recorre el número
de derecha a izquierda multiplicando cada dígito por un factor que va de 2
hasta ``base_max`` (11) y vuelve a empezar en 2. Los caracteres no numéricos
se reemplazan por su código ASCII, igual que en la implementación oficial.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = [
    "ResultadoRuc",
    "RucInvalidoError",
    "calcular_dv",
    "es_valido",
    "formatear",
    "normalizar",
    "separar",
    "validar",
]

_LIMPIEZA = re.compile(r"[\s.]")
_PATRON = re.compile(r"^([0-9A-Za-z]{1,8})-?([0-9])$")


class RucInvalidoError(ValueError):
    """Se lanza cuando un RUC no tiene formato válido o su DV no coincide."""


@dataclass(frozen=True)
class ResultadoRuc:
    numero: str
    dv: int

    @property
    def completo(self) -> str:
        return f"{self.numero}-{self.dv}"

    def __str__(self) -> str:
        return self.completo


def _a_digitos(numero: str) -> str:
    """Reemplaza caracteres no numéricos por su código ASCII (regla de la SET)."""
    return "".join(c if c.isdigit() else str(ord(c.upper())) for c in numero)


def calcular_dv(numero: str | int, base_max: int = 11) -> int:
    """Calcula el dígito verificador de un número de RUC (sin el DV).

    >>> calcular_dv("80000519")
    8
    """
    numero = _LIMPIEZA.sub("", str(numero))
    if not numero or not numero.isalnum():
        raise RucInvalidoError(f"Número de RUC vacío o con caracteres inválidos: {numero!r}")

    total = 0
    factor = 2
    for caracter in reversed(_a_digitos(numero)):
        total += int(caracter) * factor
        factor = 2 if factor >= base_max else factor + 1

    resto = total % 11
    return 11 - resto if resto > 1 else 0


def normalizar(ruc: str | int) -> str:
    """Quita espacios y puntos: ``' 80.000.519 - 8 '`` -> ``'80000519-8'``."""
    return _LIMPIEZA.sub("", str(ruc))


def separar(ruc: str | int) -> tuple[str, int]:
    """Devuelve ``(numero, dv)`` de un RUC con formato válido, sin verificar el DV."""
    limpio = normalizar(ruc)
    m = _PATRON.match(limpio)
    if not m:
        raise RucInvalidoError(
            f"Formato inválido: {ruc!r}. Se espera algo como '80000519-8'."
        )
    return m.group(1).upper(), int(m.group(2))


def validar(ruc: str | int) -> ResultadoRuc:
    """Valida un RUC completo y devuelve el resultado o lanza ``RucInvalidoError``."""
    numero, dv = separar(ruc)
    esperado = calcular_dv(numero)
    if dv != esperado:
        raise RucInvalidoError(
            f"DV incorrecto para {numero}: se recibió {dv}, corresponde {esperado}."
        )
    return ResultadoRuc(numero=numero, dv=dv)


def es_valido(ruc: str | int) -> bool:
    """Versión booleana de :func:`validar`."""
    try:
        validar(ruc)
    except RucInvalidoError:
        return False
    return True


def formatear(numero: str | int) -> str:
    """Agrega el DV a un número de RUC: ``'80000519'`` -> ``'80000519-8'``."""
    limpio = normalizar(numero).upper()
    return f"{limpio}-{calcular_dv(limpio)}"
