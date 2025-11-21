PYTHON := python3
VENV := .venv
APP_MODULE := app.main:app
IMAGE_NAME := alnitak:dev

.PHONY: venv install dev docker-build docker-run docker-stop

venv:
	$(PYTHON) -m venv $(VENV)

install:
	. $(VENV)/bin/activate && pip install -r requirements.txt

dev:
	. $(VENV)/bin/activate && uvicorn $(APP_MODULE) --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run --rm -p 8000:8000 $(IMAGE_NAME)

docker-stop:
	docker ps -q --filter "ancestor=$(IMAGE_NAME)" | xargs -r docker stop
