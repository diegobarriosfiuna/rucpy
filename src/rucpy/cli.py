"""Línea de comandos: ``rucpy validar 80000519-8`` / ``rucpy dv 80000519``."""

from __future__ import annotations

import argparse
import csv
import sys

from . import __version__
from .core import RucInvalidoError, calcular_dv, validar


def _cmd_validar(args: argparse.Namespace) -> int:
    codigo = 0
    for ruc in args.ruc:
        try:
            resultado = validar(ruc)
            print(f"OK       {resultado}")
        except RucInvalidoError as e:
            print(f"INVÁLIDO {ruc}: {e}")
            codigo = 1
    return codigo


def _cmd_dv(args: argparse.Namespace) -> int:
    codigo = 0
    for numero in args.numero:
        try:
            print(f"{numero}-{calcular_dv(numero)}")
        except RucInvalidoError as e:
            print(f"ERROR    {numero}: {e}", file=sys.stderr)
            codigo = 1
    return codigo


def _cmd_csv(args: argparse.Namespace) -> int:
    lector = csv.DictReader(args.archivo)
    if lector.fieldnames is None or args.columna not in lector.fieldnames:
        print(f"La columna {args.columna!r} no existe en el CSV.", file=sys.stderr)
        return 2
    campos = list(lector.fieldnames) + ["ruc_valido", "ruc_detalle"]
    escritor = csv.DictWriter(sys.stdout, fieldnames=campos)
    escritor.writeheader()
    invalidos = 0
    for fila in lector:
        try:
            fila["ruc_detalle"] = validar(fila[args.columna]).completo
            fila["ruc_valido"] = "si"
        except RucInvalidoError as e:
            fila["ruc_valido"] = "no"
            fila["ruc_detalle"] = str(e)
            invalidos += 1
        escritor.writerow(fila)
    return 1 if invalidos else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rucpy", description="Validador de RUC paraguayo (módulo 11, SET/DNIT)."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_val = sub.add_parser("validar", help="Valida uno o más RUC completos (con DV).")
    p_val.add_argument("ruc", nargs="+")
    p_val.set_defaults(func=_cmd_validar)

    p_dv = sub.add_parser("dv", help="Calcula el DV de uno o más números de RUC.")
    p_dv.add_argument("numero", nargs="+")
    p_dv.set_defaults(func=_cmd_dv)

    p_csv = sub.add_parser("csv", help="Valida una columna de un CSV y agrega el resultado.")
    p_csv.add_argument("archivo", type=argparse.FileType("r", encoding="utf-8"))
    p_csv.add_argument("--columna", default="ruc")
    p_csv.set_defaults(func=_cmd_csv)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
