.PHONY: install run chat test

install:
	pip install -r requirements.txt

run:
	uvicorn customer_support.api:app --reload

chat:
	python -m customer_support.cli

test:
	pytest
