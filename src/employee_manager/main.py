"""Interfaz principal en terminal usando click + rich."""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .json_storage import JsonStorage
from .gestor_empleados import (
    agregar_empleado,
    eliminar_empleado,
    buscar_empleado,
    listar_empleados,
)
from .gestor_contratos import (
    asociar_contrato,
    listar_contratos_vencidos,
)

console = Console()

DATA_DIR = Path("data")
EMP_FILE = DATA_DIR / "empleados.json"


@click.group()
def main():
    """Interfaz principal para el gestor de empleados y contratos."""
    pass


@main.command(name="init-db")
@click.option("--data-dir", "data_dir", default=str(DATA_DIR), help="Directorio donde crear JSON")
def init_db(data_dir: str):
    """Crear archivo JSON vacío para empleados."""
    p = Path(data_dir)
    p.mkdir(parents=True, exist_ok=True)
    (p / "empleados.json").write_text('{"empleados": []}', encoding="utf-8")
    console.print(f":white_check_mark: Base inicializada en [bold]{p}[/bold]")


def _print_employees_table(storage: JsonStorage) -> None:
    """Imprimir tabla de empleados."""
    empleados = listar_empleados(storage)
    table = Table(title="Empleados")
    table.add_column("ID")
    table.add_column("Nombre")
    table.add_column("Cargo")
    table.add_column("Contratos")
    for emp in empleados:
        num_contratos = len(emp.get("contratos", []))
        table.add_row(
            str(emp.get("id", "")),
            emp.get("nombre", ""),
            emp.get("cargo", ""),
            str(num_contratos)
        )
    console.print(table)


@main.command(name="list-employees")
@click.option("--file", "file_path", default=str(EMP_FILE), help="Archivo JSON de empleados")
def cli_list_employees(file_path: str):
    """Listar todos los empleados."""
    storage = JsonStorage(file_path)
    _print_employees_table(storage)


@main.command(name="menu")
@click.option("--data-dir", "data_dir", default=str(DATA_DIR), help="Directorio de datos a usar")
def menu(data_dir: str):
    """Menú interactivo con opciones numeradas para interactuar con el sistema."""
    p = Path(data_dir)
    p.mkdir(parents=True, exist_ok=True)
    emp_file = p / "empleados.json"
    if not emp_file.exists():
        emp_file.write_text('{"empleados": []}', encoding="utf-8")

    storage = JsonStorage(str(emp_file))

    while True:
        menu_text = (
            "[bold cyan]Gestor de Empleados y Contratos - Menú[/bold cyan]\n"
            "[bold]1[/bold]) Agregar empleado\n"
            "[bold]2[/bold]) Listar empleados\n"
            "[bold]3[/bold]) Buscar empleado\n"
            "[bold]4[/bold]) Eliminar empleado\n"
            "[bold]5[/bold]) Asociar contrato a empleado\n"
            "[bold]6[/bold]) Listar contratos vencidos\n"
            "[bold]7[/bold]) Inicializar base (reset)\n"
            "[bold]0[/bold]) Salir\n"
        )
        console.print(menu_text)
        try:
            choice = click.prompt("Selecciona una opción", type=int)
        except click.Abort:
            console.print(":x: Entrada abortada. Saliendo.")
            break

        if choice == 0:
            break
        if choice == 7:
            init_db(str(p))
            continue

        try:
            if choice == 1:
                nombre = click.prompt("Nombre del empleado", type=str)
                cargo = click.prompt("Cargo del empleado", type=str)
                empleado = agregar_empleado(nombre, cargo, storage)
                console.print(f":white_check_mark: Empleado '{empleado['nombre']}' (ID: {empleado['id']}) agregado")

            elif choice == 2:
                _print_employees_table(storage)

            elif choice == 3:
                emp_id = click.prompt("ID del empleado a buscar", type=int)
                empleado = buscar_empleado(emp_id, storage)
                if empleado:
                    console.print(f"\n[bold]Empleado encontrado:[/bold]")
                    console.print(f"ID: {empleado.get('id')}")
                    console.print(f"Nombre: {empleado.get('nombre')}")
                    console.print(f"Cargo: {empleado.get('cargo')}")
                    contratos = empleado.get("contratos", [])
                    console.print(f"Contratos: {len(contratos)}")
                    if contratos:
                        table = Table(title="Contratos del empleado")
                        table.add_column("ID Contrato")
                        table.add_column("Fecha Inicio")
                        table.add_column("Fecha Fin")
                        table.add_column("Salario")
                        for c in contratos:
                            table.add_row(
                                str(c.get("id_contrato", "")),
                                c.get("fecha_inicio", ""),
                                c.get("fecha_fin", ""),
                                str(c.get("salario", ""))
                            )
                        console.print(table)
                else:
                    console.print(f":x: Empleado con id '{emp_id}' no encontrado")

            elif choice == 4:
                emp_id = click.prompt("ID del empleado a eliminar", type=int)
                if click.confirm(f"Confirmar eliminación de empleado '{emp_id}'?"):
                    resultado = eliminar_empleado(emp_id, storage)
                    if resultado:
                        console.print(f":white_check_mark: Empleado '{emp_id}' eliminado")
                    else:
                        console.print(f":x: Empleado con id '{emp_id}' no encontrado")

            elif choice == 5:
                emp_id = click.prompt("ID del empleado", type=int)
                fecha_inicio = click.prompt("Fecha inicio (YYYY-MM-DD)", type=str)
                fecha_fin = click.prompt("Fecha fin (YYYY-MM-DD)", type=str)
                salario = click.prompt("Salario", type=float)
                contrato = asociar_contrato(emp_id, fecha_inicio, fecha_fin, salario, storage)
                console.print(f":white_check_mark: Contrato '{contrato['id_contrato']}' asociado al empleado '{emp_id}'")

            elif choice == 6:
                contratos_vencidos = listar_contratos_vencidos(storage)
                if contratos_vencidos:
                    console.print(f"\n[bold]Contratos vencidos:[/bold] {len(contratos_vencidos)}")
                    table = Table()
                    table.add_column("ID Contrato")
                    table.add_column("ID Empleado")
                    table.add_column("Nombre Empleado")
                    table.add_column("Cargo")
                    table.add_column("Fecha Inicio")
                    table.add_column("Fecha Fin")
                    table.add_column("Salario")
                    for c in contratos_vencidos:
                        table.add_row(
                            str(c.get("id_contrato", "")),
                            str(c.get("id_empleado", "")),
                            c.get("nombre_empleado", ""),
                            c.get("cargo_empleado", ""),
                            c.get("fecha_inicio", ""),
                            c.get("fecha_fin", ""),
                            str(c.get("salario", ""))
                        )
                    console.print(table)
                else:
                    console.print(":white_check_mark: No hay contratos vencidos")

            else:
                console.print(":warning: Opción no válida")

        except ValueError as exc:
            console.print(f":x: Error: {exc}")
        except Exception as exc:
            console.print(f":x: Error inesperado: {exc}")


if __name__ == "__main__":
    main()
