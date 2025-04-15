import keyboard
import time
import tkinter as tk
from tkinter import ttk
import threading

settings = {
    'tap_time': 0.14,    
    'ctrl_time': 0.33,    
    'trigger_key': 'alt',
    'current_mode': 1
}

def cycle_action_mode1():
    try:
        keyboard.press('s')
        time.sleep(settings['tap_time'])
        keyboard.release('s')
        
        keyboard.press('ctrl')
        time.sleep(settings['ctrl_time'])
        keyboard.release('ctrl')
    except Exception as e:
        print(f"Ошибка в цикле: {e}")
        for key in ['s', 'ctrl']:
            keyboard.release(key)

def cycle_action_mode2():
    try:
        keyboard.press('s')
        keyboard.press('ctrl')
        time.sleep(settings['ctrl_time'])
        keyboard.release('s')
        keyboard.release('ctrl')
    except Exception as e:
        print(f"Ошибка в цикле: {e}")
        for key in ['s', 'ctrl']:
            keyboard.release(key)

def macro_loop():
    while True:
        if keyboard.is_pressed(settings['trigger_key']):
            if settings['current_mode'] == 1:
                cycle_action_mode1()
            else:
                cycle_action_mode2()
        time.sleep(0.1)

def apply_settings():
    try:
        settings['tap_time'] = float(tap_time_entry.get())
        settings['ctrl_time'] = float(ctrl_time_entry.get())
        settings['trigger_key'] = trigger_key_entry.get().lower()
        status_label.config(text="Настройки применены")
    except ValueError:
        status_label.config(text="Ошибка! Проверьте значения")

def switch_mode():
    settings['current_mode'] = 3 - settings['current_mode']
    mode_label.config(text=f"Текущий режим: {settings['current_mode']}")

root = tk.Tk()
root.title("Настройки макроса")
root.geometry("300x280")

ttk.Label(root, text="Время нажатия S:").pack(pady=5)
tap_time_entry = ttk.Entry(root)
tap_time_entry.insert(0, "0.14")
tap_time_entry.pack()

ttk.Label(root, text="Время удержания Ctrl:").pack(pady=5)
ctrl_time_entry = ttk.Entry(root)
ctrl_time_entry.insert(0, "0.33")
ctrl_time_entry.pack()

ttk.Label(root, text="Клавиша активации:").pack(pady=5)
trigger_key_entry = ttk.Entry(root)
trigger_key_entry.insert(0, "alt")
trigger_key_entry.pack()

ttk.Button(root, text="Применить", command=apply_settings).pack(pady=10)
status_label = ttk.Label(root, text="")
status_label.pack()

ttk.Button(root, text="Переключить режим", command=switch_mode).pack(pady=10)
mode_label = ttk.Label(root, text="Текущий режим: 1")
mode_label.pack()

macro_thread = threading.Thread(target=macro_loop, daemon=True)
macro_thread.start()

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()