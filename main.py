from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import Unauthorized
from aiogram.dispatcher import FSMContext
import tokens, database, buttons
import logging, os, sqlite3
from states import *

"""
admin
20051205
___________
admin nima qila oladi?
 - xabar qosha oladi
 - botga kegan xabarlani kora olsin
 |_ xabarlar: ochered va taklif yoki shikoyatlar 
___________________________________
user nima qila oladi?
 - doktorga navbatga yozilishi mumkin
 - davolash muolaja bo'yicha shikoyat qila oladi
 - boglanish, locatsiya tashlash
 - ish jihozlar haqida malumot berish
 - agar user keraksz narsalar yozsa "knopkalardan birini tanlang" deb ogohlantirishi kerak.
_______________________________________________
gruppada bot nima qila oladi?
 - admindan kegan postlani gruppaga qosha olishi kerak

. User soralgan gruppalarga qoshilgan bolsagina botni ishlata olsin
. Bot designi ornida bolishi kerak
. Mustahkam bot bolishi kerak

buyrug'lar
/start, /help, /navbatlar, /takliflar, /post_blog, 
/set_new_admin, /set_group_id, /massage_navbat, 
/work_process, /feedback, /my_id
"""

# initiate settings
TOKEN = tokens.token
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot=bot, storage=storage)
logging.basicConfig(level=logging.INFO)


help_text = "Ushbu botni yaratishdan maqsad mijozlar va shifokorlar o'rtasidagi \
muloqotni yanada takomillashtirishdir. Bu bot asosan mijozlarimizning ishini osonlashtirish \
uchun xizmat qiladi. Botga asosan tugmachalar yodamida murojaat qilishingizni tafsira qilib \
qolar edik, chunki mijozlar uchun umumiy kerak boladigan buyrug'lar shu tugmachalarda mujassam."

def is_logged_in(user_id):
    with open(f"{path_normalizer()}admin_id.txt", mode="r") as file:
        id = file.read().strip()
        print(id)
        print(user_id)
    return int(id) == user_id
    
def path_normalizer():
    filtered_path = ""
    path = os.getcwd().split("\\")
    for i in path:
        filtered_path += i + "/"
    return filtered_path + "bot/"

def get_group_id():
    with open("{}group_username.txt".format(path_normalizer()), "r") as file:
        return file.read().strip()

def is_correct_group_name(text=None) -> bool:
    alphabet = [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)] + ["_"]
    if text is None:
        return None
    for i in text:
        if i not in alphabet:
            return False
    return True   

@dispatcher.message_handler(commands=["start"])
async def welcome(message: types.Message):
    if is_logged_in(message.from_user.id):
        await message.reply(
            f"Assalomu alaykum Admin {message.from_user.first_name}\nHush kelibsiz!",
            reply_markup=buttons.AdminButtons
        )
    else:
        await message.reply(
            f"Assalomu alaykum {message.from_user.first_name}",
            reply_markup=buttons.ClientButtons
        )

@dispatcher.message_handler()
async def all_message_handling_in_one_function(message: types.Message):
    if is_logged_in(message.from_user.id):
        if message.text == "🗣 Fikr-mulohazarni ko'rish":
            print(message.text)
            query = database.FeedbacksModel()
            models = query.retrieve_data()
            if not models:
                await message.reply("☹️ Hech qanday ma'lumot topilmadi!")
            for model in models:
                await message.answer(
                    f"👤 @{model[1]} dan kelgan Izoh.\n\n{model[2]}\n\nSana 📅: {model[3]}"
                )
        elif message.text == "👥 Massajga navbatlar":
            print(message.text)
            queryset = database.QueueModel()
            models = queryset.retrieve_data()
            if not models:
                await message.reply("☹️ Hech qanday ma'lumot topilmadi!")
            for model in models:
                await message.answer(
                    f"👤 @{model[1]} dan navbat\n\n{model[2]}\n\nSana 📅: {model[3]}")
        elif message.text == "📮 Post qo'yish":
            await BlogPost.post.set()
            await message.reply("Iltimos, guruhga post qo'yish uchun postni menga yozing:")
        elif message.text == "🧑🏻‍💻 Yangi Admin":
            print(message.text)
            await UserId.user_id.set()
            await message.reply(
                "Iltimos, yangi admin profilining id sini kiriting, " 
                "qanday kiritishni bilmasangiz admin panelni topshirmoqchi bo'lgan profilingizdan shu >"
                " @raw_data_bot ga nurojaat qilib 10 talik raqamni kiriting\n\n"
                "Note: Iltimos, xato qilmaslikka harakat qiling, chunki xato id kiritib qo'ysangiz admin"
                " panel bilan boshqa bog'lana olmay qolasiz!")
        elif message.text == "👥 Yangi gruppa":
            print(message.text)
            await GroupId.chat_id.set()
            await message.reply("Iltimos guruh nomini ehtiyotkorlik bilan kiriting:")
        elif message.text == "☝️ Yordam":
            await message.reply(help_text)
        elif message.text == "👥 Navbatlar bazasini tozalash":
            query = database.QueueModel()
            query.clear()
            await message.reply("Hamma mijozlardan kelgan navbatlar ma'lumotlar bazasidan o'chirib tashlandi!")
        elif message.text == "✍️ Izohlar bazasini tozalash":
            query = database.FeedbacksModel()
            query.clear()
            await message.reply("Hamma mijozlardan kelgan izohlar ma'lumotlar bazasidan o'chirib tashlandi!")
        else:
            if message.text != "/start":
                await message.reply("⚠️ Iltimos, tugmalar orqali murojaat qiling!")
    else:
        print("Not logged in")
        if message.text == "👥 Navbatga yozilish":
            await ClientMassageRequest.cover_letter.set()
            await message.reply("Iltimos, telefon raqamingiz, ism-familiyangizni tushunarli "
            "qilib kiriting va holat haqida batafsilroq yozing, shu orqali biz siz bilan "
            "keyinchalik bog'lana olamiz")
        elif message.text == "👷‍♂️ Ish Jarayonimiz":
            video = open("{}video.txt".format(path_normalizer()), "rb").read()
            await message.answer_video(video=video)
            await message.answer("Bizning shifoxona ko'p yillardan beri o'z sohasi bo'yicha bir necha "
            "yutuqlarga erishish bilan cheklanmay, ko'p mijozlarni ishonchini qozonishga ulgurgan. Bizning "
            "klinikaga murojaat qiling, biz esa qo'limizdan kelganicha sizning salomatligingizga hissamizni "
            "qo'shishga harakat qilamiz!")
        elif message.text == "✍️ Izoh qoldirish":
            await ClientFeedbackRequest.feedback.set()
            await message.reply("Iltimos, klinika haqida fikringiz, takliflaringiz "
            "yoki kamchiliklaringiz bo'lsa yozing, biz esa buni bosh shifokorimizga "
            "avtomatik tarzda yetkazamiz!")
        elif message.text == "☝️ Yordam":
            await message.reply(help_text)
        elif message.text == "🚫 Navbatni bekor qilish":
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            last_record_id = cursor.execute("""SELECT COUNT(*) FROM queue;""")[0][0]
            username = cursor.execute("""SELECT username FROM queue WHERE id = ?""", (int(last_record_id),))[0][0]
            if message.from_user.username == username:
                model = database.QueueModel()
                model.cancel_queue()
                await message.reply("E'tiboringiz uchun rahmat, boshqa safar sizni intiqlik bilan kutib qolamiz!")
            else:
                await message.reply("⚠️ Uzr, lekin siz hali navbatga yozilmadingiz "
                "yoki boshqa kishini navbatini ochirishga urinyapsiz")
        else:
            await message.reply(
                f"Hurmatli {message.from_user.first_name}\n❓ Sizga qanday "
                "yordam bera olamz?\n😊 Tugmalar orqali murojaat qiling!",
                reply_markup=buttons.ClientButtons
            )

