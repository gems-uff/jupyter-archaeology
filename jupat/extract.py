"""Extract operation: extract notebooks"""
import os
import traceback
import hashlib

import nbformat as nbf
from IPython.core.interactiveshell import InteractiveShell

def create_default(name=None):
    return {
        "name": name,
        "nbformat": 0,
        "kernel": "no-kernel",
        "language": "unknown",
        "language_version": "unknown",
        "max_execution_count": 0,
        "total_cells": 0,
        "code_cells": 0,
        "code_cells_with_output": 0,
        "markdown_cells": 0,
        "raw_cells": 0,
        "unknown_cell_formats": 0,
        "empty_cells": 0,
        "size": None,
        "sha1_file": None,
        "cells": [],
        "status": "ok",
        "exception": None,
    }

def create_cell(index=None):
    return {
        "index": index,
        "cell_type": "<unknown>",
        "execution_count": None,
        "lines": None,
        "output_formats": [],
        "source": None,
        "raw_source": None,
        "python": None,
        "status": [],
        "exception": None,
    }

def subfilter(filterlist, prefix):
    if filterlist is None:
        return filterlist
    return [
        x[len(prefix) + 1:] for x in filterlist
        if x.startswith(prefix + ".")
    ]


def filterout(key, include, exclude):
    if include and key not in include:
        return True
    if exclude and key in exclude:
        return True
    return False


def prepare_setvar(container, include, exclude):
    def setvar(key, value):
        if filterout(key, include, exclude):
            return
        pvalue = value() if callable(value) else value
        container[key] = pvalue
    return setvar


def get_size(start_path = '.'):
    if os.path.isfile(start_path):
        return os.path.getsize(start_path)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def sha1_hash(path):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()
 

def set_kernel_language(metadata, setvar):
    """Extract kernel and language from notebook metadata"""
    setvar("kernel", metadata.get("kernelspec", {}).get("name", "no-kernel"))
    language_info = metadata.get("language_info", {})
    language = language_info.get("name", "unknown")
    language_version = language_info.get("version", "unknown")
    setvar("language", language)
    setvar("language_version", language_version)
    return language, language_version


def cell_output_formats(cell):
    """Generates output formats from code cells"""
    if cell.get("cell_type") != "code":
        return
    for output in cell.get("outputs", []):
        if output.get("output_type") in {"display_data", "execute_result"}:
            for data_type in output.get("data", []):
                yield "{}/{}".format(output.get("output_type"), data_type)
        elif output.get("output_type") == "error":
            yield "error"
        elif output.get("output_type") == "stream":
            yield "stream/{}".format(output.get("name", "other"))


def load_cells(lang_tuple, nbrow, cells, include=None, exclude=None, vprint=lambda x: None):
    language, language_version = lang_tuple
    status = "ok"
    shell = InteractiveShell.instance()
    is_python = language == "python"
    is_unknown_version = language_version == "unknown"
    cells_info = []
    exec_count = -1

    for index, cell in enumerate(cells):
        vprint("Loading cell {}".format(index))
        
        cell_exec_count = cell.get("execution_count") or -1
        if isinstance(cell_exec_count, str) and cell_exec_count.isdigit():
            cell_exec_count = int(cell_exec_count)
        if isinstance(cell_exec_count, int):
            exec_count = max(exec_count, cell_exec_count)
        output_formats = list(cell_output_formats(cell))

        cell_status = set()
        if is_unknown_version:
            cell_status.add("unknown-version")

        try:
            source = raw_source = cell["source"] = cell["source"] or ""
            if is_python and cell.get("cell_type") == "code":
                try:
                    source = shell.input_transformer_manager.transform_cell(raw_source)
                except (IndentationError, SyntaxError) as err:
                    vprint("Error on cell transformation: {}".format(traceback.format_exc()))
                    source = ""
                    status = "load-syntax-error"
                    cell_status.add("syntax-error")
                if "\0" in source:
                    vprint("Found null byte in source. Replacing it by \\n")
                    source = source.replace("\0", "\n")

            cellrow = create_cell(index)
            setcvar = prepare_setvar(cellrow, include, exclude)
            setcvar("cell_type", cell.get("cell_type", "<unknown>"))
            setcvar("execution_count", cell.get("execution_count"))
            setcvar("lines", cell["source"].count("\n") + 1)
            setcvar("output_formats", output_formats)
            setcvar("source", source)
            setcvar("raw_source", raw_source)
            setcvar("python", is_python)
            setcvar("status", list(cell_status))
            cells_info.append({k: v for k, v in cellrow.items() if not filterout(k, include, exclude)})

            nbrow["total_cells"] += 1
            if cell.get("cell_type") == "code":
                nbrow["code_cells"] += 1
                if output_formats:
                    nbrow["code_cells_with_output"] += 1
            elif cell.get("cell_type") == "markdown":
                nbrow["markdown_cells"] += 1
            elif cell.get("cell_type") == "raw":
                nbrow["raw_cells"] += 1
            else:
                nbrow["unknown_cell_formats"] += 1
            if not cell["source"].strip():
                nbrow["empty_cells"] += 1
        except KeyError as err:
            vprint("Error on cell extraction: {}".format(traceback.format_exc()))
            status = "load-format-error"
    if nbrow["total_cells"] == 0:
        status = "load-format-error"
    
    nbrow["max_execution_count"] = exec_count
    nbrow["status"] = status
    return cells_info


def load(name, basepath="", nbrow=None, include=None, exclude=None, vprint=lambda x: None):
    """Extract notebook information and cells from notebook"""
    nbrow = nbrow or create_default(name)
    setvar = prepare_setvar(nbrow, include, exclude)
    try:
        npath = os.path.join(basepath, name)
        with open(npath) as ofile:
            notebook = nbf.read(ofile, nbf.NO_CONVERT)
        setvar("size", lambda: get_size(npath))
        setvar("sha1_file", lambda: sha1_hash(npath))
        setvar("nbformat", "{0[nbformat]}".format(notebook))
        if "nbformat_minor" in notebook:
            setvar("nbformat", nbrow["nbformat"] + ".{0[nbformat_minor]}".format(notebook))
        notebook = nbf.convert(notebook, 4)
        metadata = notebook["metadata"]
    except OSError:
        vprint("Failed to open notebook {}".format(nbrow["exception"]))
        setvar("status", "load-error")
        setvar("exception", traceback.format_exc())
        return nbrow
    except Exception:  # pylint: disable=broad-except
        vprint("Failed to load notebook {}".format(nbrow["exception"]))
        setvar("status", "load-format-error")
        setvar("exception", traceback.format_exc())
        return nbrow

    lang_tuple = set_kernel_language(metadata, setvar)
    setvar("cells", load_cells(
        lang_tuple, nbrow, notebook["cells"],
        include=subfilter(include, "cells"), exclude=subfilter(exclude, "cells"),
        vprint=vprint
    ))
    return {k: v for k, v in nbrow.items() if not filterout(k, include, exclude)}
