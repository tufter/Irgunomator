import logging

import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import handler_filters
import handlers
from config import config


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_handlers():
    start_handler = CommandHandler('start', handlers.start.start)
    help_handler = CommandHandler('help', handlers.start.start)
    support_handler = CommandHandler('support', handlers.support.support)
    list_requests = CommandHandler('list', handlers.list_requests.list_requests)
    close_request = CommandHandler('close', handlers.close.close)
    flush_db_handler = CommandHandler('flushdb', handlers.flush_db.flush_db)
    leaderboards_handler = CommandHandler('leaderboards', handlers.leaderboards.show_leaderboard)
    unknown_handler = MessageHandler([Filters.command], handlers.unknown.unknown)
    new_request_handler = MessageHandler([handler_filters.new_request], handlers.new_request.new_request)
    flush_db_verification_handler = MessageHandler([handler_filters.flush_db], handlers.flush_db.flush_db_reply)

    # Message handler must be the last one
    support_msg_handler = MessageHandler([Filters.text], handlers.support.support_message)

    return [
        start_handler,
        help_handler,
        support_handler,
        list_requests,
        close_request,
        new_request_handler,
        flush_db_handler,
        leaderboards_handler,
        unknown_handler,
        flush_db_verification_handler,
        support_msg_handler]  # NOTE order is important, msg_handler must be last


def get_updater():
    # Connecting to Telegram API
    # Updater retrieves information and dispatcher connects commands
    log.debug("Creating updater with default token...")
    updater = Updater(token=config['DEFAULT']['token'])
    dispatcher = updater.dispatcher

    populate_dispatcher(dispatcher)

    return updater


def populate_dispatcher(dispatcher):
    bot_handlers = get_handlers()
    for bot_handler in bot_handlers:
        dispatcher.add_handler(bot_handler)


def main():
    updater = get_updater()
    log.debug("Stopping polling...")
    updater.stop()
    log.info("Started updater polling.")
    updater.start_polling()


if __name__ == '__main__':
    main()
