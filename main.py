"""
Finance AI Agent - CLI Entry Point
"""

import click

from agents.finance_agent import commands as finance_cmds
from agents.workflow_agent import commands as workflow_cmds
from skills.wechat import commands as wechat_cmds
from skills.tax import commands as tax_cmds
from skills.ecommerce import commands as ecommerce_cmds
from skills.excel import commands as excel_cmds
from skills.ocr import commands as ocr_cmds
from skills.report import commands as report_cmds


@click.group()
def cli():
    """Finance AI Agent - AI-powered financial operations toolkit."""
    pass


# Skills subcommands
cli.add_command(wechat_cmds.wechat)
cli.add_command(tax_cmds.tax)
cli.add_command(ecommerce_cmds.ecommerce)
cli.add_command(excel_cmds.excel)
cli.add_command(ocr_cmds.ocr)
cli.add_command(report_cmds.report)

# Agent subcommands
cli.add_command(finance_cmds.finance)
cli.add_command(workflow_cmds.workflow)

if __name__ == "__main__":
    cli()
