import logging
import asyncio
from datetime import time
from pytz import timezone  # Для работы с локальным временем
from telegram.ext import ApplicationBuilder, CommandHandler, JobQueue, ContextTypes
from telegram import Update

# Настройки
TOKEN = '8156209960:AAFWJiIWfBDHPpo6PVqCtDAemyFK4fAHLX8'  # Токен твоего бота
CHANNEL_ID = '-4867904183'  # ID канала или группы

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Функции бота ---

# Ежедневная рассылка
async def send_message(context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="@Kasodochka @annannassikk @RatSalem @Annafelous 🔥 Огонёк!")
        logging.info("✅ Ежедневное сообщение успешно отправлено.")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке ежедневного сообщения: {e}")

# Тестовая команда /send
async def test_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🧪 Это тестовое сообщение!")
        await update.message.reply_text("✅ Сообщение успешно отправлено в канал.")
        logging.info("Тестовое сообщение отправлено в канал.")
    except Exception as e:
        await update.message.reply_text(f"❌ Не удалось отправить сообщение: {e}")
        logging.error(f"Ошибка при отправке тестового сообщения: {e}")

# Назначаем ежедневное задание по локальному времени
def schedule_jobs(job_queue: JobQueue):
    tz = timezone('Europe/Moscow')  # Укажи свой часовой пояс!
    daily_time = time(hour=20, minute=0, tzinfo=tz)  # 20:00 по местному времени
    job_queue.run_daily(send_message, daily_time)
    logging.info(f"⏳ Запланирована ежедневная рассылка на {daily_time.strftime('%H:%M')} по времени {tz}")

# Основная функция запуска бота
async def main():
    try:
        application = ApplicationBuilder().token(TOKEN).build()

        if application.job_queue is None:
            print("⚠️ JobQueue не настроен!")
        else:
            print("✅ JobQueue успешно настроен.")

        # Регистрируем команды
        application.add_handler(CommandHandler("send", test_send))

        # Назначаем задачи
        schedule_jobs(application.job_queue)

        # Инициализация и запуск
        await application.initialize()
        await application.start()
        print("🟢 Бот запущен и ожидает...")

        # Запускаем polling
        await application.updater.start_polling(drop_pending_updates=True)

        # Бесконечное ожидание
        await asyncio.Event().wait()

    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
    finally:
        # Корректно завершаем работу приложения
        await application.stop()
        print("🛑 Бот остановлен.")

# Точка входа
if __name__ == '__main__':
    asyncio.run(main())