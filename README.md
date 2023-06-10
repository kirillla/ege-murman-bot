# EGE-Bot ниже на русском языке

This project is a Telegram bot for viewing EGE (Unified State Exam) results from the gia.edunord.ru website.

## Installation

1. Install the necessary dependencies by running the following command:

   ```
   pip install aiogram selenium bs4 lxml
   ```

2. Download the Chrome WebDriver and place the executable file in the driver's path. Make sure you have Google Chrome installed.

3. Run the `main.py` file to start the bot:

   ```
   python main.py
   ```

## Usage

1. Add your Telegram bot token to the `token` variable in the `main.py` file.

2. When the bot is launched, it will respond to the `/start` command.

3. The bot will prompt the user for EGE result access credentials, such as last name, first name, patronymic, passport series, and number.

4. After entering the data, the bot will make a request to the official EGE website and display the exam results.

5. The user can change the data by sending the `/change` command.

## Contact

You can contact the project developer using the following contacts:
- Telegram: [@memr404]
- Email: [memr404@gmail.com]




# ЕГЭ-бот

Этот проект представляет собой телеграм-бот для просмотра результатов ЕГЭ c сайта gia.edunord.ru

## Установка

1. Установите необходимые зависимости, запустив команду:

   ```
   pip install aiogram selenium bs4 lxml
   ```

2. Скачайте Chrome WebDriver и поместите исполняемый файл в путь к драйверу. Убедитесь, что у вас установлен Google Chrome.

3. Запустите файл `main.py`, чтобы запустить бота:

   ```
   python main.py
   ```

## Использование

1. Добавьте токен вашего телеграм-бота в переменную `token` в файле `main.py`.

2. При запуске бота, он будет отвечать на команду `/start`.

3. Бот будет запрашивать у пользователя данные для доступа к результатам ЕГЭ, такие как фамилия, имя, отчество, серия и номер паспорта.

4. После ввода данных, бот выполнит запрос на официальном сайте ЕГЭ и выведет результаты экзаменов.

5. Пользователь может изменить данные, отправив команду `/change`.



## Связь

Вы можете связаться с разработчиком проекта, используя следующие контакты:
- Телеграм: [@memr404]
- Email: [memr404@gmail.com]
