# blockchain/sui.py

import requests
from config import SUI_NODE_URL

def get_sui_transactions(address):
    """
    获取指定 Sui 地址的交易记录。

    参数:
        address (str): Sui 钱包地址。

    返回:
        list: 交易记录列表，每个元素是一个字典，包含交易哈希等信息。
    """
    try:
        # Sui 目前可能没有官方的 Python SDK，需要使用 HTTP 请求

        # 构建请求 URL，假设 Sui 提供 REST API
        # 需要根据 Sui 的实际 API 文档进行调整

        api_url = f"{SUI_NODE_URL}/transactions?owner={address}"

        headers = {
            'Content-Type': 'application/json',
            # 如果需要 API Key，可以在这里添加
            # 'Authorization': 'Bearer YOUR_API_KEY'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        transactions = data.get('transactions', [])

        tx_list = []
        for tx in transactions:
            tx_data = {
                'hash': tx.get('digest'),
                'from': tx.get('sender'),
                'to': tx.get('recipient'),
                'amount': tx.get('amount'),
                'timestamp': tx.get('timestamp_ms')
            }
            tx_list.append(tx_data)

        return tx_list
    except Exception as e:
        print(f"获取 Sui 交易时发生错误：{e}")
        return []
