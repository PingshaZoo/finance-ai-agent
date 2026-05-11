import click


@click.group()
def tax():
    """Tax skill - tax calculation and filing automation."""
    pass


@tax.command()
def calculate():
    """Calculate tax obligations."""
    click.echo("Tax calculation triggered.")


@tax.command()
def report():
    """Generate tax reports."""
    click.echo("Tax report generation triggered.")
