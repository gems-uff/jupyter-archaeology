# JupArc - Jupyter analysis tools for repository Archaeology

This repository contains a library/CLI for analyzing Jupyter Notebooks and the scripts we used in the following Jupyter Archaeology studies:

* [PIMENTEL, J. F.; MURTA, L.; BRAGANHOLO, V.; FREIRE, J.; A large-scale study about quality and reproducibility of jupyter notebooks. In: International Conference on Mining Software Repositories (MSR), 2019, Montreal, Canada.](http://www2.ic.uff.br/~leomurta/papers/pimentel2019a.pdf)
* PIMENTEL, J. F.; MURTA, L.; BRAGANHOLO, V.; FREIRE, J.; Understanding and Improving the Quality and Reproducibility of Jupyter Notebooks. Empirical Software Engineering, 2021 (in press)


## Repository and README structure

The repository is structured as follows:

* [juparc](juparc) contains a standalone library/CLI we extracted from the original analysis scripts to allow the usage in other projects.
* [archaeology](archaeology) contains the scripts and libraries required to reproduce or expand the experiments.
* [analyses](analyses) contains the notebooks we used in the second study to analyze the collected data. For analyses of the first study, please check the [old zenodo repository](https://doi.org/10.5281/zenodo.2538876).

The rest of this README focuses on the standalone library/CLI we developed for analyzing notebooks. For reproducibility instructions related to the second study, please check the [new zenodo repository](https://doi.org/10.5281/zenodo.2538876).

In addition to the tool available in this repository, we used [Julynter](https://github.com/dew-uff/julynter) to execute notebooks in the second reproducibility study using different environments and strategies.

## JupArc Tool

JupArc can be used both as a standalone CLI tool that extracts data from notebooks and writes the results (mostly in JSON) to the standard output or as a Python library. It has operations for listing files in a repository, extracting cells with source code and output types, counting each type of cells, parsing Markdown and Python cells, and aggregating the results.

Most of its operations can be performed through piping of JupArc commands. Hence, we will specify the expected standard input for each command that may use it.

### Installation

To install JupArc, just run:

```
$ pip install juparc
```

If you prefer to install the development version, clone the repository and install it using the `-e` option

```
$ git clone https://github.com/gems-uff/jupyter-archaeology
$ pip install -e jupyter-archaeology
```

### Listing notebook files

Use the command `juparc list` to list notebooks:

```
$ juparc list
```

<details>
  <summary>Output: JSON list of files</summary>

  ```json
  ["analyses/A0.Skip.Notebook.ipynb", "analyses/A1.Corpus.Introduction.Data.Collection.ipynb", "analyses/A2.RQ1.RQ2.Non.duplicated.ipynb", "analyses/A3.RQ3.RQ4.Valid.Python.Notebooks.ipynb", "analyses/A4.RQ5.RQ6.Executed.Notebooks.ipynb", "analyses/A5.RQ6.Unambiguous.Notebooks.ipynb", "analyses/A6.RQ7.Unambiguous.Python.Notebooks.ipynb", "analyses/A7.Docker.Install.ipynb", "analyses/A8.Mining.Rules.ipynb", "analyses/A9.Sample.Analyses.ipynb", "analyses/E1.Repositories.ipynb", "analyses/E2.Notebooks.ipynb", "analyses/E3.Markdown.ipynb", "analyses/E4.Modules.ipynb", "analyses/E5.AST.ipynb", "analyses/E6.IPython.Features.ipynb", "analyses/E7.Names.ipynb", "analyses/E8.Execution.ipynb", "analyses/Index.ipynb", "analyses/Z0.Sample.ipynb", "analyses/Z1.To.Paper.ipynb"]
  ```
</details>


### Listing requirement files

Use the command `juparc listreq` to list requirement files:

```
$ juparc listreq
```

<details>
  <summary>Output: JSON list of files</summary>

  ```json
  {"setup.py": ["setup.py"], "requirements.txt": ["archaeology/requirements.txt", "analyses/requirements.txt"], "Pipfile": [], "Pipfile.lock": []}
  ```
</details>

Output: 

### Initial processing of notebooks

The command `juparc extract` performs an initial processing of the notebooks. It extracts the programming language, number of code cells and markdown cells, maximum execution counter number, and cells.

For cells, it extracts the source code, the post-processed source code (i.e., the source after transforming the IPython code into Python), the output formats, execution counts, and cell types.

For specifying the notebooks, it either accepts a list of notebooks in the standard input (pipe from `$ juparc list`) or accepts the `-n` argument with the notebooks.

Standard input: List of notebooks (output of `$ juparc list`)

```
$ juparc extract -n analyses/A1.Corpus.Introduction.Data.Collection.ipynb
```

<details>
  <summary>Output: JSON list of JupArc notebook objects</summary>

  ```json
  [
    {
      "name": "analyses/A1.Corpus.Introduction.Data.Collection.ipynb",
      "nbformat": "4.4",
      "kernel": "python3",
      "language": "python",
      "language_version": "3.7.3",
      "max_execution_count": 41,
      "total_cells": 54,
      "code_cells": 41,
      "code_cells_with_output": 37,
      "markdown_cells": 13,
      "raw_cells": 0,
      "unknown_cell_formats": 0,
      "empty_cells": 0,
      "size": 511396,
      "sha1_file": "25145f1a764169ed5e29c760322432edf1317559",
      "cells": [
        {
          "index": 0,
          "cell_type": "markdown",
          "execution_count": null,
          "lines": 3,
          "output_formats": [],
          "legacy_output_formats": "",
          "source": "# Analysis 1: Corpus, Introduction, Data Collection\n\nThis notebook generates the Corpus image and the variables used in the Introduction and Data Collection Sections of the paper.",
          "raw_source": "# Analysis 1: Corpus, Introduction, Data Collection\n\nThis notebook generates the Corpus image and the variables used in the Introduction and Data Collection Sections of the paper.",
          "python": true,
          "status": [],
          "exception": null
        },
        ...
      ],
      "status": "ok",
      "exception": null,
      "sha1_source": "e7736da554be619ec3ddb75f8a0b921295241ec5",
      "word_counter": {
        "homework": 2,
        "assignment": 2,
        "course": 2,
        "exercise": 2,
        "lesson": 2
      }
    }
  ]
  ```
</details>


Using pipe

```
$ juparc list | juparc extract
```

<details>
  <summary>Output: JSON list of JupArc notebook objects</summary>

  ```json
  [
    {
      "name": "analyses/A0.Skip.Notebook.ipynb",
      "nbformat": "4.4",
      "kernel": "python3",
      "language": "python",
      "language_version": "3.7.3",
      "max_execution_count": 40,
      "total_cells": 58,
      "code_cells": 40,
      "code_cells_with_output": 35,
      "markdown_cells": 18,
      ...
    },
    {
      "name": "analyses/A1.Corpus.Introduction.Data.Collection.ipynb",
      "nbformat": "4.4",
      "kernel": "python3",
      "language": "python",
      "language_version": "3.7.3",
      "max_execution_count": 41,
      "total_cells": 54,
      "code_cells": 41,
      "code_cells_with_output": 37,
      "markdown_cells": 13,
      ...
    },
    ...
  ]
  ```
</details>

The study file [archaeology/a1_notebooks_and_cells.py] uses this operation programatically.

### Selecting notebooks

Use the command `juparc select` to select a subset of notebooks based on some attributes.

Standard input: JSON list of JupArc notebook objects (from `$ juparc extract`)

All commands that accept a JSON list of JupArc notebook objects as standard inpup also have the parameter `-n` for disabling the standard input and specifying the notebook files directly.


```
$ juparc list | juparc extract | juparc select --max-execution-count "< 5"
```

<details>
  <summary>Output: JSON list of JupArc notebook objects</summary>

  ```json
  [
    {
      "name": "analyses/Index.ipynb",
      "nbformat": "4.4",
      "kernel": "python3",
      "language": "python",
      "language_version": "3.7.3",
      "max_execution_count": -1,
      "total_cells": 2,
      "code_cells": 1,
      "code_cells_with_output": 0,
      "markdown_cells": 1,
      "raw_cells": 0,
      "unknown_cell_formats": 0,
      "empty_cells": 1,
      "size": 1945,
      "sha1_file": "983738780e1a608791ae1d39d7d4bd3981c08e5b",
      "cells": [
        {
          "index": 0,
          "cell_type": "markdown",
          "execution_count": null,
          "lines": 18,
          "output_formats": [],
          "legacy_output_formats": "",
          "source": "# Index\n\nThe following notebooks analyze the data from the database:\n\n1. [Repositories](N0.Repository.ipynb)\n1. [Skip Notebooks](N1.Skip.Notebook.ipynb)\n1. [Notebooks](N2.Notebook.ipynb)\n1. [Cells](N3.Cell.ipynb)\n1. [IPython Features](N4.Features.ipynb)\n1. [Modules](N5.Modules.ipynb)\n1. [AST](N6.AST.ipynb)\n1. [Names](N7.Name.ipynb)\n1. [Executions](N8.Execution.ipynb)\n1. [Cell Execution Order](N9.Cell.Execution.Order.ipynb)\n1. [Markdown](N10.Markdown.ipynb)\n1. [Repositories With Notebook Restrictions](N11.Repository.With.Notebook.Restriction.ipynb)\n1. [Move to paper folder](N12.To.Paper.ipynb)\n",
          "raw_source": "# Index\n\nThe following notebooks analyze the data from the database:\n\n1. [Repositories](N0.Repository.ipynb)\n1. [Skip Notebooks](N1.Skip.Notebook.ipynb)\n1. [Notebooks](N2.Notebook.ipynb)\n1. [Cells](N3.Cell.ipynb)\n1. [IPython Features](N4.Features.ipynb)\n1. [Modules](N5.Modules.ipynb)\n1. [AST](N6.AST.ipynb)\n1. [Names](N7.Name.ipynb)\n1. [Executions](N8.Execution.ipynb)\n1. [Cell Execution Order](N9.Cell.Execution.Order.ipynb)\n1. [Markdown](N10.Markdown.ipynb)\n1. [Repositories With Notebook Restrictions](N11.Repository.With.Notebook.Restriction.ipynb)\n1. [Move to paper folder](N12.To.Paper.ipynb)\n",
          "python": true,
          "status": [],
          "exception": null
        },
        {
          "index": 1,
          "cell_type": "code",
          "execution_count": null,
          "lines": 1,
          "output_formats": [],
          "legacy_output_formats": "",
          "source": "\n",
          "raw_source": "",
          "python": true,
          "status": [],
          "exception": null
        }
      ],
      "status": "ok",
      "exception": null,
      "sha1_source": "216fe4237c18ef425012bca9ffcc9d484614e8a7",
      "word_counter": {}
    }
  ]

  ```
</details>


This command also provides the `-c` option to count the result:


```
$ juparc list | juparc extract | juparc select --max-execution-count "< 5" -c
```

<details>
  <summary>Output: number</summary>

  ```json
  1
  ```
</details>


### Selecting Python notebooks

Given that most of our analyses are related to Python notebooks, we also provide the command `juparc python` as a synonym to `juparc select --language python`

Standard input: JSON list of JupArc notebook objects (from `$ juparc extract`)

```
$ juparc list | juparc extract | juparc python -c
```

<details>
  <summary>Output: number</summary>

  ```json
  21
  ```
</details>


### Extracting Markdown

The command `juparc markdown` extracts Markdown cells from notebooks.

Standard input: JSON list of JupArc notebook objects (from `$ juparc extract`)

```
$ juparc markdown -n analyses/A0.Skip.Notebook.ipynb 
```

<details>
  <summary>Output: text with all the markdown cells from the notebook, with cells identified by a separator </summary>

  ```


  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:0> ######

  <h1>Table of Contents<span class="tocSkip"></span></h1>
  <div class="toc"><ul class="toc-item"><li><span><a href="#Notebooks" data-toc-modified-id="Notebooks-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Notebooks</a></span><ul class="toc-item"><li><span><a href="#Load" data-toc-modified-id="Load-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Load</a></span></li><li><span><a href="#Mark-false-positive-notebooks-and-notebooks-with-broken-format" data-toc-modified-id="Mark-false-positive-notebooks-and-notebooks-with-broken-format-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Mark false-positive notebooks and notebooks with broken format</a></span></li><li><span><a href="#Mark-empty-notebooks" data-toc-modified-id="Mark-empty-notebooks-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Mark empty notebooks</a></span></li><li><span><a href="#Mark-fork-duplicates" data-toc-modified-id="Mark-fork-duplicates-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Mark fork duplicates</a></span></li><li><span><a href="#Mark-duplicates" data-toc-modified-id="Mark-duplicates-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Mark duplicates</a></span></li><li><span><a href="#Mark-restricted-toy" data-toc-modified-id="Mark-restricted-toy-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Mark restricted toy</a></span></li><li><span><a href="#Mark-toy-examples" data-toc-modified-id="Mark-toy-examples-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Mark toy examples</a></span></li></ul></li></ul></div>

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:1> ######

  # Notebooks

  Analyze notebooks: programming languages, python version, number of cells by notebookk, and notebook names.

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:3> ######

  ## Load

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:7> ######

  Join notebooks and repository updates

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:9> ######

  Set skip = 0

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:11> ######

  ## Mark notebooks from removed repositories

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:13> ######

  ## Mark false-positive notebooks and notebooks with broken format

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:15> ######

  ## Mark empty notebooks

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:17> ######

  ## Mark fork duplicates

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:18> ######

  First, prioritize non-fork notebooks and notebooks from the same repository

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:20> ######

  Mark the notebooks

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:22> ######

  ## Mark duplicates

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:24> ######

  ## Mark restricted toy

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:26> ######

  ## Mark toy examples

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:28> ######

  ## Add stars, forks and metric to notebooks

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:32> ######

  ## Distinguish elite groups

  Get existing non duplicated valid notebooks (endv_notebooks)

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:44> ######

  ## Update Skips

  ###### <juparc:analyses/A0.Skip.Notebook.ipynb:57> ######

  This notebook prepared the skip attributes of all tables to be used in other analyses

  ```
</details>


### Extracting Markdown features

Use the command `juparc markdown-features` to parse the Markdown and extract features from it (number of elements, language, lines, words, stopwords, ...).

Standard input: Markdown text (from `$ juparc markdown` or any other Markdown file)

```
$ juparc markdown -n analyses/A0.Skip.Notebook.ipynb | juparc markdown-features
```

<details>
  <summary>Output: JSON with list of Markdown cells and their features</summary>

  ```json
  [
    {
      "identifier": "analyses/A0.Skip.Notebook.ipynb:0",
      "code": "<h1>Table of Contents<span class=\"tocSkip\"></span></h1>\n<div class=\"toc\"><ul class=\"toc-item\"><li><span><a href=\"#Notebooks\" data-toc-modified-id=\"Notebooks-1\"><span class=\"toc-item-num\">1&nbsp;&nbsp;</span>Notebooks</a></span><ul class=\"toc-item\"><li><span><a href=\"#Load\" data-toc-modified-id=\"Load-1.1\"><span class=\"toc-item-num\">1.1&nbsp;&nbsp;</span>Load</a></span></li><li><span><a href=\"#Mark-false-positive-notebooks-and-notebooks-with-broken-format\" data-toc-modified-id=\"Mark-false-positive-notebooks-and-notebooks-with-broken-format-1.2\"><span class=\"toc-item-num\">1.2&nbsp;&nbsp;</span>Mark false-positive notebooks and notebooks with broken format</a></span></li><li><span><a href=\"#Mark-empty-notebooks\" data-toc-modified-id=\"Mark-empty-notebooks-1.3\"><span class=\"toc-item-num\">1.3&nbsp;&nbsp;</span>Mark empty notebooks</a></span></li><li><span><a href=\"#Mark-fork-duplicates\" data-toc-modified-id=\"Mark-fork-duplicates-1.4\"><span class=\"toc-item-num\">1.4&nbsp;&nbsp;</span>Mark fork duplicates</a></span></li><li><span><a href=\"#Mark-duplicates\" data-toc-modified-id=\"Mark-duplicates-1.5\"><span class=\"toc-item-num\">1.5&nbsp;&nbsp;</span>Mark duplicates</a></span></li><li><span><a href=\"#Mark-restricted-toy\" data-toc-modified-id=\"Mark-restricted-toy-1.6\"><span class=\"toc-item-num\">1.6&nbsp;&nbsp;</span>Mark restricted toy</a></span></li><li><span><a href=\"#Mark-toy-examples\" data-toc-modified-id=\"Mark-toy-examples-1.7\"><span class=\"toc-item-num\">1.7&nbsp;&nbsp;</span>Mark toy examples</a></span></li></ul></li></ul></div>",
      "features": {
        "language": "english",
        "using_stopwords": false,
        "len": 1545,
        "lines": 2,
        "meaningful_lines": 2,
        "words": 48,
        "meaningful_words": 1,
        "stopwords": 0,
        "meaningful_stopwords": 0,
        "header": 0,
        "header_len": 0,
        "header_lines": 0,
        "header_words": 0,
        "header_stopwords": 0,
        "h1": 0,
        "h1_len": 0,
        "h1_lines": 0,
        "h1_words": 0,
        "h1_stopwords": 0,
        "h2": 0,
        "h2_len": 0,
        "h2_lines": 0,
        "h2_words": 0,
        "h2_stopwords": 0,
        "h3": 0,
        "h3_len": 0,
        "h3_lines": 0,
        "h3_words": 0,
        "h3_stopwords": 0,
        "h4": 0,
        "h4_len": 0,
        "h4_lines": 0,
        "h4_words": 0,
        "h4_stopwords": 0,
        "h5": 0,
        "h5_len": 0,
        "h5_lines": 0,
        "h5_words": 0,
        "h5_stopwords": 0,
        "h6": 0,
        "h6_len": 0,
        "h6_lines": 0,
        "h6_words": 0,
        "h6_stopwords": 0,
        "hrule": 0,
        "list": 0,
        "list_len": 0,
        "list_lines": 0,
        "list_items": 0,
        "list_words": 0,
        "list_stopwords": 0,
        "table": 0,
        "table_len": 0,
        "table_lines": 0,
        "table_rows": 0,
        "table_cells": 0,
        "table_words": 0,
        "table_stopwords": 0,
        "p": 1,
        "p_len": 55,
        "p_lines": 1,
        "p_words": 1,
        "p_stopwords": 0,
        "quote": 0,
        "quote_len": 0,
        "quote_lines": 0,
        "quote_words": 0,
        "quote_stopwords": 0,
        "code": 0,
        "code_len": 0,
        "code_lines": 0,
        "code_words": 0,
        "code_stopwords": 0,
        "image": 0,
        "image_len": 0,
        "image_words": 0,
        "image_stopwords": 0,
        "link": 0,
        "link_len": 0,
        "link_words": 0,
        "link_stopwords": 0,
        "autolink": 0,
        "autolink_len": 0,
        "autolink_words": 0,
        "autolink_stopwords": 0,
        "codespan": 0,
        "codespan_len": 0,
        "codespan_words": 0,
        "codespan_stopwords": 0,
        "emphasis": 0,
        "emphasis_len": 0,
        "emphasis_words": 0,
        "emphasis_stopwords": 0,
        "double_emphasis": 0,
        "double_emphasis_len": 0,
        "double_emphasis_words": 0,
        "double_emphasis_stopwords": 0,
        "strikethrough": 0,
        "strikethrough_len": 0,
        "strikethrough_words": 0,
        "strikethrough_stopwords": 0,
        "html": 2,
        "html_len": 1544,
        "html_lines": 1,
        "math": 0,
        "math_len": 0,
        "math_words": 0,
        "math_stopwords": 0,
        "block_math": 0,
        "block_math_len": 0,
        "block_math_lines": 0,
        "block_math_words": 0,
        "block_math_stopwords": 0,
        "latex": 0,
        "latex_len": 0,
        "latex_lines": 0,
        "latex_words": 0,
        "latex_stopwords": 0
      }
    },
    {
      "identifier": "analyses/A0.Skip.Notebook.ipynb:1",
      "code": "# Notebooks\n\nAnalyze notebooks: programming languages, python version, number of cells by notebookk, and notebook names.",
      "features": {
        "language": "english",
        "using_stopwords": false,
        "len": 120,
        "lines": 3,
        "meaningful_lines": 3,
        "words": 16,
        ...
      }
    },
    ...
  ]
  ```
</details>

The study file [archaeology/a4_markdown_features.py] uses this operation programatically.

### Extracting Code features

Use the command `juparc code-features` to parse Python code cells from notebooks and extract features from them (number of AST elements, modules, names, IPython features).

Standard input: JSON list of JupArc notebook objects (from `$ juparc extract`)

```
$ juparc code-features -n analyses/A0.Skip.Notebook.ipynb
```

<details>
  <summary>Output: Enriched JSON list of JupArc notebook objects with new attributes in cells</summary>

  ```json
  [
    {
      "name": "analyses/A0.Skip.Notebook.ipynb",
      "nbformat": "4.4",
      "kernel": "python3",
      "language": "python",
      "language_version": "3.7.3",
      "max_execution_count": 40,
      "total_cells": 58,
      "code_cells": 40,
      "code_cells_with_output": 35,
      "markdown_cells": 18,
      "raw_cells": 0,
      "unknown_cell_formats": 0,
      "empty_cells": 0,
      "size": 25681,
      "sha1_file": "d71182c4ea4566f74ec08b1fd70373df5ca87719",
      "cells": [
        ...
        {
          "index": 1,
          "cell_type": "markdown",
          "execution_count": null,
          "lines": 3,
          "output_formats": [],
          "legacy_output_formats": "",
          "source": "# Notebooks\n\nAnalyze notebooks: programming languages, python version, number of cells by notebookk, and notebook names.",
          "raw_source": "# Notebooks\n\nAnalyze notebooks: programming languages, python version, number of cells by notebookk, and notebook names.",
          "python": true,
          "status": [],
          "exception": null
        },
        {
          "index": 2,
          "cell_type": "code",
          "execution_count": 1,
          "lines": 25,
          "output_formats": [],
          "legacy_output_formats": "",
          "source": "import sys\nsys.path.insert(0, '../archaeology')\n\nfrom string import ascii_letters, digits\n\nimport tqdm\n\nimport numpy as np\nimport pandas as pd\n\nfrom db import connect\n\nimport analysis_helpers, importlib\nimportlib.reload(analysis_helpers)\nfrom analysis_helpers import load_vars, var, relative_var\n\ndef elite(column):\n    column = column.dropna()\n    column = column[column > 0]\n    q1 = column.quantile(0.25)\n    q3 = column.quantile(0.75)\n    iqr = q3 - q1\n    return q3 + 1.5*iqr\n\nget_ipython().run_line_magic('matplotlib', 'inline')\n",
          "raw_source": "import sys\nsys.path.insert(0, '../archaeology')\n\nfrom string import ascii_letters, digits\n\nimport tqdm\n\nimport numpy as np\nimport pandas as pd\n\nfrom db import connect\n\nimport analysis_helpers, importlib\nimportlib.reload(analysis_helpers)\nfrom analysis_helpers import load_vars, var, relative_var\n\ndef elite(column):\n    column = column.dropna()\n    column = column[column > 0]\n    q1 = column.quantile(0.25)\n    q3 = column.quantile(0.75)\n    iqr = q3 - q1\n    return q3 + 1.5*iqr\n\n%matplotlib inline",
          "python": true,
          "status": [],
          "exception": null,
          "ast": {
            "import_star": 0,
            "functions_with_decorators": 0,
            "classes_with_decorators": 0,
            "classes_with_bases": 0,
            "delname": 0,
            "delattr": 0,
            "delitem": 0,
            "assignname": 5,
            "assignattr": 0,
            "assignitem": 0,
            "ipython": 0,
            "ipython_superset": 1,
            "ast_statements": 18,
            "ast_expressions": 39,
            "class_importfrom": 0,
            "global_importfrom": 0,
            "nonlocal_importfrom": 0,
            "local_importfrom": 0,
            "total_importfrom": 6,
            "class_import": 0,
            "global_import": 0,
            "nonlocal_import": 0,
            "local_import": 0,
            "total_import": 6,
            "class_assign": 0,
            "global_assign": 0,
            "nonlocal_assign": 0,
            "local_assign": 5,
            "total_assign": 5,
            "class_delete": 0,
            "global_delete": 0,
            "nonlocal_delete": 0,
            "local_delete": 0,
            "total_delete": 0,
            "class_functiondef": 0,
            "global_functiondef": 0,
            "nonlocal_functiondef": 0,
            "local_functiondef": 0,
            "total_functiondef": 1,
            "class_classdef": 0,
            "global_classdef": 0,
            "nonlocal_classdef": 0,
            "local_classdef": 0,
            "total_classdef": 0,
            "ast_module": 1,
            "ast_interactive": 0,
            "ast_expression": 0,
            "ast_suite": 0,
            "ast_functiondef": 1,
            "ast_asyncfunctiondef": 0,
            "ast_classdef": 0,
            "ast_return": 1,
            "ast_delete": 0,
            "ast_assign": 5,
            "ast_augassign": 0,
            "ast_annassign": 0,
            "ast_print": 0,
            "ast_for": 0,
            "ast_asyncfor": 0,
            "ast_while": 0,
            "ast_if": 0,
            "ast_with": 0,
            "ast_asyncwith": 0,
            "ast_raise": 0,
            "ast_try": 0,
            "ast_tryexcept": 0,
            "ast_tryfinally": 0,
            "ast_assert": 0,
            "ast_import": 5,
            "ast_importfrom": 3,
            "ast_exec": 0,
            "ast_global": 0,
            "ast_nonlocal": 0,
            "ast_expr": 3,
            "ast_pass": 0,
            "ast_break": 0,
            "ast_continue": 0,
            "ast_boolop": 0,
            "ast_binop": 3,
            "ast_unaryop": 0,
            "ast_lambda": 0,
            "ast_ifexp": 0,
            "ast_dict": 0,
            "ast_set": 0,
            "ast_listcomp": 0,
            "ast_setcomp": 0,
            "ast_dictcomp": 0,
            "ast_generatorexp": 0,
            "ast_await": 0,
            "ast_yield": 0,
            "ast_yieldfrom": 0,
            "ast_compare": 1,
            "ast_call": 5,
            "ast_num": 5,
            "ast_str": 1,
            "ast_formattedvalue": 0,
            "ast_joinedstr": 0,
            "ast_bytes": 0,
            "ast_nameconstant": 0,
            "ast_ellipsis": 0,
            "ast_constant": 0,
            "ast_attribute": 6,
            "ast_subscript": 1,
            "ast_starred": 0,
            "ast_name": 17,
            "ast_list": 0,
            "ast_tuple": 0,
            "ast_load": 19,
            "ast_store": 5,
            "ast_del": 0,
            "ast_augload": 0,
            "ast_augstore": 0,
            "ast_param": 0,
            "ast_slice": 0,
            "ast_index": 1,
            "ast_and": 0,
            "ast_or": 0,
            "ast_add": 1,
            "ast_sub": 1,
            "ast_mult": 1,
            "ast_matmult": 0,
            "ast_div": 0,
            "ast_mod": 0,
            "ast_pow": 0,
            "ast_lshift": 0,
            "ast_rshift": 0,
            "ast_bitor": 0,
            "ast_bitxor": 0,
            "ast_bitand": 0,
            "ast_floordiv": 0,
            "ast_invert": 0,
            "ast_not": 0,
            "ast_uadd": 0,
            "ast_usub": 0,
            "ast_eq": 0,
            "ast_noteq": 0,
            "ast_lt": 0,
            "ast_lte": 0,
            "ast_gt": 1,
            "ast_gte": 0,
            "ast_is": 0,
            "ast_isnot": 0,
            "ast_in": 0,
            "ast_notin": 0,
            "ast_comprehension": 0,
            "ast_excepthandler": 0,
            "ast_arguments": 1,
            "ast_arg": 1,
            "ast_keyword": 0,
            "ast_alias": 12,
            "ast_withitem": 0,
            "ast_others": ""
          },
          "modules": [
            {
              "line": 1,
              "import_type": "import",
              "name": "sys",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 4,
              "import_type": "import_from",
              "name": "string",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 6,
              "import_type": "import",
              "name": "tqdm",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 8,
              "import_type": "import",
              "name": "numpy",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 9,
              "import_type": "import",
              "name": "pandas",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 11,
              "import_type": "import_from",
              "name": "db",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 13,
              "import_type": "import",
              "name": "analysis_helpers",
              "local": true,
              "local_possibility": 4
            },
            {
              "line": 13,
              "import_type": "import",
              "name": "importlib",
              "local": false,
              "local_possibility": 0
            },
            {
              "line": 15,
              "import_type": "import_from",
              "name": "analysis_helpers",
              "local": true,
              "local_possibility": 4
            }
          ],
          "names": {
            "main": {
              "import": {
                "sys": 1,
                "tqdm": 1,
                "np": 1,
                "pd": 1,
                "analysis_helpers": 1,
                "importlib": 1
              },
              "load": {
                "sys": 1,
                "importlib": 1,
                "analysis_helpers": 1
              },
              "importfrom": {
                "ascii_letters": 1,
                "digits": 1,
                "connect": 1,
                "load_vars": 1,
                "var": 1,
                "relative_var": 1
              },
              "function": {
                "elite": 1
              }
            },
            "local": {
              "store": {
                "column": 2,
                "q1": 1,
                "q3": 1,
                "iqr": 1
              },
              "load": {
                "column": 5,
                "q3": 2,
                "q1": 1,
                "iqr": 1
              }
            }
          },
          "ipython": [
            [
              25,
              0,
              "run_line_magic",
              "matplotlib"
            ]
          ]
        },
        ...
      ]
    }
  ]
  ```
</details>

The study file [archaeology/a6_cell_features.py] uses this operation programatically.


### Aggregating Markdown features

The command `juparc aggregate-markdown` combines the markdown analyses of multiple cells into a single aggregate object.

Standard input: JSON with list of Markdown cells and their features (from `$ juparc markdown-features`)

```
$ juparc markdown-features -n analyses/A0.Skip.Notebook.ipynb | juparc aggregate-markdown
```

<details>
  <summary>Output: JSON object with groups of aggregated objects </summary>

  ```json
  {
    "analyses/A0.Skip.Notebook.ipynb": {
      "using_stopwords": 0,
      "len": 2260,
      "lines": 23,
      "meaningful_lines": 33,
      "words": 159,
      "meaningful_words": 100,
      "stopwords": 0,
      "meaningful_stopwords": 0,
      "header": 12,
      "header_len": 282,
      "header_lines": 12,
      "header_words": 41,
      "header_stopwords": 0,
      "h1": 1,
      "h1_len": 9,
      "h1_lines": 1,
      "h1_words": 1,
      "h1_stopwords": 0,
      "h2": 11,
      "h2_len": 273,
      "h2_lines": 11,
      "h2_words": 40,
      "h2_stopwords": 0,
      "h3": 0,
      "h3_len": 0,
      "h3_lines": 0,
      "h3_words": 0,
      "h3_stopwords": 0,
      "h4": 0,
      "h4_len": 0,
      "h4_lines": 0,
      "h4_words": 0,
      "h4_stopwords": 0,
      "h5": 0,
      "h5_len": 0,
      "h5_lines": 0,
      "h5_words": 0,
      "h5_stopwords": 0,
      "h6": 0,
      "h6_len": 0,
      "h6_lines": 0,
      "h6_words": 0,
      "h6_stopwords": 0,
      "hrule": 0,
      "list": 0,
      "list_len": 0,
      "list_lines": 0,
      "list_items": 0,
      "list_words": 0,
      "list_stopwords": 0,
      "table": 0,
      "table_len": 0,
      "table_lines": 0,
      "table_rows": 0,
      "table_cells": 0,
      "table_words": 0,
      "table_stopwords": 0,
      "p": 8,
      "p_len": 449,
      "p_lines": 8,
      "p_words": 59,
      "p_stopwords": 0,
      "quote": 0,
      "quote_len": 0,
      "quote_lines": 0,
      "quote_words": 0,
      "quote_stopwords": 0,
      "code": 0,
      "code_len": 0,
      "code_lines": 0,
      "code_words": 0,
      "code_stopwords": 0,
      "image": 0,
      "image_len": 0,
      "image_words": 0,
      "image_stopwords": 0,
      "link": 0,
      "link_len": 0,
      "link_words": 0,
      "link_stopwords": 0,
      "autolink": 0,
      "autolink_len": 0,
      "autolink_words": 0,
      "autolink_stopwords": 0,
      "codespan": 0,
      "codespan_len": 0,
      "codespan_words": 0,
      "codespan_stopwords": 0,
      "emphasis": 0,
      "emphasis_len": 0,
      "emphasis_words": 0,
      "emphasis_stopwords": 0,
      "double_emphasis": 0,
      "double_emphasis_len": 0,
      "double_emphasis_words": 0,
      "double_emphasis_stopwords": 0,
      "strikethrough": 0,
      "strikethrough_len": 0,
      "strikethrough_words": 0,
      "strikethrough_stopwords": 0,
      "html": 2,
      "html_len": 1544,
      "html_lines": 1,
      "math": 0,
      "math_len": 0,
      "math_words": 0,
      "math_stopwords": 0,
      "block_math": 0,
      "block_math_len": 0,
      "block_math_lines": 0,
      "block_math_words": 0,
      "block_math_stopwords": 0,
      "latex": 0,
      "latex_len": 0,
      "latex_lines": 0,
      "latex_words": 0,
      "latex_stopwords": 0,
      "cell_count": 18,
      "main_language": "english",
      "languages": "english,norwegian,spanish,undetected",
      "languages_counts": "14,2,1,1"
    }
  }
  ```
</details>

Use REGEX in the `-g` option to separate the groups. The default value is `(.*):\d*`, which aggregates cells by notebooks. Use `(.*)` to have each cell in the result individually or `.*` to have a single `<default>` group with all the aggregated results. It aggregates cells that do not match the REGEX into the `<default>` group.

The study file [archaeology/a7_notebook_aggregate.py] uses this operation programatically.

### Aggregating Code features

The command `juparc code-markdown` combines the code analyses of multiple cells into a single aggregate object.

Standard input: Enriched JSON list of JupArc notebook objects with new attributes in cells (from `$ juparc code-features`)

```
$ juparc code-features -n analyses/A0.Skip.Notebook.ipynb | juparc aggregate-code
```

<details>
  <summary>Output: JSON object with groups of aggregated code objects </summary>

  ```json
  [
    {
      "name": "analyses/A1.Corpus.Introduction.Data.Collection.ipynb",
      "ast": {
        "import_star": 0,
        "functions_with_decorators": 0,
        "classes_with_decorators": 0,
        "classes_with_bases": 0,
        "delname": 0,
        "delattr": 0,
        "delitem": 0,
        "assignname": 79,
        "assignattr": 2,
        "assignitem": 0,
        "ipython": 0,
        "ipython_superset": 2,
        "ast_statements": 193,
        "ast_expressions": 1422,
        "class_importfrom": 0,
        "global_importfrom": 0,
        "nonlocal_importfrom": 0,
        "local_importfrom": 0,
        "total_importfrom": 20,
        "class_import": 0,
        "global_import": 0,
        "nonlocal_import": 0,
        "local_import": 0,
        "total_import": 7,
        "class_assign": 0,
        "global_assign": 0,
        "nonlocal_assign": 0,
        "local_assign": 21,
        "total_assign": 81,
        "class_delete": 0,
        "global_delete": 0,
        "nonlocal_delete": 0,
        "local_delete": 0,
        "total_delete": 0,
        "class_functiondef": 0,
        "global_functiondef": 0,
        "nonlocal_functiondef": 0,
        "local_functiondef": 0,
        "total_functiondef": 5,
        "class_classdef": 0,
        "global_classdef": 0,
        "nonlocal_classdef": 0,
        "local_classdef": 0,
        "total_classdef": 0,
        "ast_module": 41,
        "ast_interactive": 0,
        "ast_expression": 0,
        "ast_suite": 0,
        "ast_functiondef": 5,
        "ast_asyncfunctiondef": 0,
        "ast_classdef": 0,
        "ast_return": 2,
        "ast_delete": 0,
        "ast_assign": 63,
        "ast_augassign": 0,
        "ast_annassign": 0,
        "ast_print": 0,
        "ast_for": 4,
        "ast_asyncfor": 0,
        "ast_while": 0,
        "ast_if": 1,
        "ast_with": 8,
        "ast_asyncwith": 0,
        "ast_raise": 0,
        "ast_try": 0,
        "ast_tryexcept": 0,
        "ast_tryfinally": 0,
        "ast_assert": 0,
        "ast_import": 6,
        "ast_importfrom": 10,
        "ast_exec": 0,
        "ast_global": 0,
        "ast_nonlocal": 0,
        "ast_expr": 94,
        "ast_pass": 0,
        "ast_break": 0,
        "ast_continue": 0,
        "ast_boolop": 0,
        "ast_binop": 32,
        "ast_unaryop": 7,
        "ast_lambda": 1,
        "ast_ifexp": 0,
        "ast_dict": 1,
        "ast_set": 0,
        "ast_listcomp": 0,
        "ast_setcomp": 0,
        "ast_dictcomp": 0,
        "ast_generatorexp": 0,
        "ast_await": 0,
        "ast_yield": 0,
        "ast_yieldfrom": 0,
        "ast_compare": 22,
        "ast_call": 275,
        "ast_num": 67,
        "ast_str": 232,
        "ast_formattedvalue": 0,
        "ast_joinedstr": 0,
        "ast_bytes": 0,
        "ast_nameconstant": 11,
        "ast_ellipsis": 0,
        "ast_constant": 0,
        "ast_attribute": 116,
        "ast_subscript": 89,
        "ast_starred": 0,
        "ast_name": 548,
        "ast_list": 6,
        "ast_tuple": 15,
        "ast_load": 678,
        "ast_store": 96,
        "ast_del": 0,
        "ast_augload": 0,
        "ast_augstore": 0,
        "ast_param": 0,
        "ast_slice": 0,
        "ast_index": 89,
        "ast_and": 0,
        "ast_or": 0,
        "ast_add": 13,
        "ast_sub": 3,
        "ast_mult": 0,
        "ast_matmult": 0,
        "ast_div": 0,
        "ast_mod": 0,
        "ast_pow": 0,
        "ast_lshift": 0,
        "ast_rshift": 0,
        "ast_bitor": 11,
        "ast_bitxor": 0,
        "ast_bitand": 5,
        "ast_floordiv": 0,
        "ast_invert": 2,
        "ast_not": 0,
        "ast_uadd": 0,
        "ast_usub": 5,
        "ast_eq": 15,
        "ast_noteq": 0,
        "ast_lt": 0,
        "ast_lte": 2,
        "ast_gt": 3,
        "ast_gte": 1,
        "ast_is": 0,
        "ast_isnot": 0,
        "ast_in": 1,
        "ast_notin": 0,
        "ast_comprehension": 0,
        "ast_excepthandler": 0,
        "ast_arguments": 6,
        "ast_arg": 11,
        "ast_keyword": 32,
        "ast_alias": 27,
        "ast_withitem": 8,
        "cell_count": 41,
        "ast_others": ""
      },
      "modules": {
        "local_any": "analysis_helpers",
        "local_any_count": 1,
        "local_load_ext": "",
        "local_load_ext_count": 0,
        "local_import": "analysis_helpers",
        "local_import_count": 1,
        "local_import_from": "analysis_helpers",
        "local_import_from_count": 1,
        "external_any": "sys,re,matplotlib,numpy,pandas,datetime,IPython.display,importlib,db",
        "external_any_count": 9,
        "external_load_ext": "",
        "external_load_ext_count": 0,
        "external_import": "sys,re,matplotlib,numpy,pandas,importlib",
        "external_import_count": 6,
        "external_import_from": "datetime,matplotlib,IPython.display,db",
        "external_import_from_count": 4,
        "any_any": "sys,re,matplotlib,numpy,pandas,datetime,IPython.display,analysis_helpers,importlib,db",
        "any_any_count": 10,
        "any_load_ext": "",
        "any_load_ext_count": 0,
        "any_import": "sys,re,matplotlib,numpy,pandas,analysis_helpers,importlib",
        "any_import_count": 7,
        "any_import_from": "datetime,matplotlib,IPython.display,analysis_helpers,db",
        "any_import_from_count": 5,
        "index": "1",
        "index_count": 1,
        "others": ""
      },
      "names": {
        "index": "1,3,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,29,30,31,32,35,36,37,39,41,43,45,46,47,49,51,52",
        "index_count": 40,
        "any_any": "dbmt,non_duplicated,print,len,valid_notebooks,dbmt_relative_var,python_notebooks,df,prefix,plt,var,attempted_execution,gcf,relative_var,ax,t_repositories,executed_notebooks,existing_notebooks,dfs,name,np,ax1,pd,unambiguous_python_notebooks,ax2,first,last,savefig,boxplot_distribution,DBMT,unambiguous_notebooks,key,column,step,fig,f,zip,display,ax3,max_execution_count_dist,code_cells_dist,load_vars,histogram,numpy_distribution,session,boolagg,threshold,popular_notebooks,non_duplicated_repos,sampled_notebooks,VAR,repositories_10_or_more,bins,sys,re,matplotlib,analysis_helpers,importlib,datetime,SVG,display_counts,distribution_with_boxplot,connect,existing_repositories,valid_repositories,bottom_notebooks,vs,float,popular_repos,samples,sampled_repos,r_notebooks,julia_notebooks,unknown_notebooks,python2_notebooks,python3_notebooks,python_unknown,valid_syntax,svg_content,open,replace,x,repro_finished,same_results_original,same_results_image,repositories_2_or_fewer,duplicated_total,programming_language,max_exectuion_count,code_cells_max_exectuion_count,correrlation,six_months_after_notebooks,requery_date,last_six_months_notebooks,print_relative_var_group,mask,counts,slice,cnt,distribution",
        "any_any_counts": "39,37,33,28,19,18,18,17,17,15,14,14,13,12,11,10,10,8,8,8,7,7,6,6,6,6,6,5,5,5,5,5,5,5,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1",
        "any_class": "",
        "any_class_counts": "",
        "any_import": "sys,re,matplotlib,np,pd,analysis_helpers,importlib",
        "any_import_counts": "1,1,1,1,1,1,1",
        "any_importfrom": "fig,boxplot_distribution,datetime,plt,SVG,load_vars,var,relative_var,savefig,display_counts,distribution_with_boxplot,dbmt,DBMT,print_relative_var_group,dbmt_relative_var,histogram,numpy_distribution,connect",
        "any_importfrom_counts": "2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "any_function": "replace,programming_language,max_exectuion_count,code_cells_max_exectuion_count,correrlation",
        "any_function_counts": "1,1,1,1,1",
        "any_param": "",
        "any_param_counts": "",
        "any_del": "",
        "any_del_counts": "",
        "any_load": "dbmt,non_duplicated,print,len,valid_notebooks,dbmt_relative_var,python_notebooks,plt,var,attempted_execution,df,prefix,relative_var,t_repositories,executed_notebooks,ax,gcf,existing_notebooks,np,ax1,pd,unambiguous_python_notebooks,last,first,ax2,unambiguous_notebooks,key,zip,dfs,DBMT,name,savefig,display,step,boxplot_distribution,ax3,max_execution_count_dist,code_cells_dist,session,boolagg,load_vars,float,threshold,popular_notebooks,non_duplicated_repos,sampled_notebooks,open,f,x,VAR,repositories_10_or_more,column,histogram,bins,numpy_distribution,sys,importlib,analysis_helpers,connect,existing_repositories,valid_repositories,bottom_notebooks,vs,popular_repos,samples,sampled_repos,r_notebooks,julia_notebooks,unknown_notebooks,python2_notebooks,python3_notebooks,python_unknown,valid_syntax,re,replace,svg_content,SVG,repro_finished,same_results_original,same_results_image,repositories_2_or_fewer,duplicated_total,programming_language,display_counts,counts,slice,max_exectuion_count,distribution_with_boxplot,code_cells_max_exectuion_count,matplotlib,correrlation,fig,six_months_after_notebooks,datetime,requery_date,last_six_months_notebooks",
        "any_load_counts": "38,36,33,28,18,17,17,14,13,13,13,13,11,9,9,9,8,7,6,6,5,5,5,5,5,4,4,4,4,4,4,4,4,4,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "any_store": "gcf,dfs,df,prefix,name,column,f,ax,session,boolagg,t_repositories,existing_notebooks,existing_repositories,valid_notebooks,valid_repositories,mask,non_duplicated,bottom_notebooks,vs,threshold,popular_notebooks,non_duplicated_repos,popular_repos,samples,sampled_notebooks,sampled_repos,python_notebooks,r_notebooks,julia_notebooks,unknown_notebooks,python2_notebooks,python3_notebooks,python_unknown,valid_syntax,executed_notebooks,unambiguous_notebooks,unambiguous_python_notebooks,VAR,svg_content,key,attempted_execution,repro_finished,same_results_original,same_results_image,repositories_2_or_fewer,repositories_10_or_more,duplicated_total,fig,cnt,distribution,ax3,ax1,ax2,first,last,step,bins,max_execution_count_dist,code_cells_dist,six_months_after_notebooks,requery_date,last_six_months_notebooks",
        "any_store_counts": "5,4,4,4,4,3,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "nonlocal_any": "",
        "nonlocal_any_counts": "",
        "nonlocal_class": "",
        "nonlocal_class_counts": "",
        "nonlocal_import": "",
        "nonlocal_import_counts": "",
        "nonlocal_importfrom": "",
        "nonlocal_importfrom_counts": "",
        "nonlocal_function": "",
        "nonlocal_function_counts": "",
        "nonlocal_param": "",
        "nonlocal_param_counts": "",
        "nonlocal_del": "",
        "nonlocal_del_counts": "",
        "nonlocal_load": "",
        "nonlocal_load_counts": "",
        "nonlocal_store": "",
        "nonlocal_store_counts": "",
        "local_any": "ax,prefix,df,print,plt,ax1,ax2,first,last,key,step,savefig,column,gcf,ax3,max_execution_count_dist,code_cells_dist,var,boxplot_distribution,bins,x,VAR,fig,histogram,numpy_distribution,display_counts,counts,slice,cnt,distribution_with_boxplot,display,distribution,matplotlib",
        "local_any_counts": "11,9,9,7,7,7,6,6,6,5,5,4,4,4,4,4,4,4,3,3,2,2,2,2,2,1,1,1,1,1,1,1,1",
        "local_class": "",
        "local_class_counts": "",
        "local_import": "",
        "local_import_counts": "",
        "local_importfrom": "",
        "local_importfrom_counts": "",
        "local_function": "",
        "local_function_counts": "",
        "local_param": "",
        "local_param_counts": "",
        "local_del": "",
        "local_del_counts": "",
        "local_load": "prefix,ax,df,print,plt,ax1,last,first,ax2,key,savefig,step,var,boxplot_distribution,ax3,max_execution_count_dist,code_cells_dist,x,VAR,column,gcf,histogram,bins,numpy_distribution,display_counts,counts,slice,distribution_with_boxplot,display,matplotlib,fig",
        "local_load_counts": "9,9,9,7,7,6,5,5,5,4,4,4,4,3,3,3,3,2,2,2,2,2,2,2,1,1,1,1,1,1,1",
        "local_store": "ax,gcf,column,key,fig,cnt,distribution,ax3,ax1,ax2,first,last,step,bins,max_execution_count_dist,code_cells_dist",
        "local_store_counts": "2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "class_any": "",
        "class_any_counts": "",
        "class_class": "",
        "class_class_counts": "",
        "class_import": "",
        "class_import_counts": "",
        "class_importfrom": "",
        "class_importfrom_counts": "",
        "class_function": "",
        "class_function_counts": "",
        "class_param": "",
        "class_param_counts": "",
        "class_del": "",
        "class_del_counts": "",
        "class_load": "",
        "class_load_counts": "",
        "class_store": "",
        "class_store_counts": "",
        "global_any": "",
        "global_any_counts": "",
        "global_class": "",
        "global_class_counts": "",
        "global_import": "",
        "global_import_counts": "",
        "global_importfrom": "",
        "global_importfrom_counts": "",
        "global_function": "",
        "global_function_counts": "",
        "global_param": "",
        "global_param_counts": "",
        "global_del": "",
        "global_del_counts": "",
        "global_load": "",
        "global_load_counts": "",
        "global_store": "",
        "global_store_counts": "",
        "main_any": "dbmt,non_duplicated,len,print,valid_notebooks,dbmt_relative_var,python_notebooks,attempted_execution,relative_var,var,t_repositories,executed_notebooks,gcf,plt,existing_notebooks,dfs,df,prefix,name,np,pd,unambiguous_python_notebooks,DBMT,unambiguous_notebooks,f,zip,load_vars,session,boolagg,threshold,popular_notebooks,non_duplicated_repos,sampled_notebooks,repositories_10_or_more,display,sys,re,analysis_helpers,importlib,datetime,SVG,fig,boxplot_distribution,connect,existing_repositories,valid_repositories,bottom_notebooks,vs,float,popular_repos,samples,sampled_repos,r_notebooks,julia_notebooks,unknown_notebooks,python2_notebooks,python3_notebooks,python_unknown,valid_syntax,svg_content,open,replace,repro_finished,same_results_original,same_results_image,repositories_2_or_fewer,duplicated_total,programming_language,max_exectuion_count,code_cells_max_exectuion_count,correrlation,six_months_after_notebooks,requery_date,last_six_months_notebooks,matplotlib,savefig,display_counts,distribution_with_boxplot,print_relative_var_group,histogram,numpy_distribution,mask,VAR,column",
        "main_any_counts": "39,37,28,26,19,18,18,14,12,10,10,10,9,8,8,8,8,8,8,7,6,6,5,5,4,4,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1",
        "main_class": "",
        "main_class_counts": "",
        "main_import": "sys,re,matplotlib,np,pd,analysis_helpers,importlib",
        "main_import_counts": "1,1,1,1,1,1,1",
        "main_importfrom": "fig,boxplot_distribution,datetime,plt,SVG,load_vars,var,relative_var,savefig,display_counts,distribution_with_boxplot,dbmt,DBMT,print_relative_var_group,dbmt_relative_var,histogram,numpy_distribution,connect",
        "main_importfrom_counts": "2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "main_function": "replace,programming_language,max_exectuion_count,code_cells_max_exectuion_count,correrlation",
        "main_function_counts": "1,1,1,1,1",
        "main_param": "",
        "main_param_counts": "",
        "main_del": "",
        "main_del_counts": "",
        "main_load": "dbmt,non_duplicated,len,print,valid_notebooks,dbmt_relative_var,python_notebooks,attempted_execution,relative_var,var,t_repositories,executed_notebooks,existing_notebooks,plt,np,gcf,pd,unambiguous_python_notebooks,unambiguous_notebooks,zip,dfs,DBMT,name,df,prefix,display,session,boolagg,load_vars,float,threshold,popular_notebooks,non_duplicated_repos,sampled_notebooks,open,f,repositories_10_or_more,sys,importlib,analysis_helpers,connect,existing_repositories,valid_repositories,bottom_notebooks,vs,popular_repos,samples,sampled_repos,r_notebooks,julia_notebooks,unknown_notebooks,python2_notebooks,python3_notebooks,python_unknown,valid_syntax,re,replace,svg_content,SVG,repro_finished,same_results_original,same_results_image,repositories_2_or_fewer,duplicated_total,programming_language,max_exectuion_count,code_cells_max_exectuion_count,correrlation,six_months_after_notebooks,datetime,requery_date,last_six_months_notebooks",
        "main_load_counts": "38,36,28,26,18,17,17,13,11,9,9,9,7,7,6,6,5,5,4,4,4,4,4,4,4,3,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "main_store": "dfs,df,prefix,name,gcf,f,session,boolagg,t_repositories,existing_notebooks,existing_repositories,valid_notebooks,valid_repositories,mask,non_duplicated,bottom_notebooks,vs,threshold,popular_notebooks,non_duplicated_repos,popular_repos,samples,sampled_notebooks,sampled_repos,python_notebooks,r_notebooks,julia_notebooks,unknown_notebooks,python2_notebooks,python3_notebooks,python_unknown,valid_syntax,executed_notebooks,unambiguous_notebooks,unambiguous_python_notebooks,VAR,svg_content,attempted_execution,repro_finished,same_results_original,same_results_image,repositories_2_or_fewer,repositories_10_or_more,duplicated_total,column,six_months_after_notebooks,requery_date,last_six_months_notebooks",
        "main_store_counts": "4,4,4,4,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
        "others": ""
      },
      "ipython": {
        "shadown_ref": "",
        "shadown_ref_count": 0,
        "output_ref": "",
        "output_ref_count": 0,
        "system": "inkscape",
        "system_count": 1,
        "set_next_input": "",
        "set_next_input_count": 0,
        "input_ref": "",
        "input_ref_count": 0,
        "magic": "",
        "magic_count": 0,
        "run_line_magic": "matplotlib",
        "run_line_magic_count": 1,
        "run_cell_magic": "",
        "run_cell_magic_count": 0,
        "getoutput": "",
        "getoutput_count": 0,
        "set_hook": "",
        "set_hook_count": 0,
        "any": "matplotlib,inkscape",
        "any_count": 2,
        "index": "1,27",
        "index_count": 2,
        "others": ""
      }
    }
  ]
  ```
</details>

The study file [archaeology/a7_notebook_aggregate.py] uses this operation programatically.