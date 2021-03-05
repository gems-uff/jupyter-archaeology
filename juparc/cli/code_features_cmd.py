"""Code features command: extract code features from python cells"""
import json
import sys

from ..extract import load, create_cell
from ..code import supressed_extract_code_features, PathLocalChecker


def enrich_notebooks(notebooks, args):
    """enrich notebooks with features"""
    keep = set()
    if args.keep:
        keep = set(args.keep)
    for notebook in notebooks:
        checker = PathLocalChecker(notebook.get('name', '.'))
        for cell in notebook.get('cells', []):
            if cell.get('cell_type', None) == 'code':
                result = supressed_extract_code_features(
                    cell.get("source", ""),
                    checker
                )
                if not args.ignore_ast:
                    keep.add('ast')
                    cell['ast'] = result['ast']
                if not args.ignore_modules:
                    keep.add('modules')
                    cell['modules'] = result['modules']
                if not args.ignore_names:
                    keep.add('names')
                    cell['names'] = result['names']
                if not args.ignore_ipython:
                    keep.add('ipython')
                    cell['ipython'] = result['ipython']
            for attr in getattr(args, 'ignore_others', []) or []:
                if attr in cell:
                    del cell[attr]
            if args.keep:
                for attr in create_cell():
                    if attr not in keep and attr in cell:
                        del cell[attr]

def code_features_cmd(args, _):
    """code features cmd"""
    if not args.notebooks:
        lines = list(sys.stdin)
        notebooks = json.loads("\n".join(lines))
    else:
        notebooks = [load(notebook) for notebook in args.notebooks]

    enrich_notebooks(notebooks, args)
    print(json.dumps(notebooks, indent=2))


def create_subparsers(subparsers):
    """create subcommands"""
    parser = subparsers.add_parser(
        'code-features',
        help="Enrich notebook cells with code features"
    )
    parser.set_defaults(func=code_features_cmd, command=parser)
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
    parser.add_argument(
        "-o", "--ignore-others", default=None, nargs="*",
        help="Ignore other cell attributes"
    )
    parser.add_argument(
        "-k", "--keep", default=None, nargs="*",
        help="Keep cell attributes"
    )
