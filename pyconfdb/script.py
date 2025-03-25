import tkinter as tk
from tkinter import messagebox
import psycopg2
import requests
import schedule
import time
import configparser
import threading
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

# Функция SQL-запроса
def execute_query():
    try:
        db_params = {
            "dbname": config["Database"]["dbname"],
            "user": config["Database"]["user"],
            "password": config["Database"]["password"],
            "host": config["Database"]["host"],
            "port": config["Database"]["port"]
        }
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                with open(config["Settings"]["sql_file"], "r") as sql_file:
                    sql_query = sql_file.read()
                cur.execute(sql_query)
                rows = cur.fetchall()
                
                # Сохраняем в output.txt
                with open(config["Settings"]["output_file"], "w") as f:
                    delimiter = config["Settings"]["delimiter"]
                    for row in rows:
                        f.write(delimiter.join(map(str, row)) + "\n")
        
        send_to_telegram()
        messagebox.showinfo("Успех", "Запрос выполнен и данные отправлены!")
    
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {e}")

# Функция для отправки данных в Tg
def send_to_telegram():
    try:
        bot_token = config["Telegram"]["bot_token"]
        send_to = config["Telegram"]["send_to"]
        output_file = config["Settings"]["output_file"]

        with open(output_file, "r") as f:
            data = f.read()

        if send_to == "user":
            chat_id = config["Telegram"]["user_id"]
        elif send_to == "channel":
            chat_id = config["Telegram"]["channel_id"]
        else:
            raise ValueError("Некорректный режим отправки")

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {"chat_id": chat_id, "text": data}
        response = requests.post(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Ошибка отправки Telegram: {response.text}")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка отправки: {e}")

# Функция проверки подключения к БД
def check_db_connection():
    try:
        db_params = {
            "dbname": config["Database"]["dbname"],
            "user": config["Database"]["user"],
            "password": config["Database"]["password"],
            "host": config["Database"]["host"],
            "port": config["Database"]["port"]
        }
        with psycopg2.connect(**db_params) as conn:
            messagebox.showinfo("Успех", "Подключение к БД успешно!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка подключения к БД: {e}")

# Функция запуска по расписанию
def start_scheduled_task():
    schedule_mode = schedule_var.get()

    if schedule_mode == "time":
        schedule_time = config["Settings"]["schedule_time"]
        schedule.every().day.at(schedule_time).do(execute_query)
        messagebox.showinfo("Расписание", f"Запрос будет выполнен в {schedule_time}")

    elif schedule_mode == "interval":
        interval = int(config["Settings"]["schedule_interval"])
        schedule.every(interval).minutes.do(execute_query)
        messagebox.showinfo("Расписание", f"Запрос будет выполняться каждые {interval} минут")

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()

# Функция изменения режима отправки (пользователь/канал)
def set_send_mode(mode):
    config["Telegram"]["send_to"] = mode
    with open("config.ini", "w") as configfile:
        config.write(configfile)
    messagebox.showinfo("Настройки", f"Режим отправки изменен: {mode}")

# GUI
root = tk.Tk()
root.title("SQL Автоматизация")

btn_start = tk.Button(root, text="Начать", command=execute_query)
btn_start.pack(pady=5)

btn_check_db = tk.Button(root, text="Проверить подключение", command=check_db_connection)
btn_check_db.pack(pady=5)

schedule_var = tk.StringVar(value="time")
frame_schedule = tk.LabelFrame(root, text="Выбор режима отправки")
frame_schedule.pack(pady=5)

radio_time = tk.Radiobutton(frame_schedule, text="Отправка в заданное время", variable=schedule_var, value="time")
radio_time.pack(anchor="w")

radio_interval = tk.Radiobutton(frame_schedule, text="Отправка через интервал", variable=schedule_var, value="interval")
radio_interval.pack(anchor="w")

btn_schedule = tk.Button(root, text="Запустить отправку", command=start_scheduled_task)
btn_schedule.pack(pady=5)

frame_telegram = tk.LabelFrame(root, text="Куда отправлять?")
frame_telegram.pack(pady=5)

btn_user = tk.Button(frame_telegram, text="Отправка пользователю", command=lambda: set_send_mode("user"))
btn_user.pack(side="left", padx=5)

btn_channel = tk.Button(frame_telegram, text="Отправка в канал", command=lambda: set_send_mode("channel"))
btn_channel.pack(side="right", padx=5)

root.mainloop()
