import click


@click.group()
def wechat():
    """WeChat skill - extract and process WeChat data."""
    pass


@wechat.command()
def parse():
    """Parse WeChat chat records."""
    click.echo("WeChat parsing triggered.")


@wechat.command()
def export():
    """Export WeChat data to other formats."""
    click.echo("WeChat export triggered.")
