start :
	@docker build -t controller .
	@docker-compose up -d

stop:
	@docker-compose down

test:
	@docker-compose down
	@docker stop test-pgdocker || exit 0
	@docker pull postgres:14
	@docker run --rm --name test-pgdocker -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -d -p 5432:5432 postgres:14
	@container_name="test-pgdocker"; \
    pattern="ready to accept connections"; \
    while ! docker logs "$$container_name" | grep -q "$$pattern"; do \
      echo "Waiting for the container to be ready..."; \
      sleep 0.1; \
    done; \
    echo "Container is ready"
	@python manage.py migrate
	@pytest
	@docker stop test-pgdocker

