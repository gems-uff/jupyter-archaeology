import argparse
from . import list_cmd
from . import listreq_cmd
from . import extract_cmd
from . import markdown_cmd
from . import markdown_features_cmd
from . import python_cmd
from . import select_cmd
from . import code_features_cmd

def main():
    """Julynter Main CLI"""
    parser = argparse.ArgumentParser(description='Jupyter Analysis Tools')
    subparsers = parser.add_subparsers()
    list_cmd.create_subparsers(subparsers)
    listreq_cmd.create_subparsers(subparsers)
    extract_cmd.create_subparsers(subparsers)
    markdown_cmd.create_subparsers(subparsers)
    markdown_features_cmd.create_subparsers(subparsers)
    code_features_cmd.create_subparsers(subparsers)
    python_cmd.create_subparsers(subparsers)
    select_cmd.create_subparsers(subparsers)

    args, rest = parser.parse_known_args()
    if not getattr(args, 'func', None):
        parser.print_help()
    else:
        args.func(args, rest)
