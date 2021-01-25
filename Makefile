dev-image:
	docker build . -t tonghs/web-template:0.1

run-server:
	docker-compose up -d

run-dev-server:
	docker-compose -f docker-compose-dev.yml up --scale web=1

scale-reload:
	docker-compose scale web=4
	docker exec -it web-template_nginx_1 nginx -s reload

restart-rebuild:
	docker-compose up -d --no-deps --build web

restart:
	for i in {1..4} ; do \
		echo retart web-template_web_$$i...; \
	 	docker stop web-template_web_$$i && docker exec -it web-template_nginx_1 nginx -s reload; \
	 	docker start web-template_web_$$i && docker exec -it web-template_nginx_1 nginx -s reload; \
		echo done; \
	done

test:
	ci/run_test.sh
