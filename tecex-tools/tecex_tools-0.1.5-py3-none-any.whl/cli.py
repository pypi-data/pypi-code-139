import typer
import pandas as pd
import datetime
import os

# Local imports
from tecex_tools.helpers import RawBTAImport, RawBTImport

app = typer.Typer()


@app.command()
def test():
    typer.echo('test worked!')


@app.command()
def bta_imports(
        file_path: str = typer.Option(..., help="The absolute file path"),
        year: int = typer.Option(..., help="A year as an integer in the format YYYY"),
        month: int = typer.Option(..., help="A month as an integer in the format M or MM i.e. 1 - 12"),
        file_type: str = typer.Option(..., help="Either 'bt' or 'bta' are allowed")
):
    """A function to generate the BTA & BT Import File"""
    typer.secho(f"{' START '.center(100, '-')}")
    start_ts = datetime.datetime.utcnow()
    date_ = datetime.datetime(year, month, 1)
    records = None
    export_directory = os.path.dirname(file_path)
    export_file = f'{year}_{str(month).zfill(2)}__{file_type}_import_file.xlsx'
    export_path = os.path.join(export_directory, export_file)

    if file_type == 'bta':
        sheet_name = 'BTA Raw data'
        typer.secho(f'Will use sheet named: "{sheet_name}"', fg=typer.colors.WHITE)

    elif file_type == 'bt':
        sheet_name = 'BT Raw Data'
        typer.secho(f'Will use sheet named: "{sheet_name}"', fg=typer.colors.WHITE)

    else:
        typer.secho(
            f"Allowed file-type not provided, exiting application",
            fg=typer.colors.RED)
        raise typer.Exit()

    if os.path.isfile(file_path):
        typer.secho(f"File path provided exists -> '{file_path}'", fg=typer.colors.WHITE)
        if file_path.endswith('xlsx'):
            typer.secho('Excel file being processed', fg=typer.colors.WHITE)
            excel_data = pd.read_excel(file_path, sheet_name=None)

            if file_type == 'bta':
                bta = RawBTAImport(
                    data=excel_data.get(sheet_name),
                    report_date=date_)

                records = bta.create_report_records()

            elif file_type == 'bt':
                bt = RawBTImport(
                    data=excel_data.get(sheet_name),
                    report_date=date_)

                records = bt.create_report_records()

            if records:
                typer.secho(f'"{file_type}" report being compiled', fg=typer.colors.WHITE)
                pd.DataFrame(records).to_excel(export_path, index=False)
                typer.secho(f'EXPORT PATH -> "{export_path}"', fg=typer.colors.MAGENTA)
                duration = datetime.datetime.utcnow() - start_ts
                typer.secho(f'PROCESS COMPLETE. Duration: {duration}', fg=typer.colors.BRIGHT_GREEN)
                typer.secho(f"{' END '.center(100, '-')}")

        else:
            typer.secho('Unexpected file type provided', fg=typer.colors.YELLOW)
            raise typer.Exit()

    else:
        typer.secho(f"File path provided does not exist\n File path provided: '{file_path}'", fg=typer.colors.RED)
        raise typer.Exit()
