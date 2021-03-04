import csv
import dask.dataframe as dd
from dask.dataframe.core import Series as DaskSeries
from dask.array.core import Array as DaskArray
from dask.array import histogram as _dask_histogram

from analysis_helpers import display_counts, distribution_with_boxplot
from analysis_helpers import boxplot_distribution


def dask_from_query(session, query, file):
    q = session.execute(query)
    with open(file, 'w') as outfile:
        outcsv = csv.writer(outfile)
        outcsv.writerow(x[0] for x in q.cursor.description)
        outcsv.writerows(fetchgenerator(q.cursor))
    return dd.read_csv(file)


def dask_display_counts(counts, *args, **kwargs):
    counts = counts.compute() if isinstance(counts, DaskSeries) else counts
    return display_counts(counts, *args, **kwargs)


def dask_distribution_with_boxplot(column, *args, **kwargs):
    column = column.compute() if isinstance(column, DaskSeries) else column
    return distribution_with_boxplot(column, *args, **kwargs)


def dask_boxplot_distribution(column, *args, **kwargs):
    column = column.compute() if isinstance(column, DaskSeries) else column
    return boxplot_distribution(column, *args, **kwargs)


def dask_histogram(*args, **kwargs):
    histfn = _dask_histogram if isinstance(column, DaskArray) else np.histogram
    return histogram(*args, histfn=histfn, **kwargs)
