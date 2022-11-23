import openpyxl
from jinja2 import Environment, FileSystemLoader
import pdfkit


vac = 'Программист'

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("2.1.3.html")

columns1 = ['Год', 'Средняя зарплата', f'Средняя зарплата - {vac}', 'Количество вакансий',
                    f'Количество вакансий - {vac}']
columns2 = ['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий']
salary_years =  {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510, 2014: 50658}
vac_salary_years =  {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960, 2013: 58804, 2014: 62384}
vacs_years = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954, 2014: 66837}
vac_count_years =  {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990, 2014: 5492}
res_sort_area_salary =  {'Москва': 57354, 'Санкт-Петербург': 46291, 'Новосибирск': 41580, 'Екатеринбург': 41091, 'Казань': 37587, 'Самара': 34091, 'Нижний Новгород': 33637, 'Ярославль': 32744, 'Краснодар': 32542, 'Воронеж': 29725}
res_sort_fract_vac_area = {'Москва': 0.4581, 'Санкт-Петербург': 0.1415, 'Нижний Новгород': 0.0269, 'Казань': 0.0266, 'Ростов-на-Дону': 0.0234, 'Новосибирск': 0.0202, 'Екатеринбург': 0.0143, 'Воронеж': 0.014, 'Самара': 0.0133, 'Краснодар': 0.0131}
pdf_template = template.render({'vac': vac,
                                'columns1': columns1,
                                'salary_years': salary_years,
                                'vac_salary_years': vac_salary_years,
                                'vacs_years': vacs_years,
                                'vac_count_years': vac_count_years,
                                'res_sort_area_salary': res_sort_area_salary,
                                'res_sort_fract_vac_area': res_sort_fract_vac_area,
                                'columns2': columns2})

options = {'enable-local-file-access': None}

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

pdfkit.from_string(pdf_template, '2.1.3.pdf', configuration=config, options=options)

print(res_sort_fract_vac_area)
for key, value in res_sort_fract_vac_area.items():
    res_sort_fract_vac_area[key] = str(round(res_sort_fract_vac_area[key] * 100, 2)) + '%'
del res_sort_fract_vac_area['Москва']
print(res_sort_fract_vac_area)