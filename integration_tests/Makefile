.PHONY: test-setup test

test-setup: egg-info compile-catalog
	docker pull p0bailey/docker-flask
	docker pull wazopbx/wait
	docker pull wazopbx/wazo-auth-mock
	docker build --pull -t wazopbx/wazo-phoned ..
	docker build --no-cache -t wazo-phoned-test -f Dockerfile-phoned-test ..

compile-catalog:
	cd .. && python setup.py compile_catalog

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests -x
