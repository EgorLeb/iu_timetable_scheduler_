from src.input_parsing.parser_algorithm import InputParser


def printDict(d):
    for i in d:
        print(i)
        if type(d[i]) is list:
            print(end='\t')
            print(*d[i], sep='\n\t')
        else:
            print("\t", d[i])


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
courses = parse.get_lectures()
teachers = parse.get_teachers()
rooms = parse.get_rooms()
tutors = parse.get_tutorials()
ta_capacity = parse.get_ta_courses_capacity()
course_groups = parse.get_course_groups_dict()

day_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

years = dict()
for i in groups:
    years[i.split('-')[0]] = []

for i in years:
    years[i] = list(filter(lambda x: i == x.split('-')[0], list(groups)))

schedule = createEmptyWeek(sport_days, rooms)
# print(schedule)
year_courses = dict(filter(lambda x: x[1]._study_year == 1, courses.items()))
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
# cn = 0
# for i in m:
#     cn += 1
#     if type(i) is not str and i is not None:
#         print(cn, i._teacher._name, i._course_name)

find_biggest_room = max(rooms, key=lambda x: rooms[x].room_capacity * (schedule["Mon"][0][x] is None))

for i in schedule:
    if m[day_of_week.index(i)] is not None and type(m[day_of_week.index(i)]) is not str:
        schedule[i][0][find_biggest_room] = [m[day_of_week.index(i)], m[day_of_week.index(i)]._teacher._name,
                                             list(groups)]
        if m[day_of_week.index(i)]._course_name in tutors:
            schedule[i][1][find_biggest_room] = [tutors[m[day_of_week.index(i)]._course_name],
                                                 tutors[m[day_of_week.index(i)]._course_name]._teacher._name,
                                                 list(groups)]

day_ind = 0
for i in m:
    tas = []
    if type(i) is not str and i is not None:
        for j in ta_capacity:
            for k in ta_capacity[j]:
                if k == i._course_name:
                    tas.append([j, ta_capacity[j][k]])

        groupOfYear = years["B22"]
        groupind = 0
        for j in tas:
            indSlot = 2
            for k in range(j[1]):
                freeRoom = ''
                minCap = 100000
                slot = schedule[day_of_week[day_ind]][indSlot]
                for room in slot:
                    if room != '':
                        if slot[room] is None and \
                                minCap > rooms[room].room_capacity >= groups[groupOfYear[groupind]].get_people_number():
                            minCap = rooms[room].room_capacity
                            freeRoom = room
                schedule[day_of_week[day_ind]][indSlot][freeRoom] = [i._course_name, j[0]._name, [groupOfYear[groupind]]]
                groupind += 1
                indSlot += 1
    day_ind += 1


coursesOfYear = dict(filter(lambda x: x[1]._study_year == 2 or x[1]._study_year == 1, courses.items()))

info = []
for i in coursesOfYear:
    info.append([i, course_groups[i]])
    tas = []
    for j in ta_capacity:
        if i in ta_capacity[j]:
            tas.append(j)
    info[-1].append(tas)

info.sort(key=lambda x: len(x[1]), reverse=True)
# print(*info, sep='\n')

week_busy = {
    "Mon": [],
    "Tue": [],
    "Wed": [],
    "Thu": [],
    "Fri": [],
    "Sat": [],
    "Sun": []
}

# print(coursesOfYear)


def secondYear(ind):
    global week_busy, info
    if ind == len(info):
        return True
    course = info[ind][0]
    for s in set(teachers[coursesOfYear[course]._teacher._name]._preferences):
        flag = True
        for i in week_busy[s]:
            #  проверка на то что не совпадают лекции у одного препода в один день
            if coursesOfYear[i[0]]._teacher._name == coursesOfYear[course]._teacher._name:
                flag = False
                break
            for j in info[ind][1]:
                #  проверка на то что нету 2-ух предметов в один день
                if j in i[1]:
                    flag = False
                    break
        if flag:
            week_busy[s].append(info[ind])
            res = secondYear(ind + 1)
            if not res:
                week_busy[s] = week_busy[s][:-1]
            else:
                return True
    return False


flag_of_algorithm = secondYear(0)
# print(flag_of_algorithm)
printDict(week_busy)

sort_rooms = list(rooms)
sort_rooms.sort(key=lambda x: rooms[x].room_capacity, reverse=True)
# print(sort_rooms)
# print(ta_capacity)

if flag_of_algorithm:
    week = createEmptyWeek(sport_days, rooms)

    for i in week_busy:
        ind_free_room = 0
        # print(week_busy[i])
        a = week_busy[i]
        a.sort(key=lambda x: len(x[1]), reverse=True)
        # print(a)

        for k in a:
            week[i][0][sort_rooms[ind_free_room]] = [k[0] + ' (lec)', courses[k[0]]._teacher._name, k[1]]
            if k[0] in tutors:
                week[i][1][sort_rooms[ind_free_room]] = [k[0] + ' (tut)', tutors[k[0]]._teacher._name, k[1]]
            ind_free_room += 1
            ind_of_group = 0
            for j in k[2]:
                for d in range(ta_capacity[j][k[0]]):
                    m = 100000
                    minimum_room = ''
                    for t in sort_rooms:
                        if week[i][2 + d][t] is None and m > rooms[t].room_capacity >= groups[k[1][ind_of_group]]._people_number:
                            m = rooms[t].room_capacity
                            minimum_room = t
                    if minimum_room != '':
                        week[i][2 + d][minimum_room] = [k[0] + ' (lab)', j._name, [k[1][ind_of_group]]]
                        ind_of_group += 1
                    else:
                        print("Any ERROR")
    printDict(week)


# for i in schedule:
#     print(i)
#     print(*schedule[i], sep='\n')
#     print()
#     print()
#     print()
