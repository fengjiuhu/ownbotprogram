# blockchain/solana.py

from solana.rpc.api import Client
from config import SOLANA_NODE_URL

# 初始化 Solana 客户端
solana_client = Client(SOLANA_NODE_URL)

def get_solana_transactions(address):
    """
    获取指定 Solana 地址的交易记录。

    参数:
        address (str): Solana 钱包地址。

    返回:
        list: 交易记录列表，每个元素是一个字典，包含交易哈希等信息。
    """
    try:
        # 获取交易签名列表
        response = solana_client.get_signatures_for_address(address)
        signatures = response.get('result', [])

        tx_list = []
        for sig_info in signatures:
            signature = sig_info['signature']
            # 获取交易详情
            tx_response = solana_client.get_transaction(signature)
            if tx_response.get('result'):
                tx_data = {
                    'hash': signature,
                    'slot': tx_response['result']['slot'],
                    'block_time': tx_response['result']['blockTime'],
                    'meta': tx_response['result']['meta']
                }
                tx_list.append(tx_data)
        return tx_list
    except Exception as e:
        print(f"获取 Solana 交易时发生错误：{e}")
        return []
