import click


@click.group()
def report():
    """Report skill - generate financial reports and dashboards."""
    pass


@report.command()
def generate():
    """Generate a financial report."""
    click.echo("Report generation triggered.")


@report.command()
def dashboard():
    """Launch interactive dashboard."""
    click.echo("Dashboard launch triggered.")
