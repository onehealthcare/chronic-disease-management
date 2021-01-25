dev-image:
	docker build . -t tonghs/web-template:0.1

run-server:
	docker-compose up -d

run-dev-server:
	docker-compose -f docker-compose-dev.yml up --scale web=1

scale-reload:
	docker-compose scale web=4
	docker exec -it web-template_nginx_1 nginx -s reload

test:
	ci/run_test.sh
