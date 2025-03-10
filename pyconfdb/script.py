import psycopg2
import configparser
import tkinter as tk
from tkinter import messagebox
import os
import threading
import time
from datetime import datetime
import schedule

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.ini")
    if not os.path.exists(config_path):
        raise FileNotFoundError("Файл config.ini не найден в директории скрипта")
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config

def validate_config(config):
    required_db_keys = ["dbname", "user", "password", "host", "port"]
    required_settings_keys = ["query", "delimiter", "output_file", "schedule"]
    
    if not config.has_section("Database") or not config.has_section("Settings"):
        raise ValueError("Конфигурационный файл должен содержать секции [Database] и [Settings]")
    
    for key in required_db_keys:
        if not config.has_option("Database", key):
            raise ValueError(f"Отсутствует параметр {key} в секции [Database]")
    
    for key in required_settings_keys:
        if not config.has_option("Settings", key):
            raise ValueError(f"Отсутствует параметр {key} в секции [Settings]")

def execute_query():
    try:
        config = load_config()
        validate_config(config)
        db_params = {
            "dbname": config.get("Database", "dbname"),
            "user": config.get("Database", "user"),
            "password": config.get("Database", "password"),
            "host": config.get("Database", "host"),
            "port": config.get("Database", "port")
        }
        query = config.get("Settings", "query")
        delimiter = config.get("Settings", "delimiter")
        output_file = os.path.join(os.path.dirname(__file__), config.get("Settings", "output_file"))
        
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                with open(output_file, "w", encoding="utf-8") as f:
                    if rows:
                        for row in rows:
                            f.write(delimiter.join(map(str, row)) + "\n")
                    else:
                        f.write("No data returned\n")
        messagebox.showinfo("Успех", f"Результаты сохранены в {output_file}")
    except Exception as e:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Error: {str(e)}\n")
        messagebox.showerror("Ошибка", str(e))

def schedule_task():
    config = load_config()
    schedule_time = config.get("Settings", "schedule")
    schedule.every().day.at(schedule_time).do(execute_query)
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_scheduled_execution():
    thread = threading.Thread(target=schedule_task, daemon=True)
    thread.start()

def create_gui():
    root = tk.Tk()
    root.title("PostgreSQL Query Executor")
    root.geometry("300x150")
    
    tk.Button(root, text="Начать", command=execute_query, height=2, width=15).pack(pady=30)
    
    start_scheduled_execution()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
