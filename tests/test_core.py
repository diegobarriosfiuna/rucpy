import pytest

from rucpy import (
    RucInvalidoError,
    calcular_dv,
    es_valido,
    formatear,
    normalizar,
    separar,
    validar,
)


def dv_referencia(numero: str) -> int:
    """Implementación independiente y directa del módulo 11, para contrastar."""
    digitos = "".join(c if c.isdigit() else str(ord(c.upper())) for c in numero)
    total = sum(int(d) * (2 + i % 10) for i, d in enumerate(reversed(digitos)))
    resto = total % 11
    return 11 - resto if resto > 1 else 0


@pytest.mark.parametrize(
    "numero, esperado",
    [
        ("80000519", 8),  # 9*2+1*3+5*4+8*9 = 113 -> resto 3  -> 11-3  = 8
        ("1", 9),         # 1*2 = 2                -> resto 2  -> 11-2  = 9
        ("5", 1),         # 5*2 = 10               -> resto 10 -> 11-10 = 1
        ("11", 6),        # 1*2+1*3 = 5            -> resto 5  -> 11-5  = 6
    ],
)
def test_casos_calculados_a_mano(numero, esperado):
    assert calcular_dv(numero) == esperado


def test_resto_0_y_1_dan_dv_0():
    assert calcular_dv("6") == 0  # 6*2 = 12 -> resto 1 -> DV 0
    assert calcular_dv("0") == 0  # 0         -> resto 0 -> DV 0


def test_factor_reinicia_despues_de_11():
    # 12 dígitos "1": factores 2..11 (suma 65), luego reinicia en 2 y 3 -> 70
    # 70 % 11 = 4 -> DV 7
    assert calcular_dv("1" * 12) == 7


@pytest.mark.parametrize("numero", [str(n) for n in range(1, 5000, 37)] + ["12345678", "99999999"])
def test_coincide_con_referencia(numero):
    assert calcular_dv(numero) == dv_referencia(numero)


def test_acepta_entero_y_puntos():
    assert calcular_dv(80000519) == 8
    assert calcular_dv("80.000.519") == 8


def test_caracteres_alfabeticos_usan_ascii():
    assert calcular_dv("1234567A") == dv_referencia("1234567A")


def test_validar_ok():
    r = validar("80000519-8")
    assert r.numero == "80000519"
    assert r.dv == 8
    assert str(r) == "80000519-8"


@pytest.mark.parametrize("ruc", ["80000519-8", " 80.000.519 - 8 ", "800005198"])
def test_validar_formatos_tolerados(ruc):
    assert es_valido(ruc)


@pytest.mark.parametrize("ruc", ["80000519-7", "", "abc", "123456789-0", "8000-05-19-8"])
def test_invalidos(ruc):
    assert not es_valido(ruc)
    with pytest.raises(RucInvalidoError):
        validar(ruc)


def test_mensaje_indica_dv_correcto():
    with pytest.raises(RucInvalidoError, match="corresponde 8"):
        validar("80000519-1")


def test_formatear_y_separar():
    assert formatear("80000519") == "80000519-8"
    assert separar("80000519-8") == ("80000519", 8)
    assert normalizar(" 80.000.519-8 ") == "80000519-8"


def test_calcular_dv_vacio():
    with pytest.raises(RucInvalidoError):
        calcular_dv("")
