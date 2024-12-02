# config.py

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# 数据库连接字符串
DATABASE_URL = os.getenv('DATABASE_URL')

# 区块链节点 URL
ETH_NODE_URL = os.getenv('ETH_NODE_URL')
BSC_NODE_URL = os.getenv('BSC_NODE_URL')
TRON_NODE_URL = os.getenv('TRON_NODE_URL')
SOLANA_NODE_URL = os.getenv('SOLANA_NODE_URL')
SUI_NODE_URL = os.getenv('SUI_NODE_URL')
