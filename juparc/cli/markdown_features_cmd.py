"""Markdown Features command: extract features from markdown"""
import json
import sys
from ..extract import load
from ..markdown import generate_markdown_cells, split_markdown, extract_features

def extract_features_from_args(markdown, args):
    """extract markdown features according to args"""
    if args.notebooks:
        markdown_l = []
        for notebook in args.notebooks:
            markdown_l.extend(generate_markdown_cells(
                load(notebook), args.pattern
            ))
        markdown += ''.join(markdown_l)

    if args.markdowns:
        for mark in args.markdowns:
            with open(mark, 'r') as fil:
                markdown += (
                    args.pattern.format(mark)
                    + fil.read()
                )

    blocks = split_markdown(markdown, args.pattern)
    for block in blocks:
        block['features'] = extract_features(block['code'])
    return blocks

def markdown_features_cmd(args, _):
    """markdown features cmd"""
    markdown = ""
    if not args.notebooks and not args.markdowns:
        lines = list(sys.stdin)
        markdown = "".join(lines)

    blocks = extract_features_from_args(markdown, args)
    print(json.dumps(blocks, indent=2))


def create_subparsers(subparsers):
    """create markdown subcommands"""
    markdown_parser = subparsers.add_parser(
        'markdown-features',
        help="Extract markdown features as json"
    )
    markdown_parser.set_defaults(func=markdown_features_cmd, command=markdown_parser)
    markdown_parser.add_argument(
        "-n", "--notebooks", default=None, nargs="*",
        help="List of notebooks. If empty, it will read plain markdown from input"
    )
    markdown_parser.add_argument(
        "-m", "--markdowns", default=None, nargs="*",
        help="List of markdown files"
    )
    markdown_parser.add_argument(
        "-p", "--pattern", default="\n\n###### <juparc:{}> ######\n\n",
        help="Header to indicate te start of a Markdown cells"
    )
