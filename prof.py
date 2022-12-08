from pstats import Stats, SortKey
import cProfile
import pdf_report
from datetime import datetime


cProfile.run('pdf_report.InputConnect()', 'restats')
p = Stats('restats')
p.sort_stats(SortKey.TIME).print_stats(5)
