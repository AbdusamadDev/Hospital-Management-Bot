# # from datetime import timedelta

# # a = timedelta(seconds=5)
# # print(a)
# # print("asdasd")
# # if  a:
# #     print("qweqwe")
# # a = "554as"
# # print(int(a))
# from aiogram import Bot, Dispatcher, types, executor
# # import logging

# import tokens

# TOKEN = tokens.token
# bot = Bot(token=TOKEN)
# # storage = MemoryStorage()
# dp = Dispatcher(bot)
# # logging.basicConfig(level=logging.INFO)


with open("video.mp4", mode="rb") as file:
    with open("video.txt", "wb") as text:
        text.write(file.read())


# # executor.start_polling(dp)
# print(ord("_"))


# @dp.message_handler()
# async def messages(message: types.Message):
#     if message.text == "salom":
#         await message.reply("SAlom!!!!")


# async def mess_ass(message: types.Message):
#     if message.text == "asd":
#         await message.reply("Fuck you welcome")

# executor.start_polling(dp)




