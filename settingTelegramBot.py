import random
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import time
import get
from main import start

bot = telegram.Bot(token='')

# Глобальная переменная для хранения последних результатов
last_results = {}


def load_blacklist():
    """Загружает черный список из файла"""
    try:
        with open('blackList.txt', 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f.readlines() if line.strip())
    except FileNotFoundError:
        return set()


def filter_blacklisted_items(result):
    """Фильтрует элементы, удаляя те, что есть в черном списке"""
    blacklist = load_blacklist()
    filtered_result = [item for item in result if str(item) not in blacklist]
    return filtered_result


async def send_message(message, list_chat_id, result):
    # Создаем клавиатуру с кнопками
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить", callback_data='confirm')],
        [InlineKeyboardButton("❌ Отклонить", callback_data='reject')],
        #[InlineKeyboardButton("ℹ️ Информация", callback_data='info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    for chat_id in list_chat_id:
        chat_id = chat_id.strip()
        if chat_id:  # Проверяем, что chat_id не пустой
            sent_message = await bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=reply_markup
            )
            # Сохраняем результат для этого сообщения
            last_results[sent_message.message_id] = result


async def handle_callback(update, context):
    query = update.callback_query
    await query.answer()

    # Получаем сохраненный результат для этого сообщения
    message_id = query.message.message_id
    result = last_results.get(message_id, [])

    # Обработка разных типов нажатий
    if query.data == 'confirm':
        print("Подтверждение!!!")
        await query.edit_message_text(text=f"✅ Вы подтвердили: {query.message.text}")
    elif query.data == 'reject':
        print("Отклонение! Добавляем в черный список...")

        # Добавляем все элементы result в blackList.txt
        if result:
            try:
                blacklist = load_blacklist()
                new_items = [item for item in result if str(item) not in blacklist]

                if new_items:
                    with open('blackList.txt', 'a', encoding='utf-8') as f:
                        for item in new_items:
                            f.write(f"{item}\n")
                    print(f"Добавлено {len(new_items)} элементов в черный список")
                else:
                    print("Все элементы уже находятся в черном списке")

            except Exception as e:
                print(f"Ошибка при записи в blackList.txt: {e}")

        await query.edit_message_text(
            text=f"❌ Вы отклонили: {query.message.text}\n\nДобавлено в черный список: {len(result)} элементов")

        # Удаляем из памяти после обработки
        if message_id in last_results:
            del last_results[message_id]

    elif query.data == 'info':
        await query.edit_message_text(text=f"ℹ️ Дополнительная информация: {query.message.text}")

        # Удаляем из памяти после обработки
        if message_id in last_results:
            del last_results[message_id]


async def main():
    countJobing = 0

    # Добавляем обработчик callback-ов
    from telegram.ext import Application, CallbackQueryHandler
    application = Application.builder().token('8294916518:AAF_5V2yr9Z3EanACcgK0Uu1up8vuYmi08Q').build()
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Запускаем обработчик в фоне
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    while True:
        with open('chat_id.txt', 'r', encoding='utf-8') as file:
            list_chat_id = file.readlines()

        result = start()
        if len(result) != 0:
            # Фильтруем элементы через черный список
            filtered_result = filter_blacklisted_items(result)

            if filtered_result:  # Если есть элементы после фильтрации
                print("До фильтрации:", result)
                print("После фильтрации:", filtered_result)
                message = '\n'.join(str(i) for i in filtered_result)
                print("Отправляем сообщение:", message)
                await send_message(message, list(set(list_chat_id)), filtered_result)
            else:
                print("Все элементы находятся в черном списке, сообщение не отправляется")
        else:
            print("Нет результатов для обработки")


        await asyncio.sleep(random.randint(30, 60))


if __name__ == '__main__':
    asyncio.run(main())