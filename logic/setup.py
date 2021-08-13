import logic.repository as repo
import logic.sqlite as sqlite

_SCRIPT_DB_PATH = 'db/script.sql'


def prepare_deploy():
    _init_db()


def _init_db():

    try:
        sqlite.select(query=f'SELECT 1 FROM {repo._TABLE}')

    except Exception:
        print('SQLite -> creating DB')
        sqlite.exec_script(_SCRIPT_DB_PATH)
