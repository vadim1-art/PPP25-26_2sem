import requests
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Tuple

URL_1 = 'https://dummyjson.com/posts'
URL_2 = 'https://dummyjson.com/users'
DATA_BASE = 'posts.db'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


def extract(url_posts: str, url_users: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    try:
        response_posts = requests.get(url_posts)
        response_posts.raise_for_status()
        response_users = requests.get(url_users)
        response_users.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Ошибка загрузки данных: {e}")

    return response_posts.json(), response_users.json()


def transform(users: List[Dict[str, Any]], posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    user_map = {user['id']: user['name'] for user in users}
    transformed = []
    now = datetime.now().strftime(DATE_FORMAT)

    for post in posts:
        transformed.append({
            'id': post['id'],
            'title': post['title'],
            'body': post['body'],
            'author': user_map.get(post['userId'], '-'),
            'extracted_time': now
        })
    return transformed


def load(posts: List[Dict[str, Any]]) -> None:
    conn = sqlite3.connect(DATA_BASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT,
            body TEXT,
            author TEXT,
            extracted_time TEXT
        )
    ''')
    cursor.execute('DELETE FROM posts')
    cursor.executemany('''
        INSERT INTO posts (id, title, body, author, extracted_time)
        VALUES (?, ?, ?, ?, ?)
    ''', [(p['id'], p['title'], p['body'], p['author'], p['extracted_time']) for p in posts])
    conn.commit()
    conn.close()


def run_etl() -> None:
    raw_posts, raw_users = extract(URL_1, URL_2)
    transformed_posts = transform(raw_users, raw_posts)
    load(transformed_posts)


def is_data_outdated(conn: sqlite3.Connection, max_age_seconds: int = 30) -> bool:
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT extracted_time FROM posts ORDER BY extracted_time DESC LIMIT 1")
        row = cursor.fetchone()
        if row is None:
            return True  # таблица пуста
        last_time = datetime.strptime(row[0], DATE_FORMAT)
        return (datetime.now() - last_time).total_seconds() >= max_age_seconds
    except sqlite3.OperationalError:
        return True


if __name__ == '__main__':
    try:
        conn = sqlite3.connect(DATA_BASE)
        if is_data_outdated(conn):
            run_etl()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
            if cursor.fetchone() is None:
                print('Записано')
            else:
                print('Обновлено')
        conn.close()
    except Exception as e:
        print(f"Критическая ошибка: {e}")