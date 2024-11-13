import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from datetime import datetime, timedelta

# Глобальные переменные для хранения напоминаний
reminders = []
sound_file = ""  # Переменная для хранения звукового файла


def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()


def set_reminder():
    global sound_file

    reminder_text = reminder_entry.get()

    # Получаем текущее время
    current_time = datetime.now()

    try:
        reminder_hour = int(hour_spinbox.get())
        reminder_minute = int(minute_spinbox.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные значения для часов и минут.")
        return

    reminder_time = current_time.replace(hour=reminder_hour, minute=reminder_minute, second=0, microsecond=0)

    if reminder_time < current_time:
        # Если время напоминания уже прошло, добавляем 1 день
        reminder_time += timedelta(days=1)

    # Сохраняем напоминание
    reminders.append((reminder_text, reminder_time))

    # Добавляем напоминание в Listbox
    reminder_listbox.insert(tk.END, f"{reminder_text} — {reminder_time.strftime('%H:%M:%S')}")

    # Установка таймера на каждое напоминание
    delay = (reminder_time - current_time).total_seconds() * 1000  # задержка в миллисекундах
    root.after(int(delay), lambda text=reminder_text: show_reminder(text))


def show_reminder(reminder_text):
    reminder_window = tk.Toplevel(root)
    reminder_window.title("Напоминание")

    message = tk.Label(reminder_window, text=reminder_text, padx=20, pady=20)
    message.pack()

    # Воспроизводим звук
    if sound_file:
        play_sound(sound_file)

    # Кнопка закрытия окна с напоминанием
    close_button = tk.Button(reminder_window, text="Закрыть", command=lambda: close_reminder(reminder_window))
    close_button.pack(pady=10)


def close_reminder(window):
    pygame.mixer.music.stop()  # Останавливаем музыку
    window.destroy()  # Закрываем окно


def select_sound_file():
    global sound_file
    sound_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])


# Функция для обновления текущего времени
def update_time():
    now = datetime.now()
    current_time_label.config(text=now.strftime("%H:%M:%S"))  # Обновляем текст метки с текущим временем
    root.after(1000, update_time)  # Обновление каждую секунду


# Основное окно приложения
root = tk.Tk()
root.title("Напоминалка")

# Поле для ввода текста напоминания
reminder_entry = tk.Entry(root, width=50)
reminder_entry.pack(pady=10)
reminder_entry.insert(0, "Введите текст напоминания")

# Надпись "Введите время"
time_label = tk.Label(root, text="Выберите время (часы и минуты):")
time_label.pack(pady=5)

# Поля для выбора времени (часы и минуты) с использованием Spinbox
frame_time = tk.Frame(root)
frame_time.pack(pady=10)

# Spinbox для часов и минут
hour_spinbox = tk.Spinbox(frame_time, from_=0, to=23, width=5, format='%02.0f')
hour_spinbox.pack(side=tk.LEFT)
minute_spinbox = tk.Spinbox(frame_time, from_=0, to=59, width=5, format='%02.0f')
minute_spinbox.pack(side=tk.LEFT)

# Кнопка выбора звукового файла
sound_button = tk.Button(root, text="Выбрать звуковой файл", command=select_sound_file)
sound_button.pack(pady=10)

# Кнопка для создания напоминания
create_reminder_button = tk.Button(root, text="Создать напоминание", command=set_reminder)
create_reminder_button.pack(pady=10)

# Метка для отображения текущего времени
current_time_label = tk.Label(root, text="", font=("Helvetica", 24))
current_time_label.pack(pady=20)

# Список для отображения установленных напоминаний
reminder_listbox = tk.Listbox(root, width=50)
reminder_listbox.pack(pady=10)

# Запуск обновления времени
update_time()

root.mainloop()