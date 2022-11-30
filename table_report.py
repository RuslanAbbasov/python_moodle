import csv
from datetime import datetime
import math
import re
import prettytable
from prettytable import PrettyTable


class CommonTools:
    """Класс с вспомогательными методами

    """
    rus_names = {'Название': 'name', 'Описание': 'description', 'Навыки': 'key_skills', 'Опыт работы': 'experience_id',
                 'Премиум-вакансия': 'premium', 'Компания': 'employer_name', 'Оклад': 'salary_from',
                 'Верхняя граница вилки оклада': 'salary_to', 'Оклад указан до вычета налогов': 'salary_gross',
                 'Идентификатор валюты оклада': 'salary_currency', 'Название региона': 'area_name',
                 'Дата публикации вакансии': 'published_at'}

    rus_true_false = {'True': 'Да', 'False': 'Нет'}

    @staticmethod
    def exit_with_print(line):
        """Выход из программы после печати ошибки

        :param line:
        """
        print(line)
        exit()

    @staticmethod
    def edit_line(line):
        """Фильтрация строки от html тегов и '\n', так же переводит 'True' и 'False'

        :param line: (str)
        :return: string (str)
        """
        string = re.sub(r'<[^>]+>', '', line)
        if '\n' not in string:
            string = ' '.join(string.split())
        if string == 'True' or string == 'False':
            string = CommonTools.rus_true_false[string]
        return string


