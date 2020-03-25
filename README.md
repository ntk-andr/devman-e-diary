# devman-e-diary
Devman 2.0. Знакомство с Django: ORM. 

## Взламываем электронный дневник

### Цели:
- Исследуйте базу
- Исправьте успеваемость
- Удалите замечания


### Запуск скрипта на работающем сайте
- поместить файл `scripts.py` на один уровень с файлом `manage.py` проекта
- запустить скрипт командой `python scripts.py`

### Примеры запуска скрипта
- Получение учетной записи.
```
from scripts import find_schoolkid
full_name = 'Фролов Иван'
schoolkid = find_schoolkid(child_name)
print(schoolkid) 
```

- Исправление всех плохих оценок на пятерки.
```
from scripts import find_schoolkid, fix_marks
full_name = 'Фролов Иван'
schoolkid = find_schoolkid(child_name)
fix_marks(schoolkid)
```
- Удаление замечаний учителей.
```
from scripts import find_schoolkid, remove_chastisements
full_name = 'Фролов Иван'
schoolkid = find_schoolkid(child_name)
remove_chastisements(schoolkid)
```

- Создание похвалы.
```
from scripts import find_schoolkid, create_commendation
full_name = 'Фролов Иван'
schoolkid = find_schoolkid(child_name)
create_commendation(schoolkid, 'Математика')
```

