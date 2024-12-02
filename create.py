# create_empty_files.py

import os

# 要创建的文件列表
files = [
    'bot.py',
    'config.py',
    'db.py',
    'models.py',
    'handlers.py',
    'utils.py',
    'logger.py',
    'setup.py',
    'scheduler.py',
    'requirements.txt',
    'messages.py',
    '.gitignore',
    'README.md',
    'blockchain/eth_bsc.py',
    'blockchain/tron.py',
    'blockchain/solana.py',
    'blockchain/sui.py',
    'blockchain/__init__.py'
]

# 创建文件并确保目录存在
for file_path in files:
    # 提取目录名
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"已创建目录：{directory}")
    
    # 创建空文件
    with open(file_path, 'w', encoding='utf-8') as f:
        pass  # 文件内容为空
    print(f"已创建文件：{file_path}")

print("所有文件已创建完成。")
