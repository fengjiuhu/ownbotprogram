Blockchain Wallet Transaction Tracker Telegram Bot
Project Overview
This is a Telegram bot that allows users to add and remove blockchain wallet addresses they wish to track. The bot supports the following blockchains:

TRON
Solana
Sui
Ethereum
Binance Smart Chain (BSC)
The bot periodically checks the transactions of these wallets and notifies users when new transactions are detected.

Features
Add/Remove Wallets: Users can add or remove wallet addresses through simple commands.
Multi-Blockchain Support: Supports tracking wallets across multiple blockchains.
Real-Time Notifications: Sends Telegram messages to users when new transactions are detected.
Data Persistence: Stores user data and wallet addresses in an SQL database.
Secure: Sensitive information is stored securely using environment variables.
Installation
Prerequisites
Python 3.6 or higher
PostgreSQL database (or SQLite for development/testing)
Telegram account to interact with the bot
Steps
Clone the Repository


git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
Install Dependencies

Install the required Python packages using pip:


pip install -r requirements.txt
Configure Environment Variables

Copy the .env.example file to .env:


cp .env.example .env
Open the .env file and fill in the required configuration parameters:


TELEGRAM_TOKEN=your-telegram-bot-token
DATABASE_URL=postgresql://username:password@localhost:5432/mydatabase
ETH_NODE_URL=https://mainnet.infura.io/v3/your-infura-project-id
BSC_NODE_URL=https://bsc-dataseed.binance.org/
TRON_NODE_URL=https://api.trongrid.io
SOLANA_NODE_URL=https://api.mainnet-beta.solana.com
SUI_NODE_URL=https://your-sui-node-url
Note: Replace placeholders with your actual tokens and URLs.

Initialize the Database

Run the setup script to create the necessary database tables:


python setup.py
Run the Bot

Start the Telegram bot:


python bot.py
Usage
Interact with the bot on Telegram using the following commands:

/start: Register yourself with the bot.
/help: Display help information.
/addwallet <wallet_address> <blockchain_type>: Add a wallet address to track.
Example: /addwallet 0xYourWalletAddress eth
/removewallet <wallet_address>: Remove a wallet address from tracking.
/listwallets: List all your tracked wallet addresses.
Supported Blockchain Types
eth for Ethereum
bsc for Binance Smart Chain
tron for TRON
solana for Solana
sui for Sui
Project Structure
bot.py: Main program to run the Telegram bot.
config.py: Loads configuration parameters from environment variables.
db.py: Database connection and session management.
models.py: Database models for users, wallets, and transactions.
handlers.py: Telegram command handlers.
scheduler.py: Scheduler to periodically check for new transactions.
utils.py: Utility functions, including wallet address validation.
logger.py: Logging configuration.
blockchain/: Directory containing blockchain interaction modules.
eth_bsc.py
tron.py
solana.py
sui.py
requirements.txt: Python dependencies.
.env.example: Example environment variables file.
README.md: Project documentation (this file).
Dependencies
python-telegram-bot
SQLAlchemy
psycopg2-binary
python-dotenv
web3 (for Ethereum and BSC)
tronpy (for TRON)
solana (for Solana)
APScheduler
Other dependencies as listed in requirements.txt
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes with clear messages.
Submit a pull request to the main branch.
License
This project is licensed under the MIT License.
