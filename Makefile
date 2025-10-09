.PHONY: install run test demo docker-build docker-run docker-push deploy

IMAGE_NAME ?= customer-support-chatbot
IMAGE_TAG ?= latest
IMAGE_REF := $(IMAGE_NAME):$(IMAGE_TAG)
APP_DIR ?= src

install:
	pip install -r requirements.txt

run:
	uvicorn --app-dir $(APP_DIR) customer_support.api:app --reload

test:
	pytest

demo:
	python scripts/demo_chat.py

docker-build:
	docker build -t $(IMAGE_REF) .

docker-run:
	docker run --rm -p 8000:8000 $(IMAGE_REF)

docker-push:
	@if [ "$(IMAGE_NAME)" = "customer-support-chatbot" ] && [ "$(IMAGE_TAG)" = "latest" ]; then \
	echo "Pushing with default name/tag; override IMAGE_NAME or IMAGE_TAG if you need a different registry target."; \
	fi
	docker push $(IMAGE_REF)

deploy: docker-build docker-run
