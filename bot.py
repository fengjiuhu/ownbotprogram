# bot.py

from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN
from handlers import start, help_command, add_wallet, remove_wallet, list_wallets

def main():
    # 创建 Updater 并传入机器人令牌
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    
    # 获取调度器来注册处理程序
    dp = updater.dispatcher
    
    # 注册命令处理程序
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("addwallet", add_wallet))
    dp.add_handler(CommandHandler("removewallet", remove_wallet))
    dp.add_handler(CommandHandler("listwallets", list_wallets))
    
    # 启动机器人
    updater.start_polling()
    
    # 运行直到按下 Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
