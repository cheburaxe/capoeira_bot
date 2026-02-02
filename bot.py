from aiogram import Bot, Dispatcher, executor, types

# Замените на ваш токен от @BotFather
BOT_TOKEN = "8200093598:AAGe4Tj9I6vpzCro9_GS8OyWk5TRCPFyLPs"

# Данные о филиалах
BRANCHES = {
	"интеграция": {
		"адрес": "Москва, улица Лазо, 12",
		"расписание": (
			"• Дети 3–5 лет: Вт, Чт — 18:00–19:00\n"
			"• Дети 6–10 лет: Вт, Чт — 17:00–18:00\n"
			"• Подростки 11+: Вт, Чт — 19:00–20:00"
		)
	},
	"мосарт": {
		"адрес": "Москва, Свободный проспект, 19",
		"расписание": (
			"• Дети 3–5 лет: Ср, Пт — 18:00–19:00\n"
			"• Дети 5–7 лет: Ср, Пт — 16:00–17:00\n"
			"• Дети 8–9 лет: Ср, Пт — 17:00–18:00\n"
			"• Дети 10–12 лет: Ср, Пт — 19:00–20:00\n"
			"• Подростки 12+: Ср, Пт — 20:00–21:00"
		)
	},
	"взрослые": {
		"адрес": "Москва, Саянская улица, 7",
		"расписание": "• Взрослые 18+: Ср, Пт — 09:00–10:00"
	}
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	buttons = ["📍 Филиалы", "📅 Расписание", "📞 Контакты"]
	keyboard.add(*buttons)
	await message.answer(
		"Привет! Это официальный бот школы капоэйры Boitata.\n"
		"Здесь вы найдёте адреса и расписание занятий.",
		reply_markup=keyboard
	)

@dp.message_handler(lambda msg: msg.text == "📍 Филиалы")
async def show_branches(message: types.Message):
	text = "Наши филиалы в Москве:\n\n"
	for name, info in BRANCHES.items():
		text += f"• <b>{name.capitalize()}</b>\n  📍 {info['адрес']}\n\n"
	await message.answer(text, parse_mode="HTML")

@dp.message_handler(lambda msg: msg.text == "📅 Расписание")
async def choose_branch_for_schedule(message: types.Message):
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	for key in BRANCHES:
		display_name = key.capitalize() if key != "взрослые" else "Саянская (взрослые)"
		keyboard.add(
			types.InlineKeyboardButton(
				text=display_name,
				callback_data=f"schedule_{key}"
			)
		)
	await message.answer("Выберите филиал:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("schedule_"))
async def send_schedule(callback: types.CallbackQuery):
	branch_key = callback.data.split("_", 1)[1]
	if branch_key in BRANCHES:
		info = BRANCHES[branch_key]
		display_name = "Филиал «Интеграция»" if branch_key == "интеграция" \
					   else "Центр «МосАРТ»" if branch_key == "мосарт" \
					   else "Группа для взрослых (Саянская)"
		text = f"<b>{display_name}</b>\n📍 {info['адрес']}\n\n📅 Расписание:\n{info['расписание']}"
		await callback.message.edit_text(text, parse_mode="HTML")
	else:
		await callback.message.edit_text("Информация временно недоступна.")
	await callback.answer()

@dp.message_handler(lambda msg: msg.text == "📞 Контакты")
async def contacts(message: types.Message):
	# Замените на ваши реальные контакты
	await message.answer(
		"📞 Телефон: +7 (926) 336-61-43\n"
		"🌐 Telegram: @boitata_capoeira\n"
		"💬 Напишите нам — мы ответим на все вопросы!"
	)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)