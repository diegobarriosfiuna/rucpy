# rucpy 🇵🇾

[![tests](https://github.com/diegobarriosfiuna/rucpy/actions/workflows/tests.yml/badge.svg)](https://github.com/diegobarriosfiuna/rucpy/actions/workflows/tests.yml)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![licencia](https://img.shields.io/badge/licencia-MIT-green)

Validá RUC paraguayos y calculá su dígito verificador (DV) en una línea. Sin dependencias.

Sirve para limpiar padrones de clientes y proveedores antes de migrar a un ERP, validar formularios, o preparar datos para facturación electrónica (SIFEN).

## Instalación

```bash
pip install git+https://github.com/diegobarriosfiuna/rucpy.git
```

## Uso en Python

```python
>>> from rucpy import calcular_dv, validar, es_valido, formatear
>>> calcular_dv("80000519")
8
>>> es_valido("80.000.519-8")
True
>>> es_valido("80000519-1")
False
>>> formatear("80000519")
'80000519-8'
>>> validar("80000519-1")
Traceback (most recent call last):
...
rucpy.core.RucInvalidoError: DV incorrecto para 80000519: se recibió 1, corresponde 8.

```

## Línea de comandos

```bash
rucpy validar 80000519-8 1234567-9
rucpy dv 80000519
rucpy csv clientes.csv --columna ruc > clientes_validados.csv
```

El comando `csv` agrega dos columnas (`ruc_valido`, `ruc_detalle`) y devuelve código de salida 1 si encontró algún RUC inválido, así que sirve como chequeo en un pipeline de migración.

## Cómo funciona

El DV se calcula con el algoritmo **módulo 11** que publica la SET (hoy DNIT):

1. Se recorre el número de derecha a izquierda.
2. Cada dígito se multiplica por un factor que arranca en 2, sube hasta 11 y vuelve a 2.
3. Se suma todo y se obtiene el resto de dividir por 11.
4. Si el resto es mayor que 1, el DV es `11 - resto`; si no, es `0`.

Si el número trae letras, se reemplazan por su código ASCII antes del cálculo, igual que en la rutina oficial.

## Desarrollo

```bash
git clone https://github.com/diegobarriosfiuna/rucpy.git
cd rucpy
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest --cov=rucpy
```

## Hoja de ruta

- [ ] Validación de cédula de identidad
- [ ] Integración opcional con la consulta pública de RUC
- [ ] Publicación en PyPI

Las contribuciones son bienvenidas: abrí un issue o mandá un PR.

## Licencia

MIT © Diego Raúl Barrios
