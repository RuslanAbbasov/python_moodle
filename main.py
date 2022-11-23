import pdf_report
import table_report


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
