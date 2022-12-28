import requests
import datetime
from datetime import datetime


def get_group_table(group_number, user_choice, day):
    etu_group = "https://digital.etu.ru/api/general/dicts/groups?scheduleId=publicated&withFaculty=true&withSemesterSeasons=true&withFlows=true"
    r_group = requests.get(etu_group)

    week_number = datetime.today().isocalendar()[1]
    if week_number % 2 == 1:
        week = '1'
    else:
        week = '2'

    i = 0
    while group_number != str(r_group.json()[i]["fullNumber"]):
        i = i + 1
    group_id = str(r_group.json()[i]["id"])

    etu_table = "https://digital.etu.ru/api/schedule/objects/publicated?groups=" + group_id + "&withSubjectCode=true&withURL=true"
    r_table = requests.get(etu_table)

    answer = ''

    if user_choice == 1:
        today_lesson(r_table, week)
    elif user_choice == 2:
        answer = certain_day_lesson(r_table, week, day, answer)
    elif user_choice == 3:
        answer = next_day_lesson(r_table, week, answer)
    elif user_choice == 4:
        answer = certain_day_lesson(r_table, week, day, answer)

    return answer


def today_lesson(r_table, week):
    day = ''
    week_day: int = datetime.today().isoweekday()
    if week_day == 1:
        day = "MON"
    elif week_day == 2:
        day = "TUE"
    elif week_day == 3:
        day = "WED"
    elif week_day == 4:
        day = "THU"
    elif week_day == 5:
        day = "FRI"
    elif week_day == 6:
        day = "SAT"

    answer = certain_day_lesson(r_table, week, day, answer)
    return answer


def certain_day_lesson(r_table, week, day, answer):
    free_day = 1
    for i in range(30):
        if day == str(r_table.json()[0]["scheduleObjects"][i]['lesson']['auditoriumReservation']['reservationTime'][
                          'weekDay']) and week == str(
            r_table.json()[0]["scheduleObjects"][i]['lesson']['auditoriumReservation']['reservationTime']['week']):
            free_day = 0
            answer = answer + "\n\nНазвание предмета: " + str(
                r_table.json()[0]["scheduleObjects"][i]['lesson']["subject"]['title'])
            answer = answer + "\nТип предмета: " + str(
                r_table.json()[0]["scheduleObjects"][i]['lesson']["subject"]['subjectType'])
            try:
                answer = answer + "\nФИО преподавателя: " + str(
                    r_table.json()[0]["scheduleObjects"][i]['lesson']["teacher"]['initials'])
            except:
                answer = answer + "\nФИО преподавателя: Преподаватель в расписании отсутсвует"
            try:
                answer = answer + "\nНомер вудитории: " + str(
                    r_table.json()[0]["scheduleObjects"][i]['lesson']['auditoriumReservation']['auditorium'][
                        'number'])
            except:
                answer = answer + "\nНомер вудитории: Аудитория в расписании отсутсвует"

    if free_day == 1:
        answer = "Занятий нет"
    return answer


def next_day_lesson(r_table, week, answer):
    day = ''
    week_day: int = datetime.today().isoweekday() + 1
    if week_day == 1:
        day = "MON"
    elif week_day == 2:
        day = "TUE"
    elif week_day == 3:
        day = "WED"
    elif week_day == 4:
        day = "THU"
    elif week_day == 5:
        day = "FRI"
    elif week_day == 6:
        day = "SAT"

    answer = certain_day_lesson(r_table, week, day, answer)
    return answer
