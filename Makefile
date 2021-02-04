dev-image:
	docker build . -t tonghs/web-template:0.1

run-server:
	docker-compose -f docker-compose.app.yml up -d

run-dev-server:
	docker-compose -f docker-compose.dev.yml up --scale web=1

scale-reload:
	docker-compose scale web=4
	docker exec -it web-template_nginx_1 nginx -s reload

restart-rebuild:
	docker-compose up -d --no-deps --build web

restart:
	./restart.sh

test:
	docker-compose -f docker-compose.test.yml run --rm test
