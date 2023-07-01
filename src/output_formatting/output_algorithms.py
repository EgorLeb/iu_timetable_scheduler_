from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font


WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
YEARS = ('B22', 'В21', 'B20', 'B19')
PERIODS = ("9:00-10:30", "10:40-12:10", "12:40-14:10", "14:20-15:50", "16:00-17:30", "17:40-19:00")


def parametrized(week):
    result = dict()
    # format: (weekday, class_number, group_name) -> (room_number, class_name, instructor)
    for weekday in WEEKDAYS:
        for class_number in range(len(week[weekday])):
            for room_number in week[weekday][class_number].keys():
                slot = week[weekday][class_number][room_number]
                if slot is None:
                    continue
                class_name = slot[0]
                instructor = slot[1]
                groups_list = slot[2]
                for group_name in groups_list:
                    result[(weekday, class_number, group_name)] = (room_number, class_name, instructor)
    return result

# week format: (weekday, class_number, group_name) -> (room_number, class_name, instructor)
def create_xlsx(week, groups):
    wb = Workbook()
    for year in YEARS:
        year_groups = list(filter(lambda x: x.startswith(year), groups))
        entries = list(filter(lambda x: x[2] in year_groups, week.keys()))
        year_sheet = wb.create_sheet(year)

        for column_number, group in enumerate(sorted(year_groups), 2):
            year_sheet.cell(row=1, column=column_number, value=group)
        for weekday in WEEKDAYS:
            year_sheet.cell(row=get_row_offset(weekday, 0), column=1, value=weekday)
            for class_number in range(0, 6):
                year_sheet.cell(row=get_row_offset(weekday, class_number) + 2, column=1,
                                value=PERIODS[class_number])

        for slot in entries:
            weekday = slot[0]
            class_number = slot[1]
            column_number = sorted(year_groups).index(slot[2]) + 2
            row_number = get_row_offset(weekday, class_number)
            room_number = week[slot][0]
            year_sheet.cell(row=row_number + 3, column=column_number, value=room_number)
            class_name = week[slot][1]
            year_sheet.cell(row=row_number + 1, column=column_number, value=class_name)
            instructor = week[slot][2]
            year_sheet.cell(row=row_number + 2, column=column_number, value=instructor)

        prettify(year_sheet, len(year_groups))
    wb.save("schedule.xlsx")


def get_row_offset(weekday, class_number):
    weekday_number = WEEKDAYS.index(weekday)
    return 1 + weekday_number * 19 + 1 + class_number * 3


def prettify(sheet, number_of_groups):
    # formatting the whole table
    alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:1+number_of_groups]:
        sheet.column_dimensions[letter].auto_size = True
        sheet.column_dimensions[letter].width += 1
        for row in range(1, get_row_offset("Sun", 6) + 4):
            sheet[letter + str(row)].alignment = alignment

    # formatting group names
    font = Font(bold=True)
    fill = PatternFill(fill_type="darkGrid", start_color="00AA00", end_color="00AA00")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:1+number_of_groups]:
        sheet[letter + "1"].font = font
        sheet[letter + "1"].fill = fill

    # formatting weekday delimiters
    font = Font(bold=True)
    fill = PatternFill(fill_type="solid", start_color="22FF22", end_color="22FF22")
    for weekday in WEEKDAYS:
        row = str(get_row_offset(weekday, 0))
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:1 + number_of_groups]:
            sheet[letter + row].font = font
            sheet[letter + row].fill = fill

    # formatting class periods
    sheet.column_dimensions["A"].width = 10

    # formatting inner tables