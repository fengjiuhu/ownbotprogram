# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from db import get_db
from eth_monitor import monitor_eth_wallets
from models import Wallet, Transaction, User
from blockchain import eth_bsc, tron, solana, sui
from telegram import Bot
from config import TELEGRAM_TOKEN
from sqlalchemy.orm import Session
from datetime import datetime
from logger import logger

# 初始化 Telegram 机器人
bot = Bot(token=TELEGRAM_TOKEN)

def check_transactions():
    database_session_generator = get_db()
    database_session: Session = next(database_session_generator)
    wallets = database_session.query(Wallet).all()

    for wallet in wallets:
        user = database_session.query(User).filter(User.user_id == wallet.user_id).first()
        blockchain_type = wallet.blockchain_type
        wallet_address = wallet.wallet_address

        logger.info(f"正在检查用户 {user.user_id} 的钱包 {wallet_address} ({blockchain_type}) 的交易。")

        if blockchain_type == 'eth':
            transactions = eth_bsc.get_ethereum_transactions(wallet_address)
        elif blockchain_type == 'bsc':
            transactions = eth_bsc.get_binance_smart_chain_transactions(wallet_address)
        elif blockchain_type == 'tron':
            transactions = tron.get_tron_transactions(wallet_address)
        elif blockchain_type == 'solana':
            transactions = solana.get_solana_transactions(wallet_address)
        elif blockchain_type == 'sui':
            transactions = sui.get_sui_transactions(wallet_address)
        else:
            logger.warning(f"未知的区块链类型：{blockchain_type}")
            continue

        # 处理获取到的交易记录
        for transaction in transactions:
            transaction_hash = transaction['hash']
            existing_transaction = database_session.query(Transaction).filter(
                Transaction.tx_hash == transaction_hash,
                Transaction.wallet_id == wallet.wallet_id
            ).first()

            if existing_transaction:
                # 已存在的交易，跳过
                continue
            else:
                # 新交易，存入数据库并通知用户
                new_transaction = Transaction(
                    wallet_id=wallet.wallet_id,
                    tx_hash=transaction_hash,
                    details=str(transaction),
                    timestamp=datetime.utcnow()
                )
                database_session.add(new_transaction)
                database_session.commit()

                # 构建通知消息
                message = f"您的钱包 {wallet_address} 上有新的交易：\n\n交易哈希：{transaction_hash}\n区块链类型：{blockchain_type}\n详细信息：{transaction}"
                # 发送通知给用户
                bot.send_message(chat_id=user.user_id, text=message)
                logger.info(f"已通知用户 {user.user_id} 有新的交易。")

    # 关闭数据库会话
    database_session.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # 每一分钟执行一次检查
    scheduler.add_job(check_transactions, 'interval', minutes=1)
    scheduler.start()
    logger.info("调度器已启动，每一分钟检查一次交易。")

if __name__ == '__main__':
    start_scheduler()
