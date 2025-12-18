# Импортируем необходимые инструменты из библиотеки для работы с Telegram
import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Вставляем сюда ТОКЕН, который мы получили от BotFather
BOT_TOKEN = "8450460586:AAFXV-qRVEm0-MYt93R9SZwjBPpCEtDv8N0"  # <-- Убедитесь, что токен верный!

# 1. Функция приветствия. Срабатывает на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем кнопку, которая будет открывать наше мини-приложение
    keyboard = [
        [InlineKeyboardButton("🛍️ Открыть каталог", web_app=WebAppInfo(url="https://bandito-camp-bot.vercel.app"))]
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
    try:
        # Получаем данные, которые пользователь отправил из формы в мини-приложении
        data_json = update.effective_message.web_app_data.data
        print(f"DEBUG: Получены сырые данные из WebApp: {data_json}")  # Логирование для отладки
        
        # Парсим JSON строку в словарь Python
        data = json.loads(data_json)
        
        # Форматируем красивое сообщение для администратора
        admin_message = (
            "🎉 *НОВЫЙ ЗАКАЗ!*\n\n"
            f"*Товар:* {data.get('item', 'Не указано')}\n"
            f"*Размер:* {data.get('size', 'Не указан')}\n"
            f"*Цена:* {data.get('price', 'Не указана')}\n"
            f"*Контакт:* {data.get('contact', 'Не указан')}\n"
            f"*ID пользователя:* {data.get('user_id', 'Не доступен')}\n"
            f"*Время:* {update.effective_message.date}"
        )
        
        # Здесь мы можем эту информацию обработать.
        # Например, отправить себе (администратору) в личные сообщения.
        admin_chat_id = "402403714"  # <-- Убедитесь, что это ваш верный ID!
        
        try:
            # Отправляем сообщение администратору
            await context.bot.send_message(
                chat_id=admin_chat_id,
                text=admin_message,
                parse_mode="Markdown"  # Для форматирования текста
            )
            print(f"DEBUG: Сообщение отправлено администратору {admin_chat_id}")
        except Exception as e:
            print(f"ОШИБКА при отправке администратору: {e}")
        
        # И отправить подтверждение пользователю
        await update.effective_message.reply_text(
            "✅ Спасибо! Ваша заявка принята.\n"
            "Продавец свяжется с вами в Telegram в ближайшее время."
        )
        print(f"DEBUG: Подтверждение отправлено пользователю")
        
    except json.JSONDecodeError as e:
        print(f"ОШИБКА: Не удалось распарсить JSON: {e}, данные: {data_json}")
        await update.effective_message.reply_text("❌ Произошла ошибка при обработке заказа. Попробуйте еще раз.")
    except Exception as e:
        print(f"ОШИБКА в web_app_data: {e}")
        await update.effective_message.reply_text("❌ Произошла непредвиденная ошибка. Попробуйте позже.")

# 3. Главная функция, которая запускает и настраивает нашего бота
def main():
    # Создаем "приложение" и передаем ему наш токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем наши функции-обработчики
    application.add_handler(CommandHandler("start", start))
    
    # ВАЖНО: Используем MessageHandler для данных из Web App, а не CallbackQueryHandler!
    # filters.StatusUpdate.WEB_APP_DATA - специальный фильтр для данных из мини-приложений
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Запускаем бота в режиме "опрос сервера" (polling)
    print("Бот запущен и слушает сообщения...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Это точка входа. Если мы запускаем этот файл напрямую, выполнится main()
if __name__ == '__main__':
    main()
