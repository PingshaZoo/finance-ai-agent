import click


@click.group()
def ecommerce():
    """E-commerce skill - manage e-commerce financial data."""
    pass


@ecommerce.command()
def orders():
    """Process e-commerce orders."""
    click.echo("E-commerce orders processing triggered.")


@ecommerce.command()
def reconcile():
    """Reconcile e-commerce transactions."""
    click.echo("E-commerce reconciliation triggered.")
