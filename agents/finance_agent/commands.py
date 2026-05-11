import click


@click.group()
def finance():
    """Finance agent - automated financial data processing."""
    pass


@finance.command()
def analyze():
    """Analyze financial data."""
    click.echo("Finance analysis triggered.")


@finance.command()
def monitor():
    """Monitor financial transactions."""
    click.echo("Finance monitoring triggered.")
