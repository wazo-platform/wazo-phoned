.PHONY: test-setup test

test-setup: egg-info
	docker pull python:2.7
	docker pull nickstenning/flask
	docker pull n3llyb0y/wait
	docker build -t xivo/xivo-dird-phoned ..
	docker build -t xivo-auth-mock -f Dockerfile-auth-mock ..
	docker build -t xivo-dird-mock -f Dockerfile-dird-mock ..
	docker build --no-cache -t xivo-dird-phoned-test -f Dockerfile-dird-phoned-test ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests
