# eth_monitor.py

import time
from web3 import Web3
from sqlalchemy.orm import Session
from ..db import get_db
from models import Wallet, Transaction, User
from config import ETH_NODE_URL, TELEGRAM_TOKEN, ETHERSCAN_API_KEY
from telegram import Bot
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import logging

eth_web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
bot = Bot(token=TELEGRAM_TOKEN)

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[
    logging.FileHandler("wallet_scan.log"),
    logging.StreamHandler()
])
logger = logging.getLogger()

# 全局时间标记，用于记录上次 API 调用的时间
last_api_call_time = 0
API_CALL_INTERVAL = 1  # 每秒允许一次 API 调用

def get_eth_transactions(wallet_addresses):
    global last_api_call_time
    current_time = time.time()

    # 如果距离上次调用时间不到 1 秒，则等待
    if current_time - last_api_call_time < API_CALL_INTERVAL:
        time.sleep(API_CALL_INTERVAL - (current_time - last_api_call_time))

    try:
        # 构建查询地址，合并所有钱包地址到一个 API 调用中
        addresses = ','.join(wallet_addresses)
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={addresses}&sort=desc&apikey={ETHERSCAN_API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # 更新上次 API 调用时间
        last_api_call_time = time.time()

        if data['status'] == '1':
            return data['result']  # 返回交易列表
        else:
            logger.error(f"错误：{data['message']}")
            return []
    except Exception as e:
        logger.error(f"获取交易时出错：{e}")
        return []

def monitor_eth_wallets():
    db_session: Session = next(get_db())
    wallets = db_session.query(Wallet).filter(Wallet.blockchain_type == 'eth', Wallet.monitor == True).all()

    # 将钱包地址按用户进行归类，方便合并查询
    wallet_dict = {}
    for wallet in wallets:
        if wallet.user_id not in wallet_dict:
            wallet_dict[wallet.user_id] = []
        wallet_dict[wallet.user_id].append(wallet.wallet_address)

    for user_id, wallet_addresses in wallet_dict.items():
        # 使用合并后的地址列表进行查询
        transactions = get_eth_transactions(wallet_addresses)
        
        for transaction in transactions:
            tx_hash = transaction['hash']
            wallet_address = transaction.get('to') or transaction.get('from')

            # 获取钱包对象
            wallet = db_session.query(Wallet).filter(Wallet.wallet_address == wallet_address, Wallet.user_id == user_id).first()
            if not wallet:
                continue

            # 检查数据库中是否已有此交易
            existing_transaction = db_session.query(Transaction).filter(
                Transaction.tx_hash == tx_hash,
                Transaction.wallet_id == wallet.wallet_id
            ).first()

            if not existing_transaction:
                # 新交易，添加到数据库
                new_transaction = Transaction(
                    wallet_id=wallet.wallet_id,
                    tx_hash=tx_hash,
                    details=str(transaction),
                    timestamp=datetime.utcnow()
                )
                db_session.add(new_transaction)
                db_session.commit()

                # 构建并发送通知（使用 Markdown 格式）
                message = (
                    f"您的钱包 {wallet.wallet_address} 有新的交易：\n"
                    f"[交易哈希](https://etherscan.io/tx/{tx_hash})：{tx_hash}\n"
                    f"[发送方](https://etherscan.io/address/{transaction['from']})：{transaction['from']}\n"
                    f"[接收方](https://etherscan.io/address/{transaction['to']})：{transaction['to']}\n"
                    f"数量：{transaction.get('value', '未知')}"
                )
                bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
                logger.info(f"已通知用户 {user_id} 有新的交易。")

    db_session.close()

# 启动调度器
scheduler = BackgroundScheduler()
scheduler.add_job(monitor_eth_wallets, 'interval', seconds=10)  # 每 10 秒执行一次
scheduler.start()

# 保持主线程运行
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    logger.info("调度器已关闭。")