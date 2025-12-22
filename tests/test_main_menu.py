"""Tests for interactive menu (basic flows simulated)."""
from click.testing import CliRunner
import tempfile
from pathlib import Path
import os

from employee_manager.main import main


def test_menu_exit_immediately():
    runner = CliRunner()
    tmpdir = tempfile.TemporaryDirectory()
    try:
        res = runner.invoke(main, ["menu", "--data-dir", tmpdir.name], input="0\n")
        assert res.exit_code == 0
    finally:
        tmpdir.cleanup()


def test_menu_add_and_list_employee():
    runner = CliRunner()
    tmpdir = tempfile.TemporaryDirectory()
    data_dir = tmpdir.name
    try:
        # sequence: 1(add), id, first, last, email(empty), 2(list), 0(exit)
        inputs = "1\ne1\nAna\nLopez\n\n2\n0\n"
        res = runner.invoke(main, ["menu", "--data-dir", data_dir], input=inputs)
        assert res.exit_code == 0
        # should contain the employee id or name in output
        assert "e1" in res.output or "Ana" in res.output
    finally:
        tmpdir.cleanup()
