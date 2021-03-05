"""Aggregate Markdown command: aggregate markdown features from multiple markdowns"""
import json
import sys
import re

from collections import defaultdict

from .markdown_features_cmd import extract_features_from_args
from ..markdown import aggregate_markdown

def aggregate_markdown_cmd(args, _):
    """aggregate markdown cmd"""
    if not args.notebooks and not args.markdowns:
        lines = list(sys.stdin)
        blocks = json.loads("\n".join(lines))
    else:
        blocks = extract_features_from_args("", args)

    groups = defaultdict(list)
    for block in blocks:
        match = re.match(args.group, block.get('identifier', ''))
        try:
            gname = match.group(1)
        except (IndexError, ValueError) as err:
            gname = '<default>'
        groups[gname].append(block)

    result = {
        gname: aggregate_markdown(gblocks)
        for gname, gblocks in groups.items()
    }
    print(json.dumps(result, indent=2))


def create_subparsers(subparsers):
    """create aggregate markdown subcommands"""
    markdown_parser = subparsers.add_parser(
        'aggregate-markdown',
        help="Aggregate markdown features as json"
    )
    markdown_parser.set_defaults(func=aggregate_markdown_cmd, command=markdown_parser)
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
    markdown_parser.add_argument(
        "-g", "--group", default=r"(.*):\d*",
        help="Group markdown blocks for aggregations"
    )
