.PHONY: test-setup test

test-setup: egg-info
	docker pull p0bailey/docker-flask
	docker pull wazopbx/wait
	docker build --pull -t wazopbx/wazo-phoned ..
	docker build --no-cache -t wazo-phoned-test -f Dockerfile-phoned-test ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests -x
