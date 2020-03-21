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


def exceptDecorator(func):
    def wrapper(*args):
        try:
            func(*args)
        except Schoolkid.DoesNotExist:
            print(f'пользователя {args[0]} не существует')
        except AttributeError:
            print(f'что-то пошло не так, проверьте существует ли пользователь')

    return wrapper


def all_schoolkids() -> list:
    """
    Все ученики
    """
    return Schoolkid.objects.all()


@exceptDecorator
def find_schoolkid(full_name):
    """
    Поиск учетной записи
    """
    # try:
    return Schoolkid.objects.get(full_name__contains=full_name)
    # except Schoolkid.DoesNotExist:
    #     print(f'пользователя {full_name} не существует')


@exceptDecorator
def find_marks(schoolkid: Schoolkid):
    """
    Поиск оценок ученика
    """
    return Mark.objects.filter(schoolkid__full_name__contains=schoolkid.full_name)


@exceptDecorator
def find_bad_points(schoolkid: Schoolkid):
    """
    Поиск плохих оценок ученика
    """
    return Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])


@exceptDecorator
def fix_first_bad_point(schoolkid: Schoolkid):
    """
    Исправление первой плохой оценки
    """
    bad_points = Mark.objects.get(schoolkid=schoolkid, points__in=[2, 3])
    bad_points.points = 5
    bad_points.save()


@exceptDecorator
def fix_marks(schoolkid: Schoolkid):
    """
    Исправление всех плохих оценок на пятерки
    """
    bad_points = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bad_points.update(points=5)


@exceptDecorator
def find_chastisements(schoolkid: Schoolkid):
    """
    Поиск замечаний ученика
    """
    return Chastisement.objects.filter(schoolkid=schoolkid)


@exceptDecorator
def remove_chastisements(schoolkid: Schoolkid):
    """
    Удаление замечаний учителей
    """
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements_count = chastisements.count()
    chastisements.delete()
    print(f'удалено {chastisements_count} объектов')


@exceptDecorator
def find_all_lessons(schoolkid: Schoolkid):
    """
    Поиск всех занятий ученика
    """
    return Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
    )


@exceptDecorator
def find_lessons(schoolkid: Schoolkid, subject='Математика'):
    """
    Поиск всех занятий ученика по предмету
    """
    return Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject.title
    )


@exceptDecorator
def create_commendation(schoolkid: Schoolkid, subject_title='Математика'):
    """
    Создание похвалы
    """
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title,
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


if __name__ == '__main__':
    child_name = 'Фролов Иван'
    schoolkid = find_schoolkid(child_name)
    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, 'Математика')
