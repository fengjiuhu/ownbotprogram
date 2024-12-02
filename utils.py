# utils.py
import re

def sanitize_input(input_str):
    # 对用户输入进行清理，防止 SQL 注入等攻击
    pass

def validate_wallet_address(address: str, blockchain_type: str) -> bool:
    """
    验证钱包地址的格式是否正确。

    参数:
        address (str): 钱包地址。
        blockchain_type (str): 区块链类型。

    返回:
        bool: 如果地址格式正确，返回 True，否则返回 False。
    """
    if blockchain_type == 'eth' or blockchain_type == 'bsc':
        # 以太坊和 BSC 地址验证
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return re.match(pattern, address) is not None
    elif blockchain_type == 'tron':
        # TRON 地址验证，Base58 编码，T 开头
        pattern = r'^T[a-zA-Z0-9]{33}$'
        return re.match(pattern, address) is not None
    elif blockchain_type == 'solana':
        # Solana 地址验证，Base58 编码，长度在 32 到 44 之间
        return 32 <= len(address) <= 44
    elif blockchain_type == 'sui':
        # Sui 地址验证，假设为 0x 开头的 64 位十六进制字符串
        pattern = r'^0x[a-fA-F0-9]{64}$'
        return re.match(pattern, address) is not None
    else:
        return False
