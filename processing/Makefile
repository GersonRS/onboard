PROJECT_NAME=processing

# Common

all: run

## Runs application with development config.
run:
	@python -m $(PROJECT_NAME)

run-client:
	@python $(PROJECT_NAME)/predict_client.py

grpc-gen:
	@python3 -m grpc_tools.protoc \
			-I $(PROJECT_NAME)/proto \
			--python_out=./$(PROJECT_NAME)/generated \
			--grpc_python_out=./$(PROJECT_NAME)/generated \
			./$(PROJECT_NAME)/proto/*.proto
	@sed -i -E 's/^import.*_pb2/from . \0/' ./$(PROJECT_NAME)/generated/*.py

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml