from src.input_parsing.parser_algorithm import InputParser


def createEmptyWeek(sport, rooms):
    week = {
        "Mon": [dict([(j, None) for j in rooms]) for i in range(6)],
        "Tue": [dict([(j, None) for j in rooms]) for i in range(6)],
        "Wed": [dict([(j, None) for j in rooms]) for i in range(6)],
        "Thu": [dict([(j, None) for j in rooms]) for i in range(6)],
        "Fri": [dict([(j, None) for j in rooms]) for i in range(6)],
        "Sat": [dict([(j, None) for j in rooms]) for i in range(6)],
        "Sun": [dict([(j, None) for j in rooms]) for i in range(6)],
    }
    for i in sport:
        week[i] = week[i][1:]
    return week


def chooseWeekCourses(weekCourses, dayInd=0, week=(), maxDay=7):
    if len(list(filter(lambda x: type(x) is not str, week))) == len(year_courses):
        return week
    if dayInd == maxDay:
        return None
    week = list(week) + ['0']
    if dayInd <= 6:
        for i in weekCourses[day_of_week[dayInd]]:
            if i not in week or type(i) is str:
                week[-1] = i
                res = chooseWeekCourses(weekCourses, dayInd + 1, tuple(week.copy()), maxDay=maxDay)
                if res is not None:
                    return res
    return None


parse = InputParser()
print("start my program")
groups = parse.get_groups()
sport_days = parse.get_sport_days()
labs = parse.get_labs()
courses = parse.get_lectures()
teachers = parse.get_teachers()
rooms = parse.get_rooms()
tutors = parse.get_tutorials()

day_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

years = dict()
for i in groups:
    years[i.split('-')[0]] = []

for i in years:
    years[i] = list(filter(lambda x: i == x.split('-')[0], list(groups)))

schedule = createEmptyWeek(sport_days, rooms)
# print(schedule)
year_courses = dict(filter(lambda x: x[1]._study_year == 1, courses.items()))
# for i in year_courses:
#     print(year_courses[i]._teacher, teachers[year_courses[i]._teacher._name].get_preferences())

week_busy = {
    "Mon": ["nothing, string for algorithm"],
    "Tue": ["nothing, string for algorithm"],
    "Wed": ["nothing, string for algorithm"],
    "Thu": ["nothing, string for algorithm"],
    "Fri": ["nothing, string for algorithm"],
    "Sat": ["nothing, string for algorithm"],
    "Sun": ["nothing, string for algorithm"]
}

for i in week_busy:
    for j in year_courses:
        if i in teachers[year_courses[j]._teacher._name].get_preferences():
            week_busy[i].insert(0, year_courses[j])

max_day = 8
m = chooseWeekCourses(week_busy, maxDay=max_day)
while m is not None:
    max_day -= 1
    m = chooseWeekCourses(week_busy, maxDay=max_day)
max_day += 1
m = chooseWeekCourses(week_busy, maxDay=max_day) + (None, None, None, None, None, None)
# print(m)
cn = 0
for i in m:
    cn += 1
    if type(i) is not str and i is not None:
        print(cn, i._teacher._name, i._course_name)

find_biggest_room = max(rooms, key=lambda x: rooms[x].room_capacity * (schedule["Mon"][0][x] is None))

for i in schedule:
    # print(i, day_of_week.index(i))
    if m[day_of_week.index(i)] is not None and type(m[day_of_week.index(i)]) is not str:
        schedule[i][0][find_biggest_room] = [m[day_of_week.index(i)], m[day_of_week.index(i)]._teacher._name,
                                             list(groups)]
        if m[day_of_week.index(i)]._course_name in tutors:
            schedule[i][1][find_biggest_room] = [tutors[m[day_of_week.index(i)]._course_name],
                                                 tutors[m[day_of_week.index(i)]._course_name]._teacher._name,
                                                 list(groups)]


print(schedule)
