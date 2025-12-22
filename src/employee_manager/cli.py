"""CLI (esqueleto) para el gestor de empleados."""
import click
from .json_storage import JsonStorage


@click.group()
def cli():
    """Comandos para administrar empleados y contratos."""
    pass


@cli.command(name="init-db")
@click.argument("file_path")
def init_db(file_path: str):
    """Inicializa un archivo JSON vacío (esqueleto)."""
    # TODO: crear archivo y escribir []
    click.echo(f"Inicializar archivo JSON: {file_path}")


@cli.command(name="list-employees")
@click.option("--file", "file_path", required=True, help="Ruta al archivo JSON")
def list_employees(file_path: str):
    """Listar empleados (esqueleto)."""
    # TODO: cargar datos y mostrar listados formateados
    click.echo(f"Listar empleados desde: {file_path}")


if __name__ == "__main__":
    cli()
