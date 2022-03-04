PROJECT_NAME=service_api_classifier

## Runs application with development config.
adev:
	adev runserver ./$(PROJECT_NAME)/__main__.py -p 8080

## Runs application with specified postgres and redis.
wait_resources:
	python -m $(PROJECT_NAME).utils.wait_script

## Runs application with specified postgres and redis.
run-client-grpc:
	python -m $(PROJECT_NAME).utils.predict_client