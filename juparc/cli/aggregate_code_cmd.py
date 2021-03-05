"""Aggregate Code command: aggregate code features from python cells"""
import json
import sys

from .code_features_cmd import enrich_notebooks
from ..extract import load
from ..code import aggregate_ast, aggregate_modules
from ..code import aggregate_ipython, aggregate_names


def aggregate_code_cmd(args, _):
    """aggregate code features cmd"""
    if not args.notebooks:
        lines = list(sys.stdin)
        notebooks = json.loads("\n".join(lines))
    else:
        notebooks = [load(notebook) for notebook in args.notebooks]
        args.ignore_others = None
        args.keep = None
        enrich_notebooks(notebooks, args)

    result = []
    for notebook in notebooks:
        nresult = {
            'name': notebook['name']
        }
        result.append(nresult)
        if not args.ignore_ast:
            nresult['ast'] = aggregate_ast(notebook)
        if not args.ignore_modules:
            nresult['modules'] = aggregate_modules(notebook)
        if not args.ignore_names:
            nresult['names'] = aggregate_names(notebook)
        if not args.ignore_ipython:
            nresult['ipython'] = aggregate_ipython(notebook)
    print(json.dumps(result, indent=2))


def create_subparsers(subparsers):
    """create subcommands"""
    parser = subparsers.add_parser(
        'aggregate-code',
        help="Aggregate code features as json"
    )
    parser.set_defaults(func=aggregate_code_cmd, command=parser)
    parser.add_argument(
        "-n", "--notebooks", default=None, nargs="*",
        help="List of notebooks. If empty, it will read json from input"
    )
    parser.add_argument(
        "-a", "--ignore-ast", action="store_true",
        help="Ignore AST"
    )
    parser.add_argument(
        "-m", "--ignore-modules", action="store_true",
        help="Ignore Modules"
    )
    parser.add_argument(
        "-e", "--ignore-names", action="store_true",
        help="Ignore Names"
    )
    parser.add_argument(
        "-i", "--ignore-ipython", action="store_true",
        help="Ignore IPython"
    )
