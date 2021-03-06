import logging
import os

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from Handlers import commandhandlers
from Handlers import messagehandlers
from conf.settings import TELEGRAM_TOKEN
from features import request

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot:

    def __init__(self, offenseOn, muteOn):
        self.offenseOn = offenseOn
        self.mute = muteOn


bender_bot = Bot(False, False)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    request.DontStopmeNOW()

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    # updater.start_polling()

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', commandhandlers.start))
    dispatcher.add_handler(CommandHandler('mute_', commandhandlers.mute_))
    dispatcher.add_handler(CommandHandler('unmute', commandhandlers.unmute))
    dispatcher.add_handler(CommandHandler('help', commandhandlers.help))

    echo_handler = MessageHandler(Filters.text & (~Filters.command), messagehandlers.echo)
    dispatcher.add_handler(echo_handler)
    sys_handler = MessageHandler(Filters.status_update, messagehandlers.empty_message)
    dispatcher.add_handler(sys_handler)
    dispatcher.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TELEGRAM_TOKEN)
    updater.bot.setWebhook('https://bender-opencv.herokuapp.com/' + TELEGRAM_TOKEN)

    updater.idle()


if __name__ == "__main__":
    main()
