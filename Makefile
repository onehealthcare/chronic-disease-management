build-image:
	docker build . -t tonghs/web-template

run-server:
	docker-compose -f docker-compose.app.yml up -d

run-dev-server:
	docker-compose -f docker-compose.dev.yml up --scale web=1

scale:
	docker-compose -f docker-compose.app.yml scale web=4
	docker exec -it web-template_nginx_1 nginx -s reload

restart-rebuild:
	docker-compose -f docker-compose.app.yml up -d --no-deps --build web

restart:
	./ci/restart.sh

test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm test


.PHONY: build-image run-server run-dev-server scale restart-rebuild restart test
