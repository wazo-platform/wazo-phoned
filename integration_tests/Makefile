.PHONY: test-setup test

test-setup: egg-info
	docker pull p0bailey/docker-flask
	docker pull python:2.7.13-stretch
	docker pull wazopbx/wait
	docker build -t wazopbx/xivo-dird-phoned ..
	docker build --no-cache -t xivo-dird-phoned-test -f Dockerfile-dird-phoned-test ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests -x
