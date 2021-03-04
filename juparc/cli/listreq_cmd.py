"""List Requirements command: list requirements"""
import glob
import json


def listreq_cmd(args, _):
    """listreq function"""
    print(json.dumps({
        'setup.py': glob.glob(args.setup, recursive=True),
        'requirements.txt': glob.glob(args.requirements, recursive=True),
        'Pipfile': glob.glob(args.pipfile, recursive=True),
        'Pipfile.lock': glob.glob(args.pipfile_lock, recursive=True)
    }))


def create_subparsers(subparsers):
    """create listreq subcommands"""
    list_parser = subparsers.add_parser(
        'listreq',
        help="List requirements in the directory"
    )
    list_parser.set_defaults(func=listreq_cmd, command=list_parser)
    list_parser.add_argument("-s", "--setup", default="**/setup.py",
                             help="Glob to find setup.py files")
    list_parser.add_argument("-r", "--requirements", default="**/requirements.txt",
                             help="Glob to find requirements.txt files")
    list_parser.add_argument("-p", "--pipfile", default="**/Pipfile",
                             help="Glob to find Pipfile files")
    list_parser.add_argument("-l", "--pipfile-lock", default="**/Pipfile.lock",
                             help="Glob to find Pipfile.lock files")
