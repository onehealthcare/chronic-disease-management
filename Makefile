dev-image:
	docker build . -t tonghs/web-template:0.1

run-server:
	docker-compose up -d

test:
	ci/run_test.sh
