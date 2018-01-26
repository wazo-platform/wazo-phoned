.PHONY: test-setup test

test-setup: egg-info
	docker pull python:2.7.13-stretch
	docker pull p0bailey/docker-flask
	docker pull n3llyb0y/wait
	docker build -t wazopbx/xivo-dird-phoned ..
	docker build --no-cache -t xivo-dird-phoned-test -f Dockerfile-dird-phoned-test ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests
