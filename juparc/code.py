"""Code cell analyses"""

import ast
import os
import re
import sys

from collections import Counter, defaultdict, OrderedDict
from contextlib import contextmanager

from .utils import to_unicode

AST_CUSTOM = [
    "import_star", "functions_with_decorators",
    "classes_with_decorators", "classes_with_bases",
    "delname", "delattr", "delitem",
    "assignname", "assignattr", "assignitem",
    "ipython", "ipython_superset",
    "ast_statements", "ast_expressions",
]

AST_SCOPED = [
    "importfrom", "import", "assign", "delete",
    "functiondef", "classdef"
]

AST_MODULES  = [
    "module", "interactive", "expression", "suite"
]

AST_STATEMENTS = [
    "functiondef", "asyncfunctiondef", "classdef", "return",
    "delete", "assign", "augassign", "annassign", "print",
    "for", "asyncfor", "while", "if", "with", "asyncwith",
    "raise", "try", "tryexcept", "tryfinally", "assert",
    "import", "importfrom", "exec", "global", "nonlocal", "expr",
    "pass", "break", "continue"
]

AST_EXPRESSIONS = [
    "boolop", "binop", "unaryop", "lambda", "ifexp",
    "dict", "set", "listcomp", "setcomp", "dictcomp", "generatorexp",
    "await", "yield", "yieldfrom",
    "compare", "call", "num", "str", "formattedvalue", "joinedstr",
    "bytes", "nameconstant", "ellipsis", "constant",
    "attribute", "subscript", "starred", "name", "list", "tuple", "repr",
]

AST_OTHERS = [
    "load", "store", "del", "augload", "augstore", "param",
    "slice", "index",
    "and", "or",
    "add", "sub", "mult", "matmult", "div", "mod", "pow", "lshift",
    "rshift", "bitor", "bitxor", "bitand", "floordiv",
    "invert", "not", "uadd", "usub",
    "eq", "noteq", "lt", "lte", "gt", "gte", "is", "isnot", "in", "notin",
    "comprehension", "excepthandler", "arguments", "arg",
    "keyword", "alias", "withitem", "extslice",
]

MODULE_LOCAL = {
    True: "local",
    False: "external",
    "any": "any",
}

MODULE_TYPES = {
    "any", "import_from", "import", "load_ext"
}

FEATURES = [
    "shadown_ref", "output_ref", "system",
    "set_next_input", "input_ref",
    "magic", "run_line_magic", "run_cell_magic",
    "getoutput", "set_hook"
]

NAME_SCOPES = ["any", "nonlocal", "local", "class", "global", "main"]
NAME_CONTEXTS = [
    "any", "class", "import", "importfrom", "function",
    "param", "del", "load", "store"
]


def default_ast_features():
    counter = OrderedDict()

    for nodetype in AST_CUSTOM:
        counter[nodetype] = 0
    for nodetype in AST_SCOPED:
        counter["class_" + nodetype] = 0
        counter["global_" + nodetype] = 0
        counter["nonlocal_" + nodetype] = 0
        counter["local_" + nodetype] = 0
        counter["total_" + nodetype] = 0
    for nodetype in AST_MODULES:
        counter["ast_" + nodetype] = 0
    for nodetype in AST_STATEMENTS:
        counter["ast_" + nodetype] = 0
    for nodetype in AST_EXPRESSIONS:
        counter["ast_" + nodetype] = 0
    for nodetype in AST_OTHERS:
        counter["ast_" + nodetype] = 0
    #self.counter["------"] = 0
    counter["ast_others"] = ""
    return counter


class PathLocalChecker(object):
    """Check if module is local by looking at the directory"""

    def __init__(self, path):
        path = to_unicode(path)
        self.base = os.path.dirname(path)

    def exists(self, path):
        """Check if path exists"""
        return os.path.exists(path)

    def iterate_files(self):
        """Iterate on repository files"""
        for _root, _sub_folder, files in os.walk(self.base):
            for name in files:
                yield name

    def is_local(self, module):
        """Check if module is local by checking if its package exists"""
        if module.startswith("."):
            return True
        path = self.base
        for part in module.split("."):
            path = os.path.join(path, part)
            if not self.exists(path) and not self.exists(path + u".py"):
                return False
        return True

    def local_possibility(self, module):
        """Rate how likely the module is local. Maximum = 4"""
        if self.is_local(module):
            return 4
        module = module.replace(".", "/")
        if not module:
            return 0

        modes = [
            [module, 3, "Full match"],
        ]
        split = module.split("/", 1)
        if len(split) > 1:
            modes.append((split[-1], 2, "all but first 2"))
        split = module.split("/")
        if len(split) > 2:
            modes.append((split[-1], 1, "module name 1"))

        # Check if a folder matchs the module
        for name in self.iterate_files():
            for modname, value, _result in modes:
                if name.endswith(modname):
                    if len(name) <= len(modname):
                        return value
                    if name[-len(modname) - 1] == '/':
                        return value
        return 0

