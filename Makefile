build-image:
	docker build . -t tonghs/cdm

run-server:
	docker-compose -f docker-compose.app.yml up --scale web=4 -d

run-dev-server:
	docker build . -t tonghs/cdm
	docker-compose -f docker-compose.dev.yml up --remove-orphans --scale web=1

scale:
	docker-compose -f docker-compose.app.yml scale web=4
	docker exec -it cdm_nginx_1 nginx -s reload

rebuild:
	docker-compose -f docker-compose.app.yml up -d --no-deps --build web

restart:
	sudo docker ps | grep cdm | grep -v nginx | awk '{print $$NF}' | xargs -o -I {} sudo docker exec -it {} /bin/bash -c "ps -C gunicorn fch -o pid | head -n 1 | xargs kill -HUP && echo -e Restart {} ... '\033[32mdone\033[0m'"

test:
	docker build . -t tonghs/cdm
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm test

deploy:
	git pull --rebase && fab deploy

.PHONY: build-image run-server run-dev-server scale rebuild restart test deploy
