help: ## - Получить информацию о командах
	@sed \
		-e '/^[a-zA-Z0-9_\-]*:.*##/!d' \
		-e 's/:.*##\s*/:/' \
		-e 's/^\(.\+\):\(.*\)/$(shell tput setaf 6)\1$(shell tput sgr0):\2/' \
		$(MAKEFILE_LIST) | column -c2 -t -s :

run: ## - Запустить docker-compose
	docker-compose -f docker_compose/docker-compose.yaml up --build -d

stop: ## - Остановить и удалить docker-compose
	docker-compose -f docker_compose/docker-compose.yaml down

collectstatic: ## - Забрать статику
	docker-compose -f docker_compose/docker-compose.yaml exec movies_admin python manage.py collectstatic --no-input --clear

flush: ## - Очистить бд
	docker-compose -f docker_compose/docker-compose.yaml exec movies_admin python manage.py flush --no-input

migrate: ## - Создать бд
	docker-compose -f docker_compose/docker-compose.yaml exec movies_admin python manage.py migrate

load_data: ## - Заполнить бд
	docker-compose -f docker_compose/docker-compose.yaml exec movies_admin python sqlite_to_postgres/load_data.py
	docker-compose -f docker_compose/docker-compose.yaml exec movies_admin sh -c "python -m pytest -p no:cacheprovider tests/*"

superuser: ## - Создать superuser
	docker-compose -f docker_compose/docker-compose.yaml exec movies_admin python manage.py createsuperuser --username=web --email=web@example.com

movies_admin: ## - Выполнить полный запуск movies_admin
	make run
	make collectstatic
	make flush
	make migrate
	make load_data
#	make superuser

clean: ## - Очистить docker
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker images -q)
