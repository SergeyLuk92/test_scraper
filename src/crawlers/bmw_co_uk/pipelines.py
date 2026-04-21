import os
import sqlite3
from typing import Any, Dict
from src.crawlers.bmw_co_uk.consts import DB_PATH


class SQLitePipeline:
    def open_spider(self, spider: Any) -> None:
        db_path: str = DB_PATH
        if os.path.exists(db_path):
            os.remove(db_path)
            spider.logger.info(f'🗑️ Removed old database: {db_path}')
        conn: sqlite3.Connection = sqlite3.connect(db_path)
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE bmw_cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                name TEXT,
                mileage TEXT,
                registered TEXT,
                range_value TEXT,
                exterior TEXT,
                fuel TEXT,
                transmission TEXT,
                registration TEXT,
                upholstery TEXT
            )
        ''')
        conn.commit()
        conn.close()
        spider.logger.info(f'✅ Database created: {db_path}')

    def process_item(self, item: Dict[str, Any], spider: Any) -> Dict[str, Any]:
        conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bmw_cars (
                model, name, mileage, registered, range_value,
                exterior, fuel, transmission, registration, upholstery
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('model'),
            item.get('name'),
            item.get('mileage'),
            item.get('registered'),
            item.get('range_value'),
            item.get('exterior'),
            item.get('fuel'),
            item.get('transmission'),
            item.get('registration'),
            item.get('upholstery')
        ))
        conn.commit()
        conn.close()
        spider.logger.info(f'✅ Saved: {item.get("model")} - {item.get("registration")}')
        return item

    def close_spider(self, spider: Any) -> None:
        spider.logger.info('📁 Pipeline closed')
