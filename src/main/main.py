from src.input_parsing.parser_algorithm import InputParser
from src.output_formatting.output_algorithms import parametrized, create_xlsx


def get_schedule():
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

    coursesOfYear = dict(filter(lambda x: x[1]._study_year in (1, 2), courses.items()))

    info = []
    for i in coursesOfYear:
        info.append([i, course_groups[i]])
        tas = []
        for j in ta_capacity:
            if i in ta_capacity[j]:
                tas.append(j)
        info[-1].append(tas)

    info.sort(key=lambda x: len(x[1]), reverse=True)

    week_busy = {
        "Mon": [],
        "Tue": [],
        "Wed": [],
        "Thu": [],
        "Fri": [],
        "Sat": [],
        "Sun": []
    }

    def secondYear(ind):
        nonlocal week_busy, info
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
    printDict(week_busy)

    sort_rooms = list(rooms)
    sort_rooms.sort(key=lambda x: rooms[x].room_capacity, reverse=True)
    if flag_of_algorithm:
        week = createEmptyWeek(sport_days, rooms)
        for i in week_busy:
            ind_free_room = 0
            a = week_busy[i]
            a.sort(key=lambda x: len(x[1]), reverse=True)
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
    return week, tuple(x for x in groups)

week, groups = get_schedule()
create_xlsx(parametrized(week), groups)