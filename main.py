from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import handlers
from config import config


def get_handlers():
    start_handler = CommandHandler('start', handlers.start.start)
    help_handler = CommandHandler('help', handlers.start.start)
    support_handler = CommandHandler('support', handlers.support.support, pass_args=True)
    list_requests = CommandHandler('list', handlers.list_requests.list_requests)
    show_request = CommandHandler('show', handlers.unknown.unknown)
    close_request = CommandHandler('close', handlers.unknown.unknown)
    unknown_handler = MessageHandler([Filters.command], handlers.unknown.unknown)
    # Message handler must be the last one
    support_msg_handler = MessageHandler([Filters.text], handlers.support.support_message)

    return [start_handler, help_handler, support_handler, list_requests, show_request, close_request,
            unknown_handler, support_msg_handler]


def get_updater():
    # Connecting to Telegram API
    # Updater retrieves information and dispatcher connects commands
    updater = Updater(token=config['DEFAULT']['token'])
    dispatcher = updater.dispatcher

    bot_handlers = get_handlers()

    # populate dispatcher
    for bot_handler in bot_handlers:
        dispatcher.add_handler(bot_handler)

    return updater


def main():
    updater = get_updater()
    updater.stop()
    updater.start_polling()


if __name__ == '__main__':
    main()
