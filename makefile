VERSION ?= local
LOG_FILE_PATH ?= ~/.sensorial/logs/app.log
DB_FILE_PATH ?= ~/.sensorial/db/sqlite.db

.SILENT:

logs-tail lt:
	tail -f $(LOG_FILE_PATH)


logs-clean lc:
	rm -fr $(LOG_FILE_PATH).*
	> $(LOG_FILE_PATH)


db-clean dbc:
	> $(DB_FILE_PATH)


db-size dbs:
	du -ha $(DB_FILE_PATH)


docker-build:
	docker build . -t sensorial-raspberry:${VERSION} --build-arg ARG_VERSION=${VERSION} 


# remover todas las imagenes
# docker images | grep chainz | tr -s ' ' | cut -d ' ' -f 2 | xargs -I {} docker rmi erangaeb/chainz:{}
