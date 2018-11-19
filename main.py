import sys
import total_report
import personal_report


def get_report_type():
    return sys.argv[1]


report_type = get_report_type()
if report_type == 'team':
    str_start_date, str_end_date = sys.argv[2], sys.argv[3]
    total_report.generate_categories_report(str_start_date, str_end_date)
elif report_type == 'personal':
    person_name = sys.argv[2]
    str_start_date, str_end_date = sys.argv[3], sys.argv[4]
    personal_report.generate_personal_report(person_name,
                                             str_start_date, str_end_date)
print('Done!')
