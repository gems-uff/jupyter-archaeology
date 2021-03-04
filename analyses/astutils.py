from collections import Counter
from itertools import combinations
from analysis_helpers import count, counter_hist

SCOPES = ["global", "main", "local", "nonlocal", "class"]

def count_combinantions(df, options, name):
    result = Counter()
    for r in range(len(options)):
        for include in combinations(options, r + 1):
            exclude = [x for x in options if x not in include]
            label = "only {} {}".format(",".join(include), name)
            condition = None
            for col in include:
                col_label = "{}_{}".format(col, name)
                if condition is None:
                    condition = df[col_label] != 0
                else:
                    condition &= df[col_label] != 0
            for col in exclude:
                col_label = "{}_{}".format(col, name)
                condition &= df[col_label] == 0
            result[label] = len(df[condition])
    condition = None
    for col in options:
        col_label = "{}_{}".format(col, name)
        if condition is None:
            condition = df[col_label] == 0
        else:
            condition &= df[col_label] == 0
    result["none"] = len(df[condition])
    return result


def show_scope(notebooks, category, extra_counter = None, width=4, logy=False):
    counter = count(
        notebooks,
        "total_{}".format(category),
        *["{}_{}".format(scope, category)
          for scope in SCOPES]
    )
    if extra_counter is not None:
        counter += extra_counter
    
    return counter_hist(
        counter,
        label="Notebooks",
        width=width,
        show_values=True,
        logy=logy,
        template="{:,}",
        template2="{:,.0f}",
    )


def describe_sets(notebooks, category):
    return counter_hist(
        count_combinantions(
            notebooks, SCOPES, category
        ),
        width=15,
        show_values=True,
        template="{:,}",
        template2="{:,.0f}",
    )

def chain_hist(*args):
    spaces = 0
    for i, arg in enumerate(args):
        yield from arg
        if i != len(args) - 1:
            yield (" " * spaces, "Main", 0)
            spaces += 1

