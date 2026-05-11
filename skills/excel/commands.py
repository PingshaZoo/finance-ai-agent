import click


@click.group()
def excel():
    """Excel skill - read, write, and process Excel files."""
    pass


@excel.command()
def parse():
    """Parse Excel spreadsheets."""
    click.echo("Excel parsing triggered.")


@excel.command()
def generate():
    """Generate Excel reports."""
    click.echo("Excel report generation triggered.")
