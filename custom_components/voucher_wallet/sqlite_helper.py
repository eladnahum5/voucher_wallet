"""This module provides a helper class for managing the SQLite database used by the voucher_wallet custom component in Home Assistant."""

from pathlib import Path
import sqlite3

from homeassistant.core import HomeAssistant

from .const import DOMAIN, ITEM_PARAMETERS, TABLE_NAME


class VoucherWalletDatabase:
    """Helper class for managing the SQLite database for the voucher_wallet component."""

    def __init__(self, hass: HomeAssistant | None) -> None:
        """Initialize the database connection and create the items table if it doesn't exist."""
        self.hass = hass
        db_dir = self.hass.config.path(DOMAIN)
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        self.db_path = Path(db_dir) / f"{DOMAIN}.db"

        # Initialize the database and create the items table if it doesn't exist
        self._initialize_database()

    def _initialize_database(self):
        """Create the items table if it doesn't exist with columns based on ITEM_PARAMETERS dictionary."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            columns = []
            for param, details in ITEM_PARAMETERS.items():
                if details["type"] == "string":
                    columns.append(f"{param} TEXT")
                elif details["type"] == "integer":
                    columns.append(f"{param} INTEGER")
                elif details["type"] == "float":
                    columns.append(f"{param} REAL")
                else:
                    raise ValueError(f"Unsupported data type for parameter '{param}'")
            columns_sql = ", ".join(columns)
            c.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {columns_sql},
                    redeemed BOOLEAN DEFAULT 0
                )
            """)
            conn.commit()

    def _execute_sql_query(self, query: str, params: tuple = ()):
        """Execute a SQL query with optional parameters and return the results."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()
            return c.fetchall()

    def insert_item(self, data: dict):
        """Insert an item into the database based on ITEM_PARAMETERS."""
        columns = ", ".join(ITEM_PARAMETERS.keys())
        placeholders = ", ".join("?" for _ in ITEM_PARAMETERS)
        values = [data.get(param) for param in ITEM_PARAMETERS]
        query = f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({placeholders})"  # noqa: S608
        self._execute_sql_query(query, tuple(values))

    def delete_item_by_code(self, code: int):
        """Delete an item from the database based on its code."""
        query = f"DELETE FROM {TABLE_NAME} WHERE redeem_code = ?"  # noqa: S608
        self._execute_sql_query(query, (code,))

    def fetch_items(self, codes: list[int] | None = None):
        """Fetch items from the database. If codes are provided, fetch only those items; otherwise, fetch all items."""
        if codes:
            placeholders = ", ".join("?" for _ in codes)
            query = f"SELECT * FROM {TABLE_NAME} WHERE redeem_code IN ({placeholders})"  # noqa: S608
            rows = self._execute_sql_query(query, tuple(codes))
        else:
            query = f"SELECT * FROM {TABLE_NAME}"  # noqa: S608
            rows = self._execute_sql_query(query)
        if not rows:
            return []
        columns = [
            description[0]
            for description in sqlite3.connect(self.db_path).cursor().description
        ]
        return [dict(zip(columns, row, strict=False)) for row in rows]

    def reinitialize_database(self):
        """Reinitialize the database by dropping and recreating the items table."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
            conn.commit()
        self._initialize_database()
