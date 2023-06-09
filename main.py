import sqlite3, datetime, asyncio, logging
from bs4 import BeautifulSoup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import RestrictChatMember
from aiogram.types import ChatActions
from aiogram.utils.markdown import hlink

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

token = "" # Ваш токен

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

global start_text
start_text = """
👋Добро пожаловать в бота ЕГЭ-Мурманск! Здесь вы найдете надежного спутника в вашем пути к успеху на экзамене ЕГЭ. Наша цель - облегчить вам доступ к результатам и помочь вам эффективно управлять своим образовательным процессом.
✅Забудьте о долгих поисках и неудобных интерфейсах. Бот предлагает вам удобную и мгновенную возможность получать свои результаты прямо здесь, в телеграме.
Оптимизируйте свое время!\n\n🚀Не теряйте времени и присоединяйтесь к нашему боту уже сегодня. Вперед, к новым достижениям и лучшему будущему!
"""

class go(StatesGroup):
	reg1 = State()
	reg2 = State()
	reg3 = State()
	reg4 = State()
	reg5 = State()
	
@dp.message_handler()
async def start(message: types.Message,state: FSMContext):
	global connect
	connect = sqlite3.connect('users.db', check_same_thread=False)
	global cursor
	cursor= connect.cursor()

	if message.text == '/start':
		today = datetime.datetime.today()
		f = 'Старт '+ str(message.chat.id) + ' ' + today.strftime("%Y-%m-%d-%H.%M.%S")
		print(f)
		
		cursor.execute("""CREATE TABLE IF NOT EXISTS users(
				id INTEGER, username TEXT, fam TEXT, name TEXT, otch TEXT, ser TEXT, num TEXT 
			)""")
		connect.commit()
		
		userid = message.chat.id
		cursor.execute(f"SELECT * FROM users WHERE id = {userid}")
		data = cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO users(id, username, fam) VALUES(?,?,?);", (message.chat.id, message.chat.username,'None'))
			connect.commit()
			await bot.send_message(message.chat.id, start_text)
			await reg(message, state)
		elif data[2] == 'None':
			await reg(message, state)
		else:
			await mainmenu(message, state)

	elif message.text == '/change':
		await reg(message, state)


async def reg(message,state: FSMContext):
	await bot.send_message(message.chat.id, '📊Введите <i>фамилию</i>:','HTML')
	await go.reg1.set()

@dp.message_handler(state=go.reg1)
async def reg1(message,state: FSMContext):
	async with state.proxy() as data:
		data['fam'] = message.text
	await message.delete()
	await bot.send_message(message.chat.id, '📊Введите <i>имя</i>:','HTML')
	await go.reg2.set()

@dp.message_handler(state=go.reg2)
async def reg2(message,state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await message.delete()
	await bot.send_message(message.chat.id, '📊Введите <i>отчество</i>:','HTML')
	await go.reg3.set()

@dp.message_handler(state=go.reg3)
async def reg3(message,state: FSMContext):
	async with state.proxy() as data:
		data['otch'] = message.text
	await message.delete()
	await bot.send_message(message.chat.id, '#️⃣Введите <i>серию</i> паспорта:','HTML')
	await go.reg4.set()

@dp.message_handler(state=go.reg4)
async def reg4(message,state: FSMContext):
	async with state.proxy() as data:
		data['ser'] = message.text
	await message.delete()
	await bot.send_message(message.chat.id, '#️⃣Введите <i>номер</i> паспорта:','HTML')
	await go.reg5.set()

@dp.message_handler(state=go.reg5)
async def reg5(message,state: FSMContext):
	async with state.proxy() as data:
		fam = data['fam']
		name = data['name']
		otch = data['otch']
		ser = data['ser']
	num = message.text
	await state.finish()
	await message.delete()
	try:
		test = int(ser)
		test = int(num)
	except ValueError:
		cursor.execute(f"UPDATE users SET fam = 'None' WHERE id = " + str(message.chat.id))
		connect.commit()
		await bot.send_message(message.chat.id, '⛔️Вы ввели неправильные данные!')
		await reg(message, state)
	else:
		cursor.execute(f"UPDATE users SET fam = '{fam}' WHERE id = " + str(message.chat.id))
		cursor.execute(f"UPDATE users SET name = '{name}' WHERE id = " + str(message.chat.id))
		cursor.execute(f"UPDATE users SET otch = '{otch}' WHERE id = " + str(message.chat.id))
		cursor.execute(f"UPDATE users SET ser = '{ser}' WHERE id = " + str(message.chat.id))
		cursor.execute(f"UPDATE users SET num = '{num}' WHERE id = " + str(message.chat.id))
		connect.commit()

		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text="✅Всё верно", callback_data="yes"))
		keyboard.add(types.InlineKeyboardButton(text="🔄Нужно исправить", callback_data="no"))
		text = f'🔎Проверьте данные:\n\n<b>Фамилия</b>: {fam}\n<b>Имя</b>: {name}\n<b>Отчество</b>: {otch}\n<b>Серия паспорта</b>: <i>{ser}</i>\n<b>Номер паспорта</b>: <i>{num}</i>'
		await bot.send_message(message.chat.id, text, 'HTML', reply_markup=keyboard)


