# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    registered_at = Column(DateTime, default=datetime.datetime.utcnow)

    wallets = relationship("Wallet", back_populates="owner")

class Wallet(Base):
    __tablename__ = 'wallets'

    wallet_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    wallet_address = Column(String, index=True)
    blockchain_type = Column(String)
    added_at = Column(DateTime, default=datetime.datetime.utcnow)
    monitor = Column(Boolean, default=True)
    owner = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")



class Transaction(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey('wallets.wallet_id'))
    tx_hash = Column(String, index=True)
    details = Column(String)
    timestamp = Column(DateTime)
    
    wallet = relationship("Wallet", back_populates="transactions")
