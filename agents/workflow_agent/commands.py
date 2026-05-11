import click


@click.group()
def workflow():
    """Workflow agent - orchestrate multi-step financial workflows."""
    pass


@workflow.command()
def run():
    """Execute a workflow."""
    click.echo("Workflow execution triggered.")


@workflow.command()
def list():
    """List available workflows."""
    click.echo("Listing workflows...")
