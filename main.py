import os
import pandas as pd
from shamsi_date import Date


str_start = '97-07-28'
str_end = '97-08-06'
CATEGORIES = {}


def calculate_by_date(date):
    directory = os.fsencode(date.get_directory_path())
    if not os.path.isdir(directory):
        return
    # print('==> ' + date.get_str())
    for file in os.listdir(directory):
        file_path = os.path.join(date.get_directory_path(), os.fsdecode(file))
        sheet = pd.read_excel(file_path, sheet_name="Daily")
        for index, category in enumerate(sheet.iloc[:, 2]):
            if type(category) is float:
                break
            time = sheet.iloc[:, 3][index]
            if category not in CATEGORIES:
                CATEGORIES[category] = 0
            CATEGORIES[category] += time


date = Date(str_start)
end_date = Date(str_end)
should_continue = True
while should_continue:
    if date.equals(end_date):
        should_continue = False
    calculate_by_date(date)
    date = date.get_tommorow()

sum = 0
for category, time in CATEGORIES.items():
    sum += time
CATEGORY_PERCENTAGES = {}
output = open(str_start + '~' + str_end + '.out', 'w', encoding='utf-8')
for category, time in CATEGORIES.items():
    CATEGORY_PERCENTAGES[category] = (time * 100 / sum).round()
    str_category = category
    if category == 'سایر':
        str_category = 'Other'
    if category == 'آموزش':
        str_category = 'Education'
    output.write(
        str_category + ': ' + str(int(CATEGORY_PERCENTAGES[category])) + '% (' + str('{:,}'.format(int(CATEGORIES[category]))) + ' Hours)\n')
output.write('=' * 30 + '\n')
output.write('SUM: ' + str('{:,}'.format(int(sum))) + ' Hours')
