"""Python command: select python notebooks"""
from .select_cmd import create_subparsers as ocs

def create_subparsers(subparsers):
    """create subcommands"""
    ocs(subparsers, 'python', 'Equivalent to {juparc select --language python}', language='python')
