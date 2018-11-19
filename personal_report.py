import os
import pandas as pd
from shamsi_date import Date


PERSON_TASKS = []
PERSON_CATEGORIES_DURATIONS = {}
TOTAL_DAYS_COUNT = 0


def read_person_tasks_by_date(person_name, date):
    reports_directory = os.fsencode(date.get_directory_path())
    if not os.path.isdir(reports_directory):
        return
    global TOTAL_DAYS_COUNT
    TOTAL_DAYS_COUNT += 1
    for report in os.listdir(reports_directory):
        if os.fsdecode(report).startswith(person_name):
            report_path = os.path.join(
                date.get_directory_path(), os.fsdecode(report))
            sheet = pd.read_excel(report_path, sheet_name="Daily")
            for index, category in enumerate(sheet.iloc[:, 2]):
                if type(category) is float:
                    break
                duration = sheet.iloc[:, 3][index]
                PERSON_TASKS.append({
                    'date': date.get_str(),
                    'title': sheet.iloc[:, 1][index],
                    'category': category,
                    'duration': duration,
                    'description': sheet.iloc[:, 4][index],
                })
                if category not in PERSON_CATEGORIES_DURATIONS:
                    PERSON_CATEGORIES_DURATIONS[category] = 0
                PERSON_CATEGORIES_DURATIONS[category] += duration


def read_person_tasks_in_date_range(person_name, str_start_date, str_end_date):
    date = Date(str_start_date)
    end_date = Date(str_end_date)
    should_continue = True
    while should_continue:
        if date.equals(end_date):
            should_continue = False
        read_person_tasks_by_date(person_name, date)
        date = date.get_tommorow()


def generate_personal_report(person_name, str_start_date, str_end_date):
    read_person_tasks_in_date_range(person_name, str_start_date, str_end_date)
    output_report = open(person_name + ' (' + str_start_date + '~' + str_end_date + ')' + '.txt',
                         'w', encoding='utf-8')
    prev_date = ''
    for task in PERSON_TASKS:
        if prev_date != task['date']:
            output_report.write('=========\n' + task['date'] + '\n=========\n')
            prev_date = task['date']
        output_report.write(str(task['title']) + '\n' + str(task['category']) +
                            '\n' + str(task['duration']) + '\n' + str(task['description']) + '\n--------------------------------------------\n')
    output_report.write('============================================\n\n')
    total_duration = 0
    for category, duration in PERSON_CATEGORIES_DURATIONS.items():
        total_duration += duration
    category_percentages = {}
    sorted_category_durations = sorted(
        PERSON_CATEGORIES_DURATIONS.items(), key=lambda x: x[1], reverse=True)
    for category_duration in sorted_category_durations:
        category_percentages[category_duration[0]] = (
            category_duration[1] * 100 / total_duration).round()
        str_category = category_duration[0]
        if category_duration[0] == 'سایر':
            str_category = 'Other'
        if category_duration[0] == 'آموزش':
            str_category = 'Education'
        output_report.write(
            str_category + ': ' + str(int(category_percentages[category_duration[0]])) + '% (' + str(int(category_duration[1] / 60)) + ' Hours)\n')
    output_report.write('=' * 25 + '\n')
    output_report.write('SUM: ' + str(int(total_duration / 60)) +
                        ' Hours in ' + str(TOTAL_DAYS_COUNT) + ' days.')
