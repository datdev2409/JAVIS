build:
	sam build --use-container

deploy:
	sam deploy --parameter-overrides $$(python3 read_param.py env/prod.yaml )

test:
	sam local invoke -e events/event.json --env-vars events/local.json