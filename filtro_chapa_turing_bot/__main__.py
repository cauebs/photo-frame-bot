from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image

from io import BytesIO
import logging

from . import config


def handle_photo(bot, update, photo=None):
    if photo is None:
        photo = max(update.message.photo, key=lambda x: x.width)

    file = photo.get_file()
    buf = BytesIO()
    file.download(out=buf)

    avatar = Image.open(buf)
    frame = Image.open(config.FRAME_PATH)

    new_frame_height = round((avatar.width / frame.width) * frame.height)
    frame = frame.resize((avatar.width, new_frame_height))

    avatar.paste(frame, box=(0, avatar.height - frame.height), mask=frame)

    buf = BytesIO()
    avatar.save(buf, 'PNG')
    buf.seek(0)
    update.message.reply_photo(buf, caption=config.RESPONSE_CAPTION)

def handle_start(bot, update):
    update.message.reply_text(config.START_MESSAGE)

    profile_photos = update.message.from_user.get_profile_photos().photos
    last_photo = max(profile_photos[0], key=lambda x: x.width)
    handle_photo(bot, update, last_photo)


def run():
    logging.basicConfig()

    updater = Updater(config.TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', handle_start))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    run()
