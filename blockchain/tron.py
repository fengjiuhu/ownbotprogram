# blockchain/tron.py

from tronpy import Tron
from tronpy.keys import to_base58check_address
from config import TRON_NODE_URL
import requests

# 初始化 TRON 客户端
tron_client = Tron(provider=TRON_NODE_URL)

def get_tron_transactions(address):
    """
    获取指定 TRON 地址的交易记录。

    参数:
        address (str): TRON 钱包地址。

    返回:
        list: 交易记录列表，每个元素是一个字典，包含交易哈希等信息。
    """
    try:
        # 将地址转换为 hex 格式
        hex_address = tron_client.address.to_hex(address)

        # 调用 API 获取交易列表
        # 注意：TRON 不支持通过节点直接获取所有交易，需要使用第三方 API
        # 这里假设您有一个 API 可以获取交易列表
        # 以下代码仅供参考，需要根据实际的 API 进行调整

        # 示例 API URL（需替换为实际可用的 API）
        api_url = f"https://api.trongrid.io/v1/accounts/{address}/transactions"

        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        transactions = data.get('data', [])

        tx_list = []
        for tx in transactions:
            tx_data = {
                'hash': tx.get('txID'),
                'from': tx.get('raw_data', {}).get('contract', [])[0].get('parameter', {}).get('value', {}).get('owner_address'),
                'to': tx.get('raw_data', {}).get('contract', [])[0].get('parameter', {}).get('value', {}).get('to_address'),
                'amount': tx.get('raw_data', {}).get('contract', [])[0].get('parameter', {}).get('value', {}).get('amount'),
                'timestamp': tx.get('block_timestamp')
            }
            tx_list.append(tx_data)

        return tx_list
    except Exception as e:
        print(f"获取 TRON 交易时发生错误：{e}")
        return []
