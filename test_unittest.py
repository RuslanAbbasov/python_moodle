from unittest import TestCase
import pdf_report
import table_report

vac1 = {'name': 'Web-программист',
        'experience_id': 'Нет опыта', 'premium': 'Нет', 'employer_name': 'Асташенков Г. А.',
        'salary_from': '30000 - 80000 (Рубли) (С вычетом налогов)', 'area_name': 'Ульяновск',
        'published_at': '2022-05-31T17:32:31+0300'}
vac2 = {'name': 'Junior+/ Middle Python разработчик',
        'experience_id': 'От 1 года до 3 лет', 'premium': 'Нет', 'employer_name': 'CiPlay',
        'salary_from': '40000 - 80000 (Рубли) (С вычетом налогов)', 'area_name': 'Санкт-Петербург',
        'published_at': '2022-05-31T17:44:23+0300'}
vac3 = {'name': 'DevOps/Системный администратор',
        'experience_id': 'От 3 до 6 лет', 'premium': 'Нет', 'employer_name': 'ИИТ',
        'salary_from': '150000 - 350000 (Рубли) (С вычетом налогов)', 'area_name': 'Москва',
        'published_at': '2022-06-27T17:54:01+0300'}
lst_vac = [vac1, vac2, vac3]


class PdfTest(TestCase):
    def testFirstEl(self):
        dic10 = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                 '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11}
        dic8 = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                '6': 6, '7': 7, '8': 8}
        self.assertEqual(len(pdf_report.InputConnect.first_el(dic10)), 10)
        self.assertEqual(len(pdf_report.InputConnect.first_el(dic8)), 8)

    def testSymN(self):
        dic = {'Москва': 0.4581, 'Санкт-Петербург': 0.1415, 'Нижний Новгород': 0.0269, 'Казань': 0.0266}
        dicCor = {'Москва': 0.4581, 'Санкт\nПетербург': 0.1415, 'Нижний\nНовгород': 0.0269, 'Казань': 0.0266}
        self.assertEqual(pdf_report.Report.sym_n(dic), dicCor)

    def testRemoveTags(self):
        lst = ['<h1>name', 'key_skills<li></li>', 'premium<h1>', 'employer_name', 'salary_from', '<body>salary_to',
               'area_name',
               '<h1>Программист', 'Информационные технологии',
               '<h1>Автоматизированное рабочее<li></li> место (АРМ)', 'FALSE', '<body>Контур', '70000', '110000',
               'Москва',
               'Инженер', '<li></li>Ответственность']
        lstCor = ['name', 'key_skills', 'premium', 'employer_name', 'salary_from', 'salary_to', 'area_name',
                  'Программист', 'Информационные технологии',
                  'Автоматизированное рабочее место (АРМ)', 'FALSE', 'Контур', '70000', '110000', 'Москва',
                  'Инженер', 'Ответственность']
        for i in range(len(lst)):
            self.assertEqual(pdf_report.DataSet.remove_tags(lst[i]), lstCor[i])


class TableFilterTest(TestCase):
    def testexpFilter(self):
        filter = 'Опыт работы: От 3 до 6 лет'
        equal_data = [{'name': 'DevOps/Системный администратор',
                       'experience_id': 'От 3 до 6 лет', 'premium': 'Нет', 'employer_name': 'ИИТ',
                       'salary_from': '150000 - 350000 (Рубли) (С вычетом налогов)', 'area_name': 'Москва',
                       'published_at': '2022-06-27T17:54:01+0300'}]
        self.assertEqual(table_report.InputConnect.do_filter(lst_vac, filter), equal_data)

    def testareaFilter(self):
        filter = 'Название региона: Москва'
        equal_data = [{'name': 'DevOps/Системный администратор',
                       'experience_id': 'От 3 до 6 лет', 'premium': 'Нет', 'employer_name': 'ИИТ',
                       'salary_from': '150000 - 350000 (Рубли) (С вычетом налогов)', 'area_name': 'Москва',
                       'published_at': '2022-06-27T17:54:01+0300'}]
        self.assertEqual(table_report.InputConnect.do_filter(lst_vac, filter), equal_data)

    def testpremiumFilter(self):
        filter = 'Премиум-вакансия: Нет'
        equal_data = [{'name': 'Web-программист',
                       'experience_id': 'Нет опыта', 'premium': 'Нет', 'employer_name': 'Асташенков Г. А.',
                       'salary_from': '30000 - 80000 (Рубли) (С вычетом налогов)', 'area_name': 'Ульяновск',
                       'published_at': '2022-05-31T17:32:31+0300'},
                      {'name': 'Junior+/ Middle Python разработчик',
                       'experience_id': 'От 1 года до 3 лет',
                       'premium': 'Нет', 'employer_name': 'CiPlay',
                       'salary_from': '40000 - 80000 (Рубли) (С вычетом налогов)',
                       'area_name': 'Санкт-Петербург',
                       'published_at': '2022-05-31T17:44:23+0300'},
                      {'name': 'DevOps/Системный администратор',
                       'experience_id': 'От 3 до 6 лет', 'premium': 'Нет', 'employer_name': 'ИИТ',
                       'salary_from': '150000 - 350000 (Рубли) (С вычетом налогов)', 'area_name': 'Москва',
                       'published_at': '2022-06-27T17:54:01+0300'}]
        self.assertEqual(table_report.InputConnect.do_filter(lst_vac, filter), equal_data)
