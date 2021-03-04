"""List command: list notebooks"""
import glob
import json


def list_cmd(args, _):
    """list cmd"""
    print(json.dumps(sorted(glob.glob(args.notebooks, recursive=True))))


def create_subparsers(subparsers):
    """create list subcommands"""
    list_parser = subparsers.add_parser(
        'list',
        help="List notebooks in the directory"
    )
    list_parser.set_defaults(func=list_cmd, command=list_parser)
    list_parser.add_argument("-n", "--notebooks", default="**/*.ipynb",
                             help="Glob to find notebooks")
