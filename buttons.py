from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

"""
Admin uchun knopkalar:
________________________
Fikr-mulohazarni ko'rish
Massajga navbatlar
Post qo'yish
Yangi admin
Yangi gruppa

Client uchun knopkalar:
________________________
Navbatga yozilish
Ish jarayoni
Izoh qoldirish
"""

help = KeyboardButton(text="☝️ Yordam")
show_feedback = KeyboardButton(text="🗣 Fikr-mulohazarni ko'rish")
massage_queue = KeyboardButton(text="👥 Massajga navbatlar")
post_blog = KeyboardButton(text="📮 Post qo'yish")
new_admin = KeyboardButton(text="🧑🏻‍💻 Yangi Admin")
new_group = KeyboardButton(text="👥 Yangi gruppa")
clear_queue = KeyboardButton(text="👥 Navbatlar bazasini tozalash")
clear_feedback = KeyboardButton(text="✍️ Izohlar bazasini tozalash")

AdminButtons = ReplyKeyboardMarkup(resize_keyboard=True).add(
    show_feedback, 
    massage_queue, 
    post_blog, 
    new_admin, 
    new_group,
    clear_queue,
    clear_feedback
)

create_queue = KeyboardButton(text="👥 Navbatga yozilish")
work_process = KeyboardButton(text="👷‍♂️ Ish Jarayonimiz")
feedback_button = KeyboardButton(text="✍️ Izoh qoldirish")
cancel_button = KeyboardButton(text="🚫 Navbatni bekor qilish")

ClientButtons = ReplyKeyboardMarkup(resize_keyboard=True).add(
    create_queue,
    work_process,
    feedback_button,
    help
)

yes = KeyboardButton("Ha, albatta")
no = KeyboardButton("Yo'q")

yes_no = ReplyKeyboardMarkup(resize_keyboard=True).add(yes, no)
