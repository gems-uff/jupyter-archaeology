"""Extract command: extract notebooks"""
import json
import sys
from ..extract import load

def extract_cmd(args, _):
    """extract cmd"""
    if not args.notebooks:
        lines = list(sys.stdin)
        notebooks = json.loads("\n".join(lines))
    else:
        notebooks = args.notebooks
    result = []
    for notebook in notebooks:
        result.append(load(notebook))
    print(json.dumps(result, indent=2))

def create_subparsers(subparsers):
    """create list subcommands"""
    extract_parser = subparsers.add_parser(
        'extract',
        help="Extract data from notebooks as json"
    )
    extract_parser.set_defaults(func=extract_cmd, command=extract_parser)
    extract_parser.add_argument(
        "-n", "--notebooks", default=None, nargs="*",
        help="List of notebooks. If empty, it will read from input"
    )
    