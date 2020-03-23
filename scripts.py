import os

import random
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

django.setup()

from datacenter.models import Schoolkid, Lesson, Commendation, Chastisement, Mark

all_commendations = [
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
    'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!',
    'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
    'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
    'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!', 'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!', 'Теперь у тебя точно все получится!'
]


def error_catcher(func):
    def wrapper(*args):
        try:
            return func(*args)
        except Schoolkid.DoesNotExist:
            print(f'пользователя {args[0]} не существует')
        except AttributeError:
            print(f'что-то пошло не так, проверьте существует ли пользователь')

    return wrapper


@error_catcher
def get_schoolkid(full_name: str) -> Schoolkid:
    """
    Поиск учетной записи.

    :param full_name: ФИО ученика
    :return Schoolkid:
    """
    return Schoolkid.objects.get(full_name__contains=full_name)


@error_catcher
def fix_marks(schoolkid: Schoolkid):
    """
    Исправление всех плохих оценок на пятерки.

    :param schoolkid: модель ученика
    :return: no value
    """
    bad_points = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_points.update(points=5)


@error_catcher
def remove_chastisements(schoolkid: Schoolkid):
    """
    Удаление замечаний учителей.

    :param schoolkid: модель ученика
    :return: no value
    """
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements_count = chastisements.count()
    chastisements.delete()
    print(f'удалено {chastisements_count} объектов')


@error_catcher
def create_commendation(schoolkid: Schoolkid, subject='Математика'):
    """
    Создание похвалы.

    :param schoolkid: модель ученика
    :param subject: название предмета
    :return: no value
    """
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject,
    ).order_by('date')

    count_lessons = lessons.count()

    lesson = lessons[random.randint(0, count_lessons)]

    Commendation.objects.create(
        text=random.choice(all_commendations),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
