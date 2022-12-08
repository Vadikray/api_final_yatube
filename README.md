# Описание проекта:
API для сайта. Через которое можно публиковать посты. Подписываться на авторов и оставлять комментирии.

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Vadikray/api_final_yatube.git
```
```
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```

# Примеры запросов API к сайту
Запрос
```
http://127.0.0.1:8000/api/v1/posts/
```
ответ
```
{
"count": 123,
"next": "http://api.example.org/accounts/?offset=400&limit=100",
"previous": "http://api.example.org/accounts/?offset=200&limit=100",
"results": [
{
"id": 0,
"author": "string",
"text": "string",
"pub_date": "2021-10-14T20:41:29.648Z",
"image": "string",
"group": 0
}
]
}
```
запрос
```
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/
```
ответ
```
{
"id": 0,
"author": "string",
"text": "string",
"created": "2019-08-24T14:15:22Z",
"post": 0
}
```
# Автор: Конюшков В.А.