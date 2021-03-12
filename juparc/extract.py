"""Extract operation: extract notebooks"""
import hashlib
import os
import re
import traceback

from collections import Counter

import numba
import numpy
import nbformat as nbf
from IPython.core.interactiveshell import InteractiveShell

COUNT_WORDS = ['homework', 'assignment', 'course', 'exercise', 'lesson']


def legacy_output_format(outf):
    """Convert juparc format to format we used in MSR paper"""
    if outf.startswith("display_data/"):
        return outf[13:]
    if outf.startswith("execute_result/"):
        return outf[15:]
    return outf


def create_default(name=None):
    """Create Notebook Dict Object"""
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
        "sha1_source": "",
        "word_counter": {},

        "unambiguous": None,
        "actual_empty_cells": -1,
        "non_executed_cells": 0,
        "empty_cells_middle": 0,
        "empty_cells_end": 0,
        "numeric_counts_total": 0,
        "numeric_set_total": 0,
        "processing_cells": 0,
        "unordered": None,
        "execution_skips_total": 0,
        "execution_skips_size": 0,
        "execution_skips_middle_total": 0,
        "execution_skips_middle_size": 0,

    }


def create_cell(index=None):
    """Create Cell Dict Object"""
    return {
        "index": index,
        "cell_type": "<unknown>",
        "execution_count": None,
        "lines": None,
        "output_formats": [],
        "legacy_output_formats": "",
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


def int_or_none(value):
    """Returns int if the value can be converted to int or None, otherwise"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def count_middle_empty(arr):
    while arr and arr[-1] == 'empty':
        arr = arr[:-1]
    return arr.count('empty')


def select_numbers(arr):
    for count in arr:
        try:
            yield int(count)
        except (TypeError, ValueError):
            pass


@numba.jit("i8(i8[:])")
def count_skips(arr):
    last = 0
    current = -10000
    skips = 0
    for element in arr:
        current = element
        if current - last > 1:
            skips += 1
        last = current
    return skips


@numba.jit("i8(i8[:])")
def count_skips_sizes(arr):
    last = 0
    current = -10000
    skips = 0
    for element in arr:
        current = element
        if current != last:
            skips += current - last - 1
        last = current
    return skips


@numba.jit("i8(i8[:])")
def count_skips_middle(arr):
    last = -10000
    current = -10000
    skips = 0
    for element in arr:
        current = element
        if last != -10000 and current - last > 1:
            skips += 1
        last = current
    return skips


@numba.jit("i8(i8[:])")
def count_skips_sizes_middle(arr):
    last = -10000
    current = -10000
    skips = 0
    for element in arr:
        current = element
        if last != -10000 and current != last:
            skips += current - last - 1
        last = current
    return skips


def load_cells(lang_tuple, nbrow, cells, include=None, exclude=None, vprint=lambda x: None, count_words=None):
    count_words = count_words or COUNT_WORDS
    language, language_version = lang_tuple
    status = "ok"
    shell = InteractiveShell.instance()
    is_python = language == "python"
    is_unknown_version = language_version == "unknown"
    cells_info = []
    exec_count = -1

    concat_source = []
    word_counter = Counter()

    unfiltered = []
    execution_counts = []

    for index, cell in enumerate(cells):
        vprint("Loading cell {}".format(index))

        cell_exec_count = cell.get("execution_count")
        cell_exec_count_int = int_or_none(cell_exec_count)
        if cell_exec_count_int is not None:
            exec_count = max(exec_count, cell_exec_count_int)

        output_formats = list(cell_output_formats(cell))

        cell_status = set()
        if is_unknown_version:
            cell_status.add("unknown-version")

        try:
            source = raw_source = cell["source"] = cell.get("source", "") or ""
            concat_source.append(source)
            lower = cell.source.lower()
            for word in count_words:
                if word in lower:
                    word_counter[word] += 1
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
            setcvar("execution_count", cell_exec_count)
            setcvar("lines", cell["source"].count("\n") + 1)
            setcvar("output_formats", output_formats)
            cellrow["legacy_output_formats"] = ";".join(
                set(map(legacy_output_format, cellrow["output_formats"]))
            )
            concat_source.append(cellrow["legacy_output_formats"])
            setcvar("source", source)
            setcvar("raw_source", raw_source)
            setcvar("python", is_python)
            setcvar("status", list(cell_status))
            cells_info.append({
                k: v for k, v in cellrow.items()
                if not filterout(k, include, exclude)
            })

            nbrow["total_cells"] += 1
            if cell.get("cell_type") == "code":
                if re.sub(r'[\n\r]+', ' ', source).strip() == '':
                    execution_counts.append("empty")
                else:
                    execution_counts.append(cell_exec_count_int)
                if cell_exec_count_int is not None:
                    unfiltered.append(cell_exec_count_int)
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

    lower = nbrow["name"].lower()
    for word in count_words:
        if word in lower:
            word_counter[word] = -word_counter[word] - 1

    concat_str = "<#<cell>#>\n".join(concat_source)
    nbrow["sha1_source"] = hashlib.sha1(concat_str.encode('utf-8')).hexdigest()
    nbrow["word_counter"] = word_counter

    if nbrow["total_cells"] == 0:
        status = "load-format-error"

    nbrow["max_execution_count"] = exec_count
    nbrow["status"] = status


    numbers = set(unfiltered)
    nbrow["unambiguous"] = unfiltered and len(numbers) == len(unfiltered)

    numeric_counts = list(select_numbers(execution_counts))
    numeric_sorted = sorted(numeric_counts)
    numpy_sorted = numpy.array(numeric_sorted, dtype=int)

    nbrow["actual_empty_cells"] = execution_counts.count('empty')
    nbrow["non_executed_cells"] = execution_counts.count(None)
    nbrow["empty_cells_middle"] = count_middle_empty(execution_counts)
    nbrow["empty_cells_end"] = nbrow["actual_empty_cells"] - nbrow["empty_cells_middle"]
    nbrow["numeric_counts_total"] = len(numeric_counts)
    nbrow["numeric_set_total"] = len(set(numeric_counts))
    nbrow["processing_cells"] = execution_counts.count('*')
    nbrow["unordered"] = numeric_counts != numeric_sorted
    nbrow["execution_skips_total"] = count_skips(numpy_sorted)
    nbrow["execution_skips_size"] = count_skips_sizes(numpy_sorted)
    nbrow["execution_skips_middle_total"] = count_skips_middle(numpy_sorted)
    nbrow["execution_skips_middle_size"] = count_skips_sizes_middle(numpy_sorted)

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
