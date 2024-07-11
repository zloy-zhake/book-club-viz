.PHONY: help

help:             ## Показать список команд
	@echo ""
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo ""

create_venv:      ## Создать виртуальное окружение
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install

create_dev_venv:      ## Создать виртуальное окружение для разработки
	POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install --with dev

run_chitaem_vmeste_app:  ## Запустить сервис
	poetry run streamlit run chitaem_vmeste_st_app.py

# run_api:          ## Запустить API локально
# 	poetry run python spam_detector_api

# run_app:          ## Запустить сервис локально
# 	poetry run python spam_detector_app

# build_api_image:  ## Собрать образ с API
# 	docker build --file api.Dockerfile --tag spam-detector-api .

# run_api_image:    ## Запустить образ с API в контейнере
# 	docker run --publish 8001:8001 spam-detector-api

# build_app_image:  ## Собрать образ с сервисом
# 	docker build --file app.Dockerfile --tag spam-detector-app .

# run_compose_up:   ## Запустить контейнеры api и сервиса с помощью docker-compose
# 	docker compose --file compose-local.yml up

# run_compose_down: ## Остановить контейнеры api и сервиса, запущенные с помощью docker-compose
# 	docker compose --file compose-local.yml down

# run_tests:        ## Запустить тесты
# 	PYTHONPATH=. poetry run python -m pytest