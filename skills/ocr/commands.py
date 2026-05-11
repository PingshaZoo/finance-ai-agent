import click


@click.group()
def ocr():
    """OCR skill - extract text from images and documents."""
    pass


@ocr.command()
def recognize():
    """Recognize text from images."""
    click.echo("OCR recognition triggered.")


@ocr.command()
def batch():
    """Batch OCR processing."""
    click.echo("Batch OCR processing triggered.")
