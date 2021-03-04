"""Select command: select notebooks"""
import json
import sys
import re
from ..extract import load, create_default

def value(original):
    """Convert value to int, float, tuple or str"""
    if isinstance(original, (float, int, tuple)):
        return original
    if isinstance(original, str):
        try:
            return int(original)
        except ValueError:
            try:
                return float(original)
            except ValueError:
                if "." in original:
                    try:
                        return tuple(int(x) for x in original.split('.'))
                    except ValueError:
                        pass
        return original
    return json.dumps(original)


def compare(notebook_arg, attr):
    """Compare argument to notebook value"""
    if attr == "null":
        return notebook_arg is None
    nval = value(notebook_arg)
    if attr.startswith(">"):
        if attr.startswith(">="):
            return nval >= value(attr[2:])
        return nval > value(attr[1:])
    if attr.startswith("<"):
        if attr.startswith("<="):
            return nval <= value(attr[2:])
        return nval < value(attr[1:])
    if attr.startswith("=="):
        return nval == value(attr[2:].lstrip())
    if attr.startswith("!="):
        return nval != value(attr[2:].lstrip())
    return re.match(attr, str(nval)) is not None


def select_cmd(args, _):
    """select cmd"""
    if not args.notebooks:
        lines = list(sys.stdin)
        notebooks = json.loads("\n".join(lines))
    else:
        notebooks = [load(notebook) for notebook in args.notebooks]

    attributes = create_default()

    result = []
    for notebook in notebooks:
        add = True
        for arg in attributes:
            attr = getattr(args, arg, None)
            if attr is None:
                continue
            attr = attr.strip()
            if not compare(notebook[arg], attr):
                add = False
                continue
        if add:
            result.append(notebook)

    if args.count:
        print(len(result))
    else:
        print(json.dumps(result, indent=2))


def create_subparsers(
        subparsers,
        cmd='select',
        helper='Select notebooks that match condition',
        **defaults
):
    """create subcommands"""
    parser = subparsers.add_parser(cmd, help=helper)
    parser.set_defaults(func=select_cmd, command=parser)
    parser.add_argument(
        "-n", "--notebooks", default=None, nargs="*",
        help="List of notebooks. If empty, it will read json from input"
    )
    parser.add_argument(
        "-c", "--count", action="store_true",
        help="Show count instead of notebooks"
    )

    attributes = create_default()
    for attr in attributes:
        default = defaults.get(attr, None)
        parser.add_argument(
            "--" + attr.replace('_', '-'), default=default,
            help="Select " + attr
        )
