import tkinter as tk
import os
import sys
import keyboard
from tkinter import messagebox
import winsound
import threading
from screeninfo import get_monitors

def disable_keys():
    keys_to_block = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", 
        "w", "x", "y", "z", "shift", "caps lock", "escape", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", 
        "f11", "f12", "space", "left", "right", "up", "down", "home", "end", "page up", 
        "page down", "pause", "print screen", "num lock", "scroll lock", "win", "alt", "ctrl", 
        "tab", "insert"
    ]
    
    for key in keys_to_block:
        keyboard.block_key(key)

def create_red_window_on_non_main_monitors():
    monitors = get_monitors()
    main_monitor = monitors[0]

    for monitor in monitors[1:]:
        root = tk.Tk()
        root.title("نافذة غير أساسية")
        root.geometry(f"{{monitor.width}}x{{monitor.height}}+{{monitor.x}}+{{monitor.y}}")
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.config(background="black")
        root.bind("<F4>", lambda e: "break")
        root.bind("<Button-1>", lambda e: None)
        root.bind("<Button-3>", lambda e: None)
        root.bind("<Escape>", lambda e: None)
        root.resizable(False, False)
        root.mainloop()

def create_lock_screen():
    root = tk.Tk()
    root.title("نظام الحماية القصوى")
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.config(bg="black")
    
    tk.Label(root, text="تم تفعيل وضع الحماية القصوى", fg="red", bg="black", font=("Arial", 24)).pack(pady=50)
    tk.Label(root, text="لإلغاء الحماية، الرجاء إدخال كود الأمان من قبل المسؤول", fg="white", bg="black").pack()
    
    entry = tk.Entry(root, width=30, font=("Arial", 16), justify="center")
    entry.pack(pady=20)
    
    def check_code():
        if entry.get() == "{PROTECTION_CODE}":
            root.destroy()
            os.system("taskkill /f /im protection.exe")
        else:
            winsound.Beep(1000, 500)
            messagebox.showerror("خطأ", "كود الأمان غير صحيح")
    
    tk.Button(root, text="إدخال", command=check_code).pack()
    
    disable_keys()
    threading.Thread(target=create_red_window_on_non_main_monitors, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    create_lock_screen()
