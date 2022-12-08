"""
Скрипт разделяет файл вакансий на файлы, разделенные по году
"""

import pandas as pd
from pdf_report import format_date


class SplitData:
    def __init__(self, file_name):
        pd.set_option('expand_frame_repr', False)
        df = pd.read_csv(file_name)
        df['years'] = df['published_at'].apply(format_date)
        years = df['years'].unique()

        for year in years:
            data = df[df['years'] == year]
            data.drop(columns='years').to_csv(rf'csv_files\csv_{year}.csv', index=False)


SplitData('vacancies_by_year.csv')