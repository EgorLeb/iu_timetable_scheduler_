from src.input_parsing.parser_algorithm import InputParser
from src.output_formatting.output_algorithms import parametrized, create_xlsx


class ErrorOfCreation(Exception):
    """
    Raise when algorithm can't create the schedule
    """

    def __init__(self):
        super().__init__("Algorithm can't create the schedule")


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

    def getCourses(type):
        coursesOfYear = dict(
            filter(lambda x: x[1].get_type() == type, courses.items()))
        info = []
        for i in coursesOfYear:
            info.append([i, course_groups[i]])
            tas = []
            for j in ta_capacity:
                if i in ta_capacity[j]:
                    tas.append(j)
            info[-1].append(tas)
        info.sort(key=lambda x: len(x[1]), reverse=True)
        return info, coursesOfYear

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

    infoG, coursesOfYearG = getCourses("Full")

    week_busy_tmp = {
        "Mon": [],
        "Tue": [],
        "Wed": [],
        "Thu": [],
        "Fri": [],
        "Sat": [],
        "Sun": []
    }

    ind_of_online = 1

    def createBlock(ind, info, coursesOfYear, week_busy):
        nonlocal sport_days
        if ind == len(info):
            yield week_busy
            return
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
                res = createBlock(ind + 1, info, coursesOfYear, week_busy)
                for r in res:
                    yield week_busy
                week_busy[s] = week_busy[s][:-1]

    generalCourses = createBlock(0, infoG, coursesOfYearG, week_busy_tmp)
    sort_rooms = list(rooms)
    sort_rooms.sort(key=lambda x: rooms[x].room_capacity, reverse=True)
    week1 = createEmptyWeek(sport_days, rooms)
    week2 = createEmptyWeek(sport_days, rooms)

    infoBlock1, coursesOfYearBlock1 = getCourses("Block 1")
    infoBlock2, coursesOfYearBlock2 = getCourses("Block 2")

    for G in generalCourses:
        week_busy_save2 = {
            "Mon": [],
            "Tue": [],
            "Wed": [],
            "Thu": [],
            "Fri": [],
            "Sat": [],
            "Sun": []
        }
        for i in week_busy_save2:
            for k in G[i]:
                week_busy_save2[i].append(k)
        B2 = createBlock(0, infoBlock2, dict(list(coursesOfYearBlock2.items()) + list(coursesOfYearG.items())),
                         week_busy_save2)
        for b2 in B2:
            print(2)
            week_busy_save = {
                "Mon": [],
                "Tue": [],
                "Wed": [],
                "Thu": [],
                "Fri": [],
                "Sat": [],
                "Sun": []
            }
            for i in week_busy_save:
                for k in G[i]:
                    week_busy_save[i].append(k)
            B1 = createBlock(0, infoBlock1, dict(list(coursesOfYearBlock1.items()) + list(coursesOfYearG.items())),
                             week_busy_save)
            for b1 in B1:
                q = []
                for i in b1:
                    week_busy = b1
                    ind_free_room = 0
                    a = week_busy[i]
                    a.sort(key=lambda x: len(x[1]), reverse=True)
                    for k in a:
                        l = 0
                        if courses[k[0]]._study_format == "Offline":
                            week1[i][0][sort_rooms[ind_free_room]] = [k[0] + ' (lec)', courses[k[0]]._teacher._name,
                                                                      k[1]]
                        else:
                            week1[i][0][f"online {ind_of_online}"] = [k[0] + ' (lec)', courses[k[0]]._teacher._name,
                                                                      k[1]]
                            ind_of_online += 1
                        if k[0] in tutors:
                            l = 1
                            if tutors[k[0]]._study_format == "Offline":
                                week1[i][1][sort_rooms[ind_free_room]] = [k[0] + ' (tut)', tutors[k[0]]._teacher._name,
                                                                          k[1]]
                            else:
                                week1[i][1][f"online {ind_of_online}"] = [k[0] + ' (tut)', tutors[k[0]]._teacher._name,
                                                                          k[1]]
                                ind_of_online += 1
                        ind_free_room += 1
                        ind_of_group = 0
                        for j in k[2]:
                            if i in j.get_preferences() or len(j.get_preferences()) == 0:
                                for d in range(min(2, ta_capacity[j][k[0]])):
                                    m = 100000
                                    minimum_room = ''
                                    for t in sort_rooms:
                                        if week1[i][1 + d + l][t] is None and \
                                                m > rooms[t].room_capacity >= groups[k[1][ind_of_group]]._people_number:
                                            m = rooms[t].room_capacity
                                            minimum_room = t
                                    if minimum_room != '':
                                        week1[i][1 + d + l][minimum_room] = [k[0] + ' (lab)', j._name, [k[1][ind_of_group]]]
                                        if k[0] in coursesOfYearBlock1:
                                            q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                        ind_of_group += 1
                                    else:
                                        q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                        if k[0] in coursesOfYearBlock1:
                                            q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                for d in range(2, ta_capacity[j][k[0]]):
                                    q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                    ind_of_group += 1
                            else:
                                for d in range(ta_capacity[j][k[0]]):
                                    q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                    ind_of_group += 1
                for i in q:
                    for j in (set(list(createEmptyWeek(sport_days, rooms))) - {"Sun", "Sat"} if len(
                            i[1].get_preferences()) == 0 else i[1].get_preferences()):
                        for k in range(2, len(week1[j])):
                            flag = True
                            for l in week1[j][k]:
                                if week1[j][k][l] is not None and (
                                        i[2].get_name() in week1[j][k][l][2] or week1[j][k][l][1] == i[1]._name):
                                    flag = False
                            if flag:
                                for l in week1[j][k]:
                                    if week1[j][k][l] is None and rooms[l].room_capacity >= i[2].get_people_number():
                                        week1[j][k][l] = [i[0]._course_name + ' (lab)', i[1]._name,
                                                          [i[2].get_name()]]
                                        break
                                else:
                                    continue
                                break
                        else:
                            continue
                        break
                    else:
                        print("Что-то не добавилось(")

                q = []
                for i in b2:
                    week_busy = b2
                    ind_free_room = 0
                    a = week_busy[i]
                    a.sort(key=lambda x: len(x[1]), reverse=True)
                    for k in a:
                        l = 0
                        if courses[k[0]]._study_format == "Offline":
                            week2[i][0][sort_rooms[ind_free_room]] = [k[0] + ' (lec)', courses[k[0]]._teacher._name,
                                                                      k[1]]
                        else:
                            week2[i][0][f"online {ind_of_online}"] = [k[0] + ' (lec)', courses[k[0]]._teacher._name,
                                                                      k[1]]
                            ind_of_online += 1
                        if k[0] in tutors:
                            l = 1
                            if tutors[k[0]]._study_format == "Offline":
                                week2[i][1][sort_rooms[ind_free_room]] = [k[0] + ' (tut)', tutors[k[0]]._teacher._name,
                                                                          k[1]]
                            else:
                                week2[i][1][f"online {ind_of_online}"] = [k[0] + ' (tut)', tutors[k[0]]._teacher._name,
                                                                          k[1]]
                                ind_of_online += 1
                        ind_free_room += 1
                        ind_of_group = 0
                        for j in k[2]:
                            for d in range(min(2, ta_capacity[j][k[0]])):
                                m = 100000
                                minimum_room = ''
                                for t in sort_rooms:
                                    if week2[i][1 + d + l][t] is None and m > rooms[t].room_capacity >= groups[
                                        k[1][ind_of_group]]._people_number:
                                        m = rooms[t].room_capacity
                                        minimum_room = t
                                if minimum_room != '':
                                    week2[i][1 + d + l][minimum_room] = [k[0] + ' (lab)', j._name, [k[1][ind_of_group]]]
                                    if k[0] in coursesOfYearBlock2:
                                        q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                    ind_of_group += 1
                                else:
                                    q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                    if k[0] in coursesOfYearBlock2:
                                        q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                            for d in range(2, ta_capacity[j][k[0]]):
                                q.append([courses[k[0]], j, groups[k[1][ind_of_group]], i])
                                ind_of_group += 1
                for i in q:
                    for j in (set(list(createEmptyWeek(sport_days, rooms))) - {"Sun", "Sat"} if len(
                            i[1].get_preferences()) == 0 else i[1].get_preferences()):
                        for k in range(2, len(week2[j])):
                            flag = True
                            for l in week2[j][k]:
                                if week2[j][k][l] is not None and (
                                        i[2].get_name() in week2[j][k][l][2] or week2[j][k][l][1] == i[1]._name):
                                    flag = False
                            if flag:
                                for l in week2[j][k]:
                                    if week2[j][k][l] is None and rooms[l].room_capacity >= i[2].get_people_number():
                                        week2[j][k][l] = [i[0]._course_name + ' (lab)', i[1]._name, [i[2].get_name()]]
                                        break
                                else:
                                    continue
                                break
                        else:
                            continue
                        break
                    else:
                        print("Что-то не добавилось(")

                break
            else:
                continue
            break
        else:
            continue
        break
    else:
        raise ErrorOfCreation()

    for i in sport_days:
        week2[i].insert(0, {'Sport Complex': ["Sport", "Electives", [x for x in groups if "B" in x]]})
    for i in sport_days:
        week1[i].insert(0, {'Sport Complex': ["Sport", "Electives", [x for x in groups if "B" in x]]})
    print(321)
    return week1, week2, tuple(x for x in groups)


week1, week2, groups = get_schedule()
create_xlsx(parametrized(week1), parametrized(week2), groups)
