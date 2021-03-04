"""Markdown command: extract markdown cells from notebooks"""
import json
import sys
from ..extract import load
from ..markdown import generate_markdown_cells

def markdown_cmd(args, _):
    """markdown cmd"""
    if not args.notebooks:
        lines = list(sys.stdin)
        notebooks = json.loads("\n".join(lines))
    else:
        notebooks = [load(notebook) for notebook in args.notebooks]

    result = []
    for notebook in notebooks:
        result.extend(generate_markdown_cells(notebook, args.pattern))
    print(''.join(result))


def create_subparsers(subparsers):
    """create markdown subcommands"""
    markdown_parser = subparsers.add_parser(
        'markdown',
        help="Extract markdown from notebooks as plain text"
    )
    markdown_parser.set_defaults(func=markdown_cmd, command=markdown_parser)
    markdown_parser.add_argument(
        "-n", "--notebooks", default=None, nargs="*",
        help="List of notebooks. If empty, it will read json from input"
    )
    markdown_parser.add_argument(
        "-p", "--pattern", default="\n\n###### <juparc:{}> ######\n\n",
        help="Header to indicate te start of a Markdown cells"
    )
