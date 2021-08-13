import logic.repository as repo
import logic.sqlite as sqlite
import logic.config as config

_SCRIPT_DB_PATH = 'db/script.sql'


def prepare_deploy():
    _init_db()


def _init_db():

    try:
        sqlite.select(query=f'SELECT 1 FROM {repo._TABLE}')

    except Exception:
        config.logger().info('SQLite -> creating DB')
        sqlite.exec_script(_SCRIPT_DB_PATH)
