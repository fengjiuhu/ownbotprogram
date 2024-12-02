# handlers.py

from telegram import Update
from telegram.ext import CallbackContext
from db import get_db
from models import User, Wallet
from sqlalchemy.orm import Session

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    db: Session = next(get_db())
    
    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.user_id == user.id).first()
    if not existing_user:
        # 创建新用户
        new_user = User(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        db.add(new_user)
        db.commit()
        update.message.reply_text(f"欢迎 {user.first_name}！")
    else:
        update.message.reply_text(f"欢迎回来，{user.first_name}！")

def help_command(update: Update, context: CallbackContext):
    help_text = """
可用命令：
/addwallet <钱包地址> - 添加钱包地址
/removewallet <钱包地址> - 删除钱包地址
/listwallets - 列出已添加的钱包地址
/help - 显示帮助信息
"""
    update.message.reply_text(help_text)

def add_wallet(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.message.reply_text("请提供钱包地址和区块链类型，例如：/addwallet <钱包地址> <区块链类型>")
        return
    
    wallet_address = args[0]
    blockchain_type = args[1] if len(args) > 1 else 'eth'  # 默认 eth

    # 验证钱包地址（此处需根据区块链类型添加验证逻辑）
    if not validate_wallet_address(wallet_address, blockchain_type):
        update.message.reply_text("钱包地址格式不正确，请检查后重试。")
        return

    db: Session = next(get_db())
    user_id = update.effective_user.id

    # 检查钱包是否已存在
    existing_wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id,
        Wallet.wallet_address == wallet_address,
        Wallet.blockchain_type == blockchain_type
    ).first()

    if existing_wallet:
        update.message.reply_text("该钱包已在您的列表中。")
    else:
        new_wallet = Wallet(
            user_id=user_id,
            wallet_address=wallet_address,
            blockchain_type=blockchain_type
        )
        db.add(new_wallet)
        db.commit()
        update.message.reply_text(f"已成功添加钱包地址：{wallet_address}")

def remove_wallet(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.message.reply_text("请提供要删除的钱包地址，例如：/removewallet <钱包地址>")
        return
    
    wallet_address = args[0]
    db: Session = next(get_db())
    user_id = update.effective_user.id

    wallet = db.query(Wallet).filter(
        Wallet.user_id == user_id,
        Wallet.wallet_address == wallet_address
    ).first()

    if wallet:
        db.delete(wallet)
        db.commit()
        update.message.reply_text(f"已删除钱包地址：{wallet_address}")
    else:
        update.message.reply_text("未找到该钱包地址。")

def list_wallets(update: Update, context: CallbackContext):
    db: Session = next(get_db())
    user_id = update.effective_user.id

    wallets = db.query(Wallet).filter(Wallet.user_id == user_id).all()
    if wallets:
        wallet_list = '\n'.join([f"{w.wallet_address} ({w.blockchain_type})" for w in wallets])
        update.message.reply_text(f"您已添加的钱包地址：\n{wallet_list}")
    else:
        update.message.reply_text("您还未添加任何钱包地址。")

def validate_wallet_address(address: str, blockchain_type: str) -> bool:
    # 根据区块链类型验证钱包地址格式
    # 这里需要为每种区块链实现地址验证逻辑
    return True  # 简化处理，实际需要完善
