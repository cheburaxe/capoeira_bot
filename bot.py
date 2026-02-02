import os
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("8200093598:AAGe4Tj9I6vpzCro9_GS8OyWk5TRCPFyLPs")
if not BOT_TOKEN:
	raise RuntimeError("BOT_TOKEN не задан! Добавьте его в Environment Variables на Render.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	keyboard.add("📍 Филиалы", "📅 Расписание", "📞 Контакты")
	await message.answer(
		"Привет! 👋 Это официальный бот школы капоэйры.\n\n"
		"Выберите интересующий вас раздел:",
		reply_markup=keyboard
	)

@dp.message_handler(lambda m: m.text == "📍 Филиалы")
async def branches(message: types.Message):
	text = (
		"<b>Наши филиалы в Москве:</b>\n\n"
		"• <b>Интеграция</b>\n  📍 ул. Лазо, 12\n\n"
		"• <b>МосАРТ</b>\n  📍 Свободный проспект, 19\n\n"
		"• <b>Взрослые</b>\n  📍 Саянская улица, 7"
	)
	await message.answer(text, parse_mode="HTML")

@dp.message_handler(lambda m: m.text == "📅 Расписание")
async def schedule_menu(message: types.Message):
	kb = types.InlineKeyboardMarkup(row_width=1)
	kb.add(
		types.InlineKeyboardButton("Интеграция", callback_data="int"),
		types.InlineKeyboardButton("МосАРТ", callback_data="art"),
		types.InlineKeyboardButton("Взрослые", callback_data="adult")
	)
	await message.answer("Выберите филиал:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data in ("int", "art", "adult"))
async def show_schedule(callback: types.CallbackQuery):
	schedules = {
		"int": (
			"<b>Интеграция</b>\n📍 ул. Лазо, 12\n\n"
			"<b>Расписание:</b>\n"
			"• Дети 3–5 лет: Вт, Чт — 18:00–19:00\n"
			"• Дети 6–10 лет: Вт, Чт — 17:00–18:00\n"
			"• Подростки 11+: Вт, Чт — 19:00–20:00"
		),
		"art": (
			"<b>МосАРТ</b>\n📍 Свободный проспект, 19\n\n"
			"<b>Расписание:</b>\n"
			"• Дети 3–5 лет: Ср, Пт — 18:00–19:00\n"
			"• Дети 5–7 лет: Ср, Пт — 16:00–17:00\n"
			"• Дети 8–9 лет: Ср, Пт — 17:00–18:00\n"
			"• Дети 10–12 лет: Ср, Пт — 19:00–20:00\n"
			"• Подростки 12+: Ср, Пт — 20:00–21:00"
		),
		"adult": (
			"<b>Взрослые</b>\n📍 Саянская улица, 7\n\n"
			"<b>Расписание:</b>\n"
			"• Взрослые 18+: Ср, Пт — 09:00–10:00"
		)
	}
	text = schedules.get(callback.data, "Расписание временно недоступно.")
	await callback.message.edit_text(text, parse_mode="HTML")
	await callback.answer()

@dp.message_handler(lambda m: m.text == "📞 Контакты")
async def contacts(message: types.Message):
	await message.answer(
		"📞 Телефон: +7 (XXX) XXX-XX-XX\n"
		"📧 Email: capoeira@moscow.ru\n"
		"🌐 Instagram: @your_capoeira_school"
	)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)