class Salary:
    """Класс для представления зарплаты

    Attribute:
        salary_from(str): Нижняя граница вилки оклада
        salary_to(str): Верхняя граница вилки оклада
        salary_gross(str): Оклад указан до вычета налогов
        salary_currency(str): Идентификатор валюты оклада
    """
    currency_to_rub = {
        "Манаты": 35.68, "Белорусские рубли": 23.91, "Евро": 59.90, "Грузинский лари": 21.74, "Киргизский сом": 0.76,
        "Тенге": 0.13, "Рубли": 1, "Гривны": 1.64, "Доллары": 60.66, "Узбекский сум": 0.0055}

    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """Инициализирует объект Salary

        :param salary_from: (str): Нижняя граница вилки оклада
        :param salary_to: (str): Верхняя граница вилки оклада
        :param salary_gross: (str): Оклад указан до вычета налогов
        :param salary_currency: (str): Идентификатор валюты оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    @staticmethod
    def currency_translate(salary_from, salary_to, salary_currency):
        """Переводит зарплату в рубли

        :param salary_from: (str): Нижняя граница вилки оклада
        :param salary_to: (str): Верхняя граница вилки оклада
        :param salary_currency: (str): Идентификатор валюты оклада
        :return:
            salary_from(str): Нижняя граница вилки оклада
            salary_to(str): Верхняя граница вилки оклада
        """
        salary_from = int(math.trunc(float(salary_from))) * Salary.currency_to_rub[salary_currency]
        salary_to = int(math.trunc(float(salary_to))) * Salary.currency_to_rub[salary_currency]
        return salary_from, salary_to


class Vacancy:
    """Класс для представления вакансии

    Attribute:
        name(str): название вакансии
        description(str): описание
        key_skills(str): Навыки
        experience_id(str): Опыт работы
        premium(str): Премиум-вакансия
        employer_name(str): Компания
        salary(str): Зарплата
        area_name(str): Местонахождение
        published_at(str): Дата публикации
    """
    experience_rus = {'noExperience': 'Нет опыта',
                      'between1And3': 'От 1 года до 3 лет',
                      'between3And6': 'От 3 до 6 лет',
                      'moreThan6': 'Более 6 лет'}

    def __init__(self, dictionary):
        """ Инициализация объекта Vacancy

        :param dictionary: (dict) словарь вакансии
        """
        self.name = dictionary['name']
        self.description = dictionary['description']
        self.key_skills = dictionary['key_skills']
        self.experience_id = Vacancy.experience_rus[dictionary['experience_id']]
        self.premium = dictionary['premium']
        self.employer_name = dictionary['employer_name']
        self.salary = Salary(dictionary['salary_from'], dictionary['salary_to'], dictionary['salary_gross'],
                             dictionary['salary_currency'])
        self.area_name = dictionary['area_name']
        self.published_at = dictionary['published_at']


class DataSet:
    """Класс для составления списка вакансий

    Attribute:
        file_name(str): имя файла
        vacancies_objects(list[Vacancy]): датасет вакансий
    """
    def __init__(self, file_name):
        """Инициализирует объект DataSet

        :param file_name: (str): имя файла
        """
        self.file_name = file_name
        data_tuple = DataSet.read_csv(file_name)
        resume_dict = DataSet.csv_filter(data_tuple[0], data_tuple[1])
        vacancies_objects = []
        for dictionary in resume_dict:
            vacancies_objects.append(Vacancy(dictionary))
        self.vacancies_objects = vacancies_objects

    @staticmethod
    def read_csv(file_name):
        """парсит csv файл и проверяет ег на пустоту или отсутствие данных

        :param file_name:(str): имя файла
        :return: vacancies, columns (tuple[list]): кортеж из списка названий колонок и списка данных о вакансиях
        """
        reader_csv = csv.reader(open(file_name, encoding='utf_8_sig'))
        list_data = [x for x in reader_csv]
        if len(list_data) == 0:
            CommonTools.exit_with_print("Пустой файл")
        if len(list_data) == 1:
            CommonTools.exit_with_print("Нет данных")
        columns = list_data[0]
        vacancies = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
        return vacancies, columns

    @staticmethod
    def csv_filter(reader, list_naming):
        """Обрабатывает данные и преобразует их в список словарей

        :param reader: (list) данные о вакансиях
        :param list_naming: (list) название колонок
        :return: resumes: (list[dict]) список словарей
        """
        resumes = []
        sentences = {}
        for resume in reader:
            for i in range(len(resume)):
                resume[i] = CommonTools.edit_line(resume[i])
                sentences[list_naming[i]] = resume[i]
            resumes.append(sentences.copy())
        return resumes


class InputConnect:
    """Класс для работы с входными данными

    """
    def __init__(self):
        """Реализует вызов методов чтения входных данных,
         создания датасета вакансий и печати таблицы

        """
        params = InputConnect.get_params()
        data_set = DataSet(params[0])
        InputConnect.print_vacancies(data_set, params[1], params[2], params[3], params[4], params[5])

    @staticmethod
    def get_params():
        """Получение входных данных и работа с некорректными данными

        :return: tuple[str] кортеж с входными данными
        """
        file_name = input('Введите название файла: ')
        parameter = input('Введите параметр фильтрации: ')
        sort_parametr = input('Введите параметр сортировки: ')
        reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
        start_end_index = input('Введите диапазон вывода: ').split()
        fields_name = input('Введите требуемые столбцы: ').split(', ')

        if parameter != '' and ': ' not in parameter:
            CommonTools.exit_with_print('Формат ввода некорректен')
        if parameter != '' and parameter.split(': ')[0] not in CommonTools.rus_names:
            CommonTools.exit_with_print('Параметр поиска некорректен')
        if sort_parametr != '' and sort_parametr not in CommonTools.rus_names:
            CommonTools.exit_with_print('Параметр сортировки некорректен')
        if reverse_sort != '' and reverse_sort not in CommonTools.rus_true_false.values():
            CommonTools.exit_with_print('Порядок сортировки задан некорректно')

        return file_name, parameter, sort_parametr, reverse_sort, start_end_index, fields_name

    currency_rus = {'AZN': 'Манаты', 'BYR': 'Белорусские рубли', 'EUR': 'Евро', 'GEL': 'Грузинский лари',
                    'KGS': 'Киргизский сом', 'KZT': 'Тенге', 'RUR': 'Рубли', 'UAH': 'Гривны', 'USD': 'Доллары',
                    'UZS': 'Узбекский сум'}

    @staticmethod
    def salary_format(salary_from, salary_to, salary_gross, salary_currency):
        """Объединение информации о зарплате в строку

        :param salary_from:(str) Нижняя граница оклада
        :param salary_to:(str) Верхняя граница оклада
        :param salary_gross:(str) Оклад указан до вычета налогов
        :param salary_currency:(str) Валюта
        :return: (str) строка, содержащая всю информацию о зарплате
        """
        currency = InputConnect.currency_rus[salary_currency]
        if salary_gross == 'Нет':
            is_gross = 'С вычетом налогов'
        else:
            is_gross = 'Без вычета налогов'
        salary_from = math.trunc(float(salary_from))
        salary_to = math.trunc(float(salary_to))
        return f"{salary_from} - {salary_to} ({currency}) ({is_gross})"


    @staticmethod
    def formatter(row):
        """Форматирует информацию объекта Vacancy и создает из нее словарь

        :param row:(Vacancy) объект класса (Vacancy)
        :return:new_dict(dict[str, str]): словарь вакансии
        """
        new_dict = {}
        dict_names = list(CommonTools.rus_names.values())
        dict_names = dict_names[:7] + dict_names[10:]
        for key in dict_names:
            if key == 'salary_from':
                new_dict[key] = InputConnect.salary_format(row.salary.salary_from, row.salary.salary_to, row.salary.salary_gross,
                                           row.salary.salary_currency)
                continue
            else:
                new_dict[key] = getattr(row, key)
        return new_dict


    @staticmethod
    def do_filter(data, filter_list):
        """Фильтрация данных
        
        :param data: (dict) словарь с данными
        :param filter_list: (list) список параметров фильтрации
        :return: filtered_list (list) список фильтрованных знач
        """
        def for_filter(row):
            """Функция используется функцией do_filter для объекта filter

            :param row:
            :return:
            """
            if filter_list == '':
                return True
            parameter = filter_list.split(': ')
            if parameter[0] == 'Оклад':
                salary = row['salary_from'].split()
                salary_from = salary[0]
                salary_to = salary[2]
                return int(salary_from) <= int(parameter[1]) <= int(salary_to)
            if parameter[0] == 'Идентификатор валюты оклада':
                return row['salary_from'].split()[3].replace('(', '').replace(')', '') == parameter[1]
            if parameter[0] == 'Навыки':
                parameters = parameter[1].split(', ')
                list_skill = row['key_skills'].split('\n')
                k = 0
                for x in parameters:
                    if x in list_skill:
                        k = k + 1
                return k == len(parameters)
            if parameter[0] == 'Дата публикации вакансии':
                return datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y') == parameter[1]
            return row[CommonTools.rus_names[parameter[0]]] == parameter[1]

        filtered_list = list(filter(for_filter, data))
        if not filtered_list:
            CommonTools.exit_with_print('Ничего не найдено')
        return filtered_list

    @staticmethod
    def do_sort(data, sort, reverse):
        """Реализует сортировку по определенному параметру

        :param data: (dict) список с данными
        :param sort: (str) параметр сортировки
        :param reverse: (bool) переворот список
        :return: data: (dict) сортированный список с данными
        """
        is_reverse = False
        if reverse == 'Да':
            is_reverse = True

        experience_sort = {'Нет опыта': 0, 'От 1 года до 3 лет': 1, 'От 3 до 6 лет': 2, 'Более 6 лет': 3}

        def for_sort(row):
            """Функция используется функцией do_sort() для реализации сортировки

            :param row: (dict): Словарь с данными
            :return: (int or str or datetime): Значение для сортировки
            """
            if sort == 'Оклад':
                salary = row['salary_from'].split()
                currency = re.search(r'\((.*?)\)', row['salary_from']).group(1)
                salary_from, salary_to = Salary.currency_translate(salary[0], salary[2], currency)
                return (salary_from + salary_to) / 2
            if sort == 'Навыки':
                skills = row['key_skills'].split('\n')
                return len(skills)
            if sort == 'Дата публикации вакансии':
                return datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z')
            if sort == 'Опыт работы':
                return experience_sort[row['experience_id']]
            return row[CommonTools.rus_names[sort]]

        if sort != '':
            return sorted(data, key=for_sort, reverse=is_reverse)
        else:
            return data


    @staticmethod
    def create_data(data, filter_list, sort, reverse):
        """Создает итоговый список данных с итоговыми правками для печати

        :param data: (DataSet): Набор данных
        :param filter_list: (list): Список с данными для фильтрации
        :param sort: (str): Параметр сортировки
        :param reverse: (bool) переворот список
        :return: sorted_list: (list): итоговый список с данными
        """
        result_list = []
        for i in range(len(data.vacancies_objects)):
            dictionary = InputConnect.formatter(data.vacancies_objects[i])
            result_list.append(dictionary)

        filtered_list = InputConnect.do_filter(result_list, filter_list)
        sorted_list = InputConnect.do_sort(filtered_list, sort, reverse)

        for i in range(len(sorted_list)):
            salary = sorted_list[i]['salary_from'].split()
            salary_from = '{0:,}'.format(int(salary[0])).replace(',', ' ')
            salary_to = '{0:,}'.format(int(salary[2])).replace(',', ' ')
            salary[0] = str(salary_from)
            salary[2] = str(salary_to)
            sorted_list[i]['salary_from'] = ' '.join(salary)
            sorted_list[i]['published_at'] = datetime.strptime(sorted_list[i]['published_at'], '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y')

            new_list = list(sorted_list[i].values())
            for j in range(len(new_list)):
                if len(new_list[j]) > 100:
                    new_list[j] = new_list[j][:100] + '...'
            sorted_list[i] = new_list
            sorted_list[i].insert(0, str(i + 1))
        return sorted_list


    @staticmethod
    def print_vacancies(data_set, filter_list, sort, reverse, indexes, fields_list):
        """Печать данных в таблице

        :param data_set: (DataSet): Набор данных
        :param filter_list: (list): Список с данными для фильтрации
        :param sort: (str): Параметр сортировки
        :param reverse: (bool) переворот список
        :param indexes: (list): Диапазон вывода строк
        :param fields_list:(list): Список колонок, которые нужно вывести
        """
        table = PrettyTable()
        rus_list = list(CommonTools.rus_names.keys())
        table.field_names = ['№'] + rus_list[:7] + rus_list[10:]
        table.align = 'l'
        table.hrules = prettytable.ALL
        table.max_width = 20

        data = InputConnect.create_data(data_set, filter_list, sort, reverse)
        table.add_rows(data)

        try:
            indexes[0] = int(indexes[0]) - 1
            indexes[1] = int(indexes[1]) - 1
        except IndexError:
            if len(indexes) == 0:
                indexes.append(0)
                indexes.append(len(data_set.vacancies_objects))
            if len(indexes) == 1:
                indexes.append(len(data_set.vacancies_objects))

        if fields_list == ['']:
            print(table.get_string(start=indexes[0], end=indexes[1]))
        elif len(fields_list) == 1:
            fields_list.insert(0, '№')
            print(table.get_string(start=indexes[0], end=indexes[1], fields=fields_list))
        else:
            fields_list.insert(0, '№')
            print(table.get_string(start=indexes[0], end=indexes[1], fields=fields_list))