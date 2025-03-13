### Это приложение предназначенно для автоматизированного выполнения SQL-запросов и отправки результатов в Telegram (пользователю или в канал). Приложение поддерживает выполнение запросов как вручную, так и по расписанию (в заданное время или через определённый интервал).
## Установка
### Установить python версии 3.10+ и выше.
- Windows: 
При установке поставить галочки "pip", "tcl/tk", "Add Python to environment variables"
- Ubuntu
```sh
sudo apt install python3-pip
```
## Установка зависимостей
Выполнить в консоле:
```sh
pip install psycopg2 requests schedule
```
(tkinter встроен в стандартную библиотеку Python и не требует установки)

## Список необходимых библиотек
Основные библиотеки:
tkinter – графический интерфейс
psycopg2 – подключение к PostgreSQL
requests – отправка данных в Telegram
schedule – выполнение запросов по расписанию
Вспомогательные библиотеки:
configparser – работа с config.ini
time – задержки в коде
datetime – работа с датой и временем
threading – многопоточное выполнение задач

## Сборка(Windows)
```sh
pip install pyinstaller
pyinstaller --onefile --windowed app.py
```
В папке с проектом появится папка dist, внутри будет скомпилированный исполняемый файл

## Настройка config.ini
Для подключения к базе данных и отправки сообщений через tg в config.ini вместо x в соответсвующих строках нужно указать значения(например: user = x, заменить user = root)
Данные сохраняются в той же директории где находится script.py и config.ini в output.txt

## Настройка zapros.sql
В zapros.sql должен находится запрос который будет отправляться базе данных и ответ сохраняться в output.txt, далее отправлятся в настроенный канал или пользователю.
Он также поддерживает многострочные запросы.

## Пример запроса
```
WITH recent_orders AS (
    SELECT user_id, MAX(order_date) AS last_order_date
    FROM orders
    GROUP BY user_id
)
SELECT u.id, u.username, r.last_order_date
FROM users u
LEFT JOIN recent_orders r ON u.id = r.user_id
WHERE r.last_order_date > NOW() - INTERVAL '30 days';
```

## error_log.txt 
Используется для логирования ошибок. Если в процессе работы программы возникнет ошибка (например, сбой подключения к базе данных, неверный SQL-запрос или ошибка при отправке данных в Telegram), информация о ней будет записана в этот файл.

Каждая ошибка содержит:
Временную метку 
Описание ошибки

## Запуск
Запускать можно как скомпилированное приложение из папки dist, так и script.py напрямую командой

Для использования пользователем после запуска кода напишите боту (t.me/Chillraport_bot)
чтобы начать чат нажмите кнопку Старт 

## Использование графического интерфейса
Основные кнопки:

"Начать" — выполняет SQL-запрос и отправляет результат.
"Проверить подключение" — проверяет соединение с базой данных.
"Запустить отправку" — активирует отправку по расписанию.
Выбор режима отправки:
"Отправка в заданное время" — выполняет запрос в конкретное время.
"Отправка через интервал" — выполняет запрос каждые N минут.
Выбор получателя Telegram:
"Отправка пользователю" — данные отправляются в личные сообщения.
"Отправка в канал" — данные отправляются в канал Telegram.

## Возможные ошибки и их решения
Ошибка: chat not found в Telegram

При использовании бота в канале: проверьте, что бот добавлен в канал и является администратором.
При использовании бота для отправки пользователю нужно начать чат с ботом на кнопку (Старт) 

Ошибка: can't parse entities
Проверьте содержимое output.txt. Telegram не поддерживает некоторые спецсимволы.

Ошибка подключения к PostgreSQL
Убедитесь, что PostgreSQL запущен и параметры в config.ini указаны верно.
Проверьте, что брандмауэр или антивирус не блокирует соединение.

ID должен быть числовым

## Дополнительная информация 
Как узнать ID?
Для пользователя:
Напишите боту @userinfobot и получите свой ID.
Вставьте его в config.ini

Для канала:
Добавьте бота в канал и дайте ему права администратора.
Узнайте ID через бота или через API.
Вставьте его в config.ini 


