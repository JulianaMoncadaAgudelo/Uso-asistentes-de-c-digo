"""Pruebas básicas del `main` CLI (comandos que no requieren interacción)."""
from pathlib import Path
import tempfile
import os

from click.testing import CliRunner
from employee_manager.main import main


def test_init_db_and_list_commands():
    runner = CliRunner()
    tmpdir = tempfile.TemporaryDirectory()
    data_dir = tmpdir.name

    try:
        # init-db
        res = runner.invoke(main, ["init-db", "--data-dir", data_dir])
        assert res.exit_code == 0
        assert Path(data_dir, "empleados.json").exists()
        assert Path(data_dir, "contratos.json").exists()

        # list-employees (empty)
        res2 = runner.invoke(main, ["list-employees", "--file", str(Path(data_dir, "empleados.json"))])
        assert res2.exit_code == 0

        # list-contracts (empty)
        res3 = runner.invoke(main, ["list-contracts", "--file", str(Path(data_dir, "contratos.json"))])
        assert res3.exit_code == 0
    finally:
        tmpdir.cleanup()