@dispatcher.message_handler(state=ClientMassageRequest.cover_letter)
async def massage_request(message: types.Message, state: FSMContext):
    print(message.text)
    if not is_logged_in(int(message.from_user.id)):
        model = database.QueueModel(username=message.from_user.username, body=message.text)
        model.add()
        await message.reply("🥳🥳🥳\nTabriklaymiz! Siz bilan shifokorlarimiz o'zlari tez orada bog'lanishadi.")
        await state.finish()
    else:
        await message.reply("⚠️ Uzr, lekin siz adminsiz. Admin mijozlar qilgan ishni qila olmaydi!")
        await state.finish()

@dispatcher.message_handler(state=BlogPost.post)
async def admin_post(message: types.Message, state: FSMContext):
    print(message.text)
    try:
        chat_id = get_group_id()
        await bot.send_message(chat_id=chat_id, text=message.text)
        await state.finish()
        await message.answer("Sizning postingiz guruhga joylandi!")
    except Unauthorized:
        await message.reply("Bot hali guruhga qo'shilmagan, iltimos "
        "botni birinchi guruhga qo'shib keyin post qo'ying!")

@dispatcher.message_handler(state=UserId.user_id)
async def process_name(message: types.Message, state: FSMContext):
    print(message.text)
    if str(message.text).isdigit() and len(message.text) == 10:
        with open("{}admin_id.txt".format(path_normalizer()), "w") as file:
            file.write(str(message.text))
            file.close()
        await message.reply("🥳🥳🥳\nTabriklaymiz, Siz hozirgina admin panelni boshqa profilga topshirdingiz!")
        await state.finish()
    else:
        await state.finish()
        await message.reply("⚠️ ID yaroqsiz, iltimos yaroqli ID kiriting!")

@dispatcher.message_handler(state=GroupId.chat_id)
async def set_group_id(message: types.Message, state: FSMContext):
    print(message.text)
    if not is_correct_group_name(text=message.text):
        await message.reply("⚠️ Iltimos yaroqli guruh nomini kiriting!")
        await state.finish()
    else:
        with open("{}group_username.txt".format(path_normalizer()), "w") as file:
            file.write("@" + message.text if message.text[0] != "@" else message.text)
        await message.reply("🥳🥳🥳\nTabriklaymiz! Endi bot {} "
        "nomli guruhga xizmat qiladi!".format("@" + message.text))
        await state.finish()

@dispatcher.message_handler(state=ClientFeedbackRequest.feedback)
async def give_feedback(message: types.Message, state: FSMContext):
    print(message.text)
    if not is_logged_in(int(message.from_user.id)):
        model = database.FeedbacksModel(username=message.from_user.username, body=message.text)
        model.add()
        await message.reply("🥳🥳🥳\nTashakkur! Sizning har bir izoh va takliflaringiz biz uchun qadrli!")
        await state.finish()
    else:
        await message.reply("⚠️ Uzr, lekin siz adminsiz. Admin mijozlar qilgan ishni qila olmaydi!")

if __name__ == "__main__":
    obj = database.QueueModel()
    obj.create()  
    executor.start_polling(dispatcher=dispatcher, skip_updates=False)
