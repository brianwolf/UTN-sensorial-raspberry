import os
import sqlite3
from typing import List

import logic.vars as vars


def select(query: str, params: List[any] = []) -> List[any]:

    conn = _get_connection()

    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    cursor.close()
    return result


def insert(query: str, params: List[any] = []) -> any:

    conn = _get_connection()

    cursor = conn.cursor()
    cursor.execute(query, params)
    id_inserted = cursor.lastrowid1

    conn.commit()
    cursor.close()

    return id_inserted


def exec(query: str, params: List[any] = []) -> List[any]:

    conn = _get_connection()

    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    conn.commit()
    cursor.close()

    return result


def exec_script(script_path: str) -> List[any]:

    with open(script_path, 'r') as f:
        query = f.read()

    conn = _get_connection()

    cursor = conn.cursor()
    cursor.executescript(query)
    result = cursor.fetchall()

    conn.commit()
    cursor.close()

    return result


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _get_connection() -> sqlite3.Connection:

    if not os.path.exists(vars.SQLITE_PATH):
        directory = os.path.dirname(vars.SQLITE_PATH)
        os.makedirs(directory, exist_ok=True)

    con = sqlite3.connect(vars.SQLITE_PATH, check_same_thread=True)
    con.row_factory = _dict_factory

    return con