class CellVisitor(ast.NodeVisitor):
    """Visit cell ast to extract data"""
    # pylint: disable=invalid-name

    def __init__(self, local_checker):
        self.counter = default_ast_features()

        self.statements = set(AST_STATEMENTS)
        self.expressions = set(AST_EXPRESSIONS)

        self.scope = None
        self.globals = set()
        self.nonlocals = set()

        self.ipython_features = []
        self.modules = []
        self.local_checker = local_checker
        self.names = defaultdict(Counter)

    def new_module(self, line, type_, name):
        """Insert new module"""
        local = self.local_checker.is_local(name)
        local_possibility = self.local_checker.local_possibility(name)
        self.modules.append({
            'line': line,
            'import_type': type_,
            'name': name,
            'local': local,
            'local_possibility': local_possibility,
        })

    @contextmanager
    def set_scope(self, scope):
        """Set visiting scope"""
        old_scope = self.scope
        old_globals = self.globals
        old_nonlocals = self.nonlocals
        try:
            self.scope = scope
            self.globals = set()
            self.nonlocals = set()
            yield
        finally:
            self.scope = old_scope
            self.globals = old_globals
            self.nonlocals = old_nonlocals

    def count_simple(self, name):
        """Count var"""
        if name not in self.counter:
            self.counter["ast_others"] += name + " "
        else:
            self.counter[name] += 1

    def count(self, name, varname=None, scope=None):
        """Count scoped var"""
        if varname in self.globals:
            scope = "global"
        if varname in self.nonlocals:
            scope = "nonlocal"
        scope = scope or self.scope
        if scope is not None:
            self.counter["{}_{}".format(scope, name)] += 1
        self.counter["total_{}".format(name)] += 1
        return scope

    def count_name(self, varname, mode, scope=None):
        """Count scoped name"""
        if varname in self.globals:
            scope = "global"
        if varname in self.nonlocals:
            scope = "nonlocal"
        scope = scope or self.scope or "main"
        self.names[(scope, mode)][varname] += 1

    def count_targets(self, targets, name, sub_name):
        """Count target"""
        for target in targets:
            if isinstance(target, ast.Name):
                self.count_simple("{}name".format(sub_name))
                self.count(name, target.id)
            if isinstance(target, ast.Attribute):
                self.count_simple("{}attr".format(sub_name))
                self.count(name)
            if isinstance(target, ast.Subscript):
                self.count_simple("{}item".format(sub_name))
                self.count(name)
            if isinstance(target, (ast.List, ast.Tuple)):
                self.count_targets(target.elts, name, sub_name)

    def visit_children(self, node, *children):
        """Visit children"""
        for child in children:
            child_node = getattr(node, child, None)
            if child_node:
                if isinstance(child_node, (list, tuple)):
                    for child_part in child_node:
                        self.visit(child_part)
                else:
                    self.visit(child_node)
        if not children:
            ast.NodeVisitor.generic_visit(self, node)

    def generic_visit(self, node):
        """Visit undeclared elements"""
        name = type(node).__name__.lower()
        self.count_simple("ast_" + name)
        if name in self.statements:
            self.count_simple("ast_statements")
        if name in self.expressions:
            self.count_simple("ast_expressions")
        self.visit_children(node)

    def visit_FunctionDef(self, node, simple="ast_functiondef"):
        """Visit function definition"""
        self.count_name(node.name, "function")
        self.count_simple("ast_statements")
        self.count_simple(simple)
        self.count("functiondef", node.name)
        with self.set_scope("local"):
            self.visit_children(node, "body")

        if node.decorator_list:
            self.count_simple("functions_with_decorators")

        if sys.version_info < (3, 0):
            self.visit_children(node, "args", "decorator_list")
        else:
            self.visit_children(node, "args", "decorator_list", "returns")

    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition"""
        self.visit_FunctionDef(node, simple="ast_asyncfunctiondef")

    def visit_ClassDef(self, node):
        """Visit class definition"""
        self.count_name(node.name, "class")
        self.count_simple("ast_statements")
        self.count_simple("ast_classdef")
        self.count("classdef", node.name)
        with self.set_scope("class"):
            self.visit_children(node, "body")

        if node.decorator_list:
            self.count_simple("classes_with_decorators")

        if any(
                base for base in node.bases
                if not isinstance(base, ast.Name)
                or not base.id == "object"
        ):
            self.count_simple("classes_with_bases")

        if sys.version_info < (3, 0):
            self.visit_children(node, "bases", "decorator_list")
        elif sys.version_info < (3, 5):
            self.visit_children(node, "bases", "keywords", "starargs", "kwargs", "decorator_list")
        else:
            self.visit_children(node, "bases", "keywords", "decorator_list")

    def visit_Delete(self, node):
        """Visit delete"""
        self.count_targets(node.targets, "delete", "del")
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Visit assign"""
        self.count_targets(node.targets, "assign", "assign")
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        """Visit augmented assign"""
        self.count_targets([node.target], "assign", "assign")
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        """Visit annotated assign"""
        self.count_targets([node.target], "assign", "assign")
        self.generic_visit(node)

    def visit_For(self, node):
        """Visit for loop"""
        self.count_targets([node.target], "assign", "assign")
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        """Visit async for loop"""
        self.visit_For(node)

    def visit_Import(self, node):
        """Get module from imports"""
        for import_ in node.names:
            self.new_module(node.lineno, "import", import_.name)
        for alias in node.names:
            name = alias.asname or alias.name
            self.count_name(name, "import")
            self.count("import", name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Get module from imports"""
        self.new_module(
            node.lineno, "import_from",
            ("." * (node.level or 0)) + (node.module or "")
        )
        for alias in node.names:
            name = alias.asname or alias.name
            self.count_name(name, "importfrom")
            if name == "*":
                self.count_simple("import_star")
            self.count("importfrom", name)
        self.generic_visit(node)

    def visit_Global(self, node):
        """Visit global"""
        self.globals.update(node.names)
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        """Visit nonlocal"""
        self.nonlocals.update(node.names)
        self.generic_visit(node)

    def visit_Call(self, node):
        """get_ipython().<method> calls"""

        func = node.func
        if not isinstance(func, ast.Attribute):
            return self.generic_visit(node)
        value = func.value
        if not isinstance(value, ast.Call):
            return self.generic_visit(node)
        value_func = value.func
        if not isinstance(value_func, ast.Name):
            return self.generic_visit(node)
        if value_func.id != "get_ipython":
            return self.generic_visit(node)
        args = node.args
        if not args:
            return self.generic_visit(node)
        if not isinstance(args[0], ast.Str):
            return self.generic_visit(node)
        if not args[0].s:
            return self.generic_visit(node)

        self.count_simple("ipython_superset")

        type_ = func.attr
        split = args[0].s.split()
        name, = split[0:1] or ['']

        self.ipython_features.append({
            'line': node.lineno,
            'column': node.col_offset,
            'feature_name': type_,
            'feature_value': name
        })

        if name == "load_ext":
            try:
                module = split[1] if len(split) > 1 else args[1].s
            except IndexError:
                return
            self.new_module(node.lineno, "load_ext", module)

    def visit_Subscript(self, node):
        """Collect In, Out, _oh, _ih"""
        self.generic_visit(node)
        if not isinstance(node.value, ast.Name):
            return
        if node.value.id in {"In", "_ih"}:
            type_ = "input_ref"
        elif node.value.id in {"Out", "_oh"}:
            type_ = "output_ref"
        else:
            return
        self.count_simple("ipython")
        self.ipython_features.append({
            'line': node.lineno,
            'column': node.col_offset,
            'feature_name': type_,
            'feature_value': node.value.id + "[]"
        })

    def visit_Name(self, node):
        """Collect _, __, ___, _i, _ii, _iii, _0, _1, _i0, _i1, ..., _sh"""
        self.count_name(node.id, type(node.ctx).__name__.lower())
        self.generic_visit(node)
        type_ = None
        underscore_num = re.findall(r"(^_(i)?\d*$)", node.id)
        many_underscores = re.findall(r"(^_{1,3}$)", node.id)
        many_is = re.findall(r"(^_i{1,3}$)", node.id)
        if underscore_num:
            type_ = "input_ref" if underscore_num[0][1] else "output_ref"
        elif many_underscores:
            type_ = "output_ref"
        elif many_is:
            type_ = "input_ref"
        elif node.id == "_sh":
            type_ = "shadown_ref"

        if type_ is not None:
            self.count_simple("ipython")
            self.ipython_features.append({
                'line': node.lineno,
                'column': node.col_offset,
                'feature_name': type_,
                'feature_value': node.id
            })


def extract_code_features(text, checker):
    """Use cell visitor to extract features from cell text"""
    visitor = CellVisitor(checker)
    try:
        parsed = ast.parse(text)
    except ValueError:
        raise SyntaxError("Invalid escape")
    visitor.visit(parsed)
    visitor.counter["ast_others"] = visitor.counter["ast_others"].strip()
    return {
        'ast': visitor.counter,
        'modules': visitor.modules,
        'ipython': visitor.ipython_features,
        'names': visitor.names
    }


def supressed_extract_code_features(source, checker):
    """Extract code features but suppress syntax errors"""
    try:
        result = extract_code_features(source, checker)
        names = defaultdict(lambda: defaultdict(Counter))
        for (scope, context), values in result['names'].items():
            names[scope][context] = values
        result['names'] = names
        return result
    except SyntaxError:
        return {
            'ast': '<SyntaxError>',
            'modules': '<SyntaxError>',
            'ipython': '<SyntaxError>',
            'names': '<SyntaxError>',
        }


def aggregate_ast(notebook):
    """Aggregate ASTs from notebook"""
    ast_columns = default_ast_features()
    del ast_columns['ast_others']

    agg_ast = {col: 0 for col in ast_columns}
    agg_ast["cell_count"] = 0
    ast_others = []

    for cell in notebook.get('cells', []) or []:
        if cell.get("cell_type", "unknown") != "code":
            continue
        agg_ast["cell_count"] += 1
        ast_obj = cell.get('ast', {})
        if ast_obj['ast_others']:
            ast_others.append(ast_obj['ast_others'])
        for column in ast_columns:
            agg_ast[column] += int(ast_obj.get(column))

    agg_ast["ast_others"] = ",".join(ast_others)
    return agg_ast


def aggregate_modules(notebook):
    """Aggregate Modules from notebook"""
    temp_agg = {
        (local + "_" + type_): OrderedDict()
        for _, local in MODULE_LOCAL.items()
        for type_ in MODULE_TYPES
    }
    temp_agg["index"] = OrderedDict()
    others = []
    def add_key(key, module):
        if key in temp_agg:
            temp_agg[key][module["name"]] = 1
        else:
            others.append("{}:{}".format(key, module["name"]))

    for cell in notebook.get('cells', []) or []:
        for module in cell.get("modules", []) or []:
            temp_agg["index"][str(cell["index"])] = 1
            local = module["local"] or module["local_possibility"] > 0

            key = MODULE_LOCAL[local] + "_" + module["import_type"]
            add_key(key, module)

            key = MODULE_LOCAL[local] + "_any"
            add_key(key, module)

            key = "any_" + module["import_type"]
            add_key(key, module)

            key = "any_any"
            add_key(key, module)

    agg = {}
    for attr, elements in temp_agg.items():
        agg[attr] = ",".join(elements)
        agg[attr + "_count"] = len(elements)

    agg["others"] = ",".join(others)
    return agg


def aggregate_ipython(notebook):
    """Aggregate IPython features from notebook"""
    temp_agg = {
        col: OrderedDict()
        for col in FEATURES
    }
    temp_agg['any'] = OrderedDict()
    temp_agg['index'] = OrderedDict()
    others = []
    def add_feature(key, feature):
        if key in temp_agg:
            temp_agg[key][feature["feature_value"]] = 1
        else:
            others.append("{}:{}".format(key, feature["feature_value"]))

    for cell in notebook.get('cells', []) or []:
        for feature in cell.get("ipython", []) or []:
            temp_agg["index"][str(cell["index"])] = 1
            key = feature["feature_name"]
            add_feature(key, feature)

            key = "any"
            add_feature(key, feature)

    agg = {}
    for attr, elements in temp_agg.items():
        agg[attr] = ",".join(elements)
        agg[attr + "_count"] = len(elements)

    agg["others"] = ",".join(others)
    return agg


def aggregate_names(notebook):
    """Aggregate Names from notebook"""
    temp_agg = {
        (scope + "_" + context): Counter()
        for scope in NAME_SCOPES
        for context in NAME_CONTEXTS
    }
    index = OrderedDict()
    others = []
    def add_key(key, counts):
        for name, count in counts.items():
            if key in temp_agg:
                temp_agg[key][name] += count
            else:
                others.append("{}:{}({})".format(key, name, count))

    for cell in notebook.get('cells', []) or []:
        for scope, contexts in (cell.get("names", {}) or {}).items():
            for context, counts in contexts.items():
                index[str(cell["index"])] = 1
                key = scope + "_" + context
                add_key(key, counts)

                key = scope + "_any"
                add_key(key, counts)

                key = "any_" + context
                add_key(key, counts)

                key = "any_any"
                add_key(key, counts)

    agg = {}
    agg["index"] = ",".join(index)
    agg["index_count"] = len(index)
    for attr, elements in temp_agg.items():
        mc = elements.most_common()
        agg[attr] = ",".join(str(name) for name, _ in mc)
        agg[attr + "_counts"] = ",".join(str(count) for _, count in mc)

    agg["others"] = ",".join(others)
    return agg
