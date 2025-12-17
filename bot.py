# Импортируем необходимые инструменты из библиотеки для работы с Telegram
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Вставляем сюда ТОКЕН, который мы получили от BotFather
BOT_TOKEN = "8450460586:AAFXV-qRVEm0-MYt93R9SZwjBPpCEtDv8N0"  # <-- ПОДСТАВЬ СВОЙ!

# 1. Функция приветствия. Срабатывает на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем кнопку, которая будет открывать наше мини-приложение
    keyboard = [
        [InlineKeyboardButton("🛍️ Открыть каталог", web_app=WebAppInfo(url="https://bandito-camp-bot.vercel.app"))]
        # ПРИМЕЧАНИЕ: Ссылку мы заменим позже, после загрузки приложения на хостинг.
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем пользователю приветственное сообщение с нашей кнопкой
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}!\n"
        "Добро пожаловать в наш магазин одежды! Нажми кнопку ниже, чтобы открыть каталог и выбрать вещь.",
        reply_markup=reply_markup
    )

# 2. Функция обработки данных из мини-приложения
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем данные, которые пользователь отправил из формы в мини-приложении
    data = update.effective_message.web_app_data.data
    # data - это строка в формате JSON. Пример: '{"item":"Футболка", "size":"M", "contact":"@username"}'

    # Здесь мы можем эту информацию обработать.
    # Например, отправить себе (администратору) в личные сообщения.
    admin_chat_id = "402403714"  # <-- ПОДСТАВЬ СВОЙ ID в Telegram
    await context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"🎉 Новый заказ!\nДанные от приложения: {data}\nСвяжись с клиентом!"
    )

    # И отправить подтверждение пользователю
    await update.message.reply_text("Спасибо! Ваша заявка принята. Продавец свяжется с вами в Telegram в ближайшее время.")

# 3. Главная функция, которая запускает и настраивает нашего бота
def main():
    # Создаем "приложение" и передаем ему наш токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем наши функции-обработчики
    application.add_handler(CommandHandler("start", start))
    # Обработчик данных из Web App
    application.add_handler(CallbackQueryHandler(web_app_data))

    # Запускаем бота в режиме "опрос сервера" (polling) - он постоянно спрашивает у Telegram, есть ли для него новые сообщения
    print("Бот запущен и слушает сообщения...")
    application.run_polling()

# Это точка входа. Если мы запускаем этот файл напрямую, выполнится main()
if __name__ == '__main__':

    main()



