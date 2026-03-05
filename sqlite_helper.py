# helper to push and pull data from the sqlite server in home assistant

import sqlite3


class VoucherWalletDatabase:
    def __init__(self, db_path='voucher_wallet.db'):
        self.db_path = db_path
        
        # Initialize the database and create the vouchers table if it doesn't exist
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS vouchers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code INTEGER NOT NULL,
                    value REAL NOT NULL,
                    redeemed BOOLEAN NOT NULL CHECK (redeemed IN (0, 1))
                )
            ''')
            conn.commit()

    def add_voucher(self, code: int, value: float, redeemed: bool=False):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO vouchers (code, value, redeemed) VALUES (?, ?, ?)', (code, value, redeemed))
            conn.commit()

    def remove_voucher(self, code: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM vouchers WHERE code = ?', (code,))
            conn.commit()