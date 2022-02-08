# praktikum_new_diplom
![foodgram](https://github.com/Andromaril/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

<h2>Описание проекта:</h2>
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

<h2>Как запустить проект</h2>
Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/Andromaril/foodgram-project-react.git


Запустить docker-compose и собрать контейнеры  командой  
docker-compose up -d --build

Теперь в контейнере backend нужно выполнить миграции, создать суперпользователя.

<h3>Выполните по очереди команды:</h3>

docker-compose exec backend python manage.py makemigrations

docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py createsuperuser

docker-compose exec backend python manage.py collectstatic --noinput

<h3>Oписание команды для заполнения базы данными.</h3>

sudo docker-compose exec backend python manage.py load_ingredients

<h3>Для того, чтобы выключить контейнер, используйте команду</h3>

docker-compose down

<h2>шаблон наполнения env-файла</h2>

DB_ENGINE= # указываем, что работаем с postgresql

DB_NAME= # имя базы данных

POSTGRES_USER= # логин для подключения к базе данных

POSTGRES_PASSWORD= # пароль для подключения к БД (установите свой)

DB_HOST= # название сервиса (контейнера)

DB_PORT= # порт для подключения к БД 

https://51.250.23.88/
Админка
Login: Test01
Password: testtest
