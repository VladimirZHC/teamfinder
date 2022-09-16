## Для запуска локального сервера разработки  
Склонируйте репозиторий.  
В папке **hseblog** создайте файл `.env` с ключом `SECRET_KEY='<your_key>'`, это необходимо для работы Django. Можете придумать свой ключ, или воспользоваться генератором (например [djecrety](https://djecrety.ir/)).

Для параметров почты gmail обратитесь к разработчику!

*До конца установки все команды выполняются из корневой директории проекта.*  
Установите виртуальное окружение: `python -m venv venv`  
Активируйте его:
- на linux/mac: `source venv/bin/activate`  
- на windows: `source venv\Scripts\activate`

Установите зависимости:  
`pip install -r requirements.txt`  
Проведите миграции БД:  
`python manage.py migrate`  
Загрузить данные из БД:  
`python manage.py loaddata data.json`  
Запустите сервер разработчика:  
`python manage.py runserver`