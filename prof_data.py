from pstats import Stats, SortKey
import cProfile
import pdf_report
from datetime import datetime


def format_data(date):
    # return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y')
    # return date[:4]
    date.split('-')
    return date[0]
cProfile.run('format_data("2022-12-08T22:24:09+0300")', 'restats')
p = Stats('restats')
p.sort_stats(SortKey.TIME).print_stats(5)