@dp.callback_query_handler(text="yes")
async def yes(call: types.CallbackQuery,state: FSMContext):
	await call.message.edit_text(text="⏱Ваш запрос выполняется...\n\n☕️Вы можете пока что выйти из чата, загрузка может занять много времени (от 1 до 10 минут)\n\n⚠️Начиная с 6 июня, бот будет работать быстрее")
	await zapr(call.message,state)

@dp.callback_query_handler(text="no")
async def no(call: types.CallbackQuery,state: FSMContext):
	await call.message.delete()
	await reg(call.message, state)


async def zapr(message,state: FSMContext):
	today = datetime.datetime.today()
	f = 'Запрос '+ str(message.chat.id) + ' ' + today.strftime("%Y-%m-%d-%H.%M.%S")
	print(f)
	cursor.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
	data = cursor.fetchone()
	options = Options()
	
	options.add_argument("start-maximized")
	options.add_argument("enable-automation")
	options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-browser-side-navigation")
	options.add_argument("--disable-gpu")
	
	driver = webdriver.Chrome(options=options)

	driver.set_page_load_timeout(10)
	try:
		driver.get('http://gia.edunord.ru/res_ege.shtml')
	except:
		#print('except')
		driver.find_element("xpath","//input[@name='fam']").send_keys(data[2])
		driver.find_element("xpath","//input[@name='name']").send_keys(data[3])
		driver.find_element("xpath","//input[@name='otch']").send_keys(data[4])
		driver.find_element("xpath","//input[@name='ser']").send_keys(data[5])
		driver.find_element("xpath","//input[@name='num']").send_keys(data[6])
		#print('ok')
		driver.set_page_load_timeout(1000)
		driver.find_element("xpath","//input[@type='submit']").click()
	page = driver.page_source
	driver.quit()

	if 'Не найдено результатов по вашему запросу' in page:
		cursor.execute(f"UPDATE users SET fam = 'None' WHERE id = " + str(message.chat.id))
		connect.commit()
		await bot.send_message(message.chat.id, '⛔️Вы ввели неправильные данные!')
		await reg(message,state)
	else:
		soup = BeautifulSoup(page, "lxml")
		rez = []
		rezp = []
		for i in soup.find_all('div',attrs={'class':'results'}):
			rezp.append(i.find('h3').text)
			for n in i.find_all('table',attrs={'class':'results-sub'}):
				mask = []
				for j in n.find_all('td'):
					mask.append(j.text)
			rezp.append(mask)
			for h in i.find_all('table',attrs={'class':'results-main'}):
				alll = []
				for d in h.find_all('tr'):
					kek = []
					for nb in d.find_all('font'):
						fff = nb.text
						fff = fff.replace('\t','')
						fff = fff.replace('\n','')
						kek.append(fff)
					alll.append(kek)
				rezp.append(alll)
		rez = rezp
		for i in range(len(rez)//3):
			i = i*3
			text = f"""
			🎓<b>{rez[i]}</b>\n\n
			🔑<b>Маска:</b>\n<i>{rez[i + 1][3]}</i> {rez[i + 1][4]} <b>{rez[i + 1][5]}</b>\n<i>{rez[i+1][6]}</i> {rez[i+1][7]} <b>{rez[i+1][8]}</b>\n\n
			💡<b>Результат:</b>\n<i>{rez[i+2][0][0]}</i>: <code>{rez[i+2][0][1]}</code>\n<i>{rez[i+2][1][0]}</i>: <code>{rez[i+2][1][1]}</code>\n<i>{rez[i+2][2][0]}</i>: <code>{rez[i+2][2][1]}</code>\n<i>{rez[i+2][3][0]}</i>: <code>{rez[i+2][3][1]}</code>
			"""

			await bot.send_message(message.chat.id, text, 'HTML')
		await mainmenu(message,state)

async def mainmenu(message, state):
	cursor.execute(f"SELECT * FROM users WHERE id = {message.chat.id}")
	data = cursor.fetchone()
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="🔎Узнать результаты", callback_data="yes"))
	keyboard.add(types.InlineKeyboardButton(text="🆕Изменить данные", callback_data="no"))
	await bot.send_message(message.chat.id, f'👋Здравствуйте, {data[3]}\nЭто главное меню', reply_markup=keyboard)


async def main():
	await dp.start_polling(bot)


if __name__ == '__main__':
	asyncio.run(main())