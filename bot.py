import os
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
	raise RuntimeError("BOT_TOKEN is not set! Add it in Render Environment.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	buttons = ["📍 Филиалы", "📅 Расписание", "📞 Контакты"]
	keyboard.add(*buttons)
	await message.answer(
		"Привет! Это бот школы капоэйры.\n"
		"Выберите раздел:",
		reply_markup=keyboard
	)

# ... остальной код (как раньше) — можно скопировать из предыдущего ответа

@dp.message_handler(lambda msg: msg.text == "📍 Филиалы")
async def show_branches(message: types.Message):
	text = (
		"• Интеграция: Москва, ул. Лазо, 12\n"
		"• МосАРТ: Москва, Свободный проспект, 19\n"
		"• Взрослые: Москва, Саянская ул., 7"
	)
	await message.answer(text)

@dp.message_handler(lambda msg: msg.text == "📅 Расписание")
async def schedule_menu(message: types.Message):
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	keyboard.add(
		types.InlineKeyboardButton("Интеграция", callback_data="sch_int"),
		types.InlineKeyboardButton("МосАРТ", callback_data="sch_art"),
		types.InlineKeyboardButton("Взрослые", callback_data="sch_adult")
	)
	await message.answer("Выберите филиал:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("sch_"))
async def send_schedule(callback: types.CallbackQuery):
	mapping = {
		"sch_int": "Интеграция\n📍 ул. Лазо, 12\n\n• 3–5 лет: Вт, Чт — 18:00–19:00\n• 6–10 лет: Вт, Чт — 17:00–18:00\n• 11+: Вт, Чт — 19:00–20:00",
		"sch_art": "МосАРТ\n📍 Свободный пр., 19\n\n• 3–5 лет: Ср, Пт — 18:00–19:00\n• 5–7 лет: Ср, Пт — 16:00–17:00\n• 8–9 лет: Ср, Пт — 17:00–18:00\n• 10–12 лет: Ср, Пт — 19:00–20:00\n• 12+: Ср, Пт — 20:00–21:00",
		"sch_adult": "Взрослые\n📍 Саянская ул., 7\n\n• 18+: Ср, Пт — 09:00–10:00"
	}
	text = mapping.get(callback.data, "Неизвестный филиал")
	await callback.message.edit_text(text)
	await callback.answer()

@dp.message_handler(lambda msg: msg.text == "📞 Контакты")
async def contacts(message: types.Message):
	await message.answer("📞 +7 (XXX) XXX-XX-XX\n📧 capoeira@moscow.ru")

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)