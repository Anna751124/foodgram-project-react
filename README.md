## Проект Foodgram

«Фудграм» — сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное 
и подписываться на публикации других авторов. Пользователям сайта также будет доступен сервис «Список 
покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Технологии:

Python, Django, Docker, Gunicorn, NGINX, PostgreSQL

### Сервис доступен по адресу:
```
http://foodgram256.hopto.org/
```
### Запуск проекта:
1. Клонируйте проект:
```
git clone git@github.com:Anna751124/foodgram-project-react.git
```
2. Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```
3. Соберите контейнер и выполните миграции:
```
sudo docker compose -f docker-compose.production.yml up -d --build
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
4. Данные для проверки работы приложения:
Суперпользователь:
```
email: admin@mail.ru
password: Diplom1748
```