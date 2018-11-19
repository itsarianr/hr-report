import os
import sys
import pandas as pd
from shamsi_date import Date


CATEGORY_DURATIONS = {}
TOTAL_DAYS_COUNT = 0


def get_date_range():
    try:
        return sys.argv[1], sys.argv[2]
    except:
        raise 'Please enter date range!'


def read_durations_from_file_by_date(date):
    reports_directory = os.fsencode(date.get_directory_path())
    if not os.path.isdir(reports_directory):
        return
    global TOTAL_DAYS_COUNT
    TOTAL_DAYS_COUNT += 1
    for report in os.listdir(reports_directory):
        report_path = os.path.join(
            date.get_directory_path(), os.fsdecode(report))
        sheet = pd.read_excel(report_path, sheet_name="Daily")
        for index, category in enumerate(sheet.iloc[:, 2]):
            if type(category) is float:
                break
            if category not in CATEGORY_DURATIONS:
                CATEGORY_DURATIONS[category] = 0
            duration = sheet.iloc[:, 3][index]
            CATEGORY_DURATIONS[category] += duration


def read_durations_in_date_range(str_start_date, str_end_date):
    date = Date(str_start_date)
    end_date = Date(str_end_date)
    should_continue = True
    while should_continue:
        if date.equals(end_date):
            should_continue = False
        read_durations_from_file_by_date(date)
        date = date.get_tommorow()


def generate_categories_report(str_start_date, str_end_date):
    read_durations_in_date_range(str_start_date, str_end_date)
    total_duration = 0
    for category, duration in CATEGORY_DURATIONS.items():
        total_duration += duration
    category_percentages = {}
    output_report = open(str_start_date + '~' + str_end_date + '.txt',
                         'w', encoding='utf-8')
    sorted_category_durations = sorted(
        CATEGORY_DURATIONS.items(), key=lambda x: x[1], reverse=True)
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


str_start, str_end = get_date_range()
generate_categories_report(str_start, str_end)
print('Done!')
