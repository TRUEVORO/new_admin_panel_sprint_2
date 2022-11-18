THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help build up start down destroy stop restart migrate flushmake  collectstatic
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
build:
	docker-compose -f docker-compose.prod.yml build $(c)
up:
	docker-compose -f docker-compose.prod.yml up -d $(c)
start:
	docker-compose -f docker-compose.prod.yml start $(c)
down:
	docker-compose -f docker-compose.prod.yml down $(c)
destroy:
	docker-compose -f docker-compose.prod.yml down -v $(c)
stop:
	docker-compose -f docker-compose.prod.yml stop $(c)
restart:
	docker-compose -f docker-compose.prod.yml stop $(c)
	docker-compose -f docker-compose.prod.yml up -d $(c)
migrate:
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
flush:
	docker-compose -f docker-compose.prod.yml exec web python manage.py flush --no-input
collectstatic:
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear