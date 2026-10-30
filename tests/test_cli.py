
from rucpy.cli import main


def test_validar_ok(capsys):
    assert main(["validar", "80000519-8"]) == 0
    assert "OK" in capsys.readouterr().out


def test_validar_invalido(capsys):
    assert main(["validar", "80000519-1"]) == 1
    assert "INVÁLIDO" in capsys.readouterr().out


def test_dv(capsys):
    assert main(["dv", "80000519"]) == 0
    assert capsys.readouterr().out.strip() == "80000519-8"


def test_csv(tmp_path, capsys):
    archivo = tmp_path / "clientes.csv"
    archivo.write_text("nombre,ruc\nA,80000519-8\nB,80000519-2\n", encoding="utf-8")
    assert main(["csv", str(archivo)]) == 1
    salida = capsys.readouterr().out.splitlines()
    assert salida[0] == "nombre,ruc,ruc_valido,ruc_detalle"
    assert salida[1].startswith("A,80000519-8,si")
    assert ",no," in salida[2]
