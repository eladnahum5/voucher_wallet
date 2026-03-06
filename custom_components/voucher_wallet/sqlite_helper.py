# helper to push and pull data from the sqlite server in home assistant

import os
import sqlite3

from aiohttp import request
from .const import DOMAIN, VOUCHER_PARAMETERS


class VoucherWalletDatabase:
    def __init__(self, hass):
        self.hass = hass
        db_dir = self.hass.config.path(DOMAIN)
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, f"{DOMAIN}.db")

        # Initialize the database and create the vouchers table if it doesn't exist
        self._initialize_database()

    def _initialize_database(self):
        """
        Create the vouchers table if it doesn't exist with columns based on VOUCHER_PARAMETERS dictionary.
        The dictionary keys will be used as column names and the 'type' field will determine the SQLite data type.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            columns = []
            for param, details in VOUCHER_PARAMETERS.items():
                if details["type"] == "string":
                    columns.append(f"{param} TEXT")
                elif details["type"] == "integer":
                    columns.append(f"{param} INTEGER")
                elif details["type"] == "float":
                    columns.append(f"{param} REAL")
                else:
                    raise ValueError(f"Unsupported data type for parameter '{param}'")
            columns_sql = ", ".join(columns)
            c.execute(f'''
                CREATE TABLE IF NOT EXISTS vouchers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {columns_sql},
                    redeemed BOOLEAN DEFAULT 0
                )
            ''')
            conn.commit()


    def add_voucher(self, data: dict):
        """
        Add a voucher to the database based on VOUCHER_PARAMETERS.
        Example for parameter:
        "name": {
            "type": "string",
            "description": "Name of the voucher",
            "required": True
        },
        The amount of parameters can be changed in the const.py file, and this function will adapt to it
        without known what is required and what is not, it will just insert None for the missing parameters.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            columns = ", ".join(VOUCHER_PARAMETERS.keys())
            placeholders = ", ".join("?" for _ in VOUCHER_PARAMETERS)
            values = [data.get(param) for param in VOUCHER_PARAMETERS]
            c.execute(f'INSERT INTO vouchers ({columns}) VALUES ({placeholders})', values)
            conn.commit()

    def remove_voucher(self, code: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM vouchers WHERE redeem_code = ?', (code,))
            conn.commit()

    def get_all_vouchers(self):
        """Retrieve all vouchers from the database and return them as a list of dictionaries."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM vouchers')
            rows = c.fetchall()
            columns = [description[0] for description in c.description]
            vouchers = [dict(zip(columns, row)) for row in rows]
            return vouchers

    def reinitialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DROP TABLE IF EXISTS vouchers')
            conn.commit()
        self._initialize_database()