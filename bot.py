import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from speech_recognition import Recognizer, AudioFile
import os

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне голосовое сообщение, и я его обработаю.')


def voice_handler(update: Update, context: CallbackContext) -> None:
    voice_file = update.message.voice.get_file()
    voice_file.download('voice.ogg')

    # Распознавание речи
    recognizer = Recognizer()
    with AudioFile('voice.ogg') as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='ru-RU')
        update.message.reply_text(f'Вы сказали: "{text}"')
    except Exception as e:
        update.message.reply_text('Извините, я не смог распознать вашу речь.')


def main() -> None:
    # Вставьте ваш токен
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
