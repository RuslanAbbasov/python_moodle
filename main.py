import pdf_report
import table_report

"""
Файл main.py, реализующий выбор функциональности программы.

Файл имеет метод main, который и реализует работу.
"""


def main():
    """"
    Вызываемый метод, который получает команду от пользователя (-Вакансии- или -Статистика-).

    Ввод сразу опускает строку до нижнего регистра и исключает многочисленные пробелы
    """
    command = "".join(input(
        'Введите, что вы желаете получить\n  -Вакансии- или -Статистика-\nПоле для ввода:'
    ).lower().split())
    print(command)
    if command == 'вакансии':
        table_report.InputConnect()
    elif command == 'статистика':
        pdf_report.InputConnect()
    else:
        print('Вы ввели некорректные данные\nНеобходимо ввести\n-Вакансии- или -Статистика-')


if __name__ == '__main__':
    import doctest

    main()
    doctest.testmod()
