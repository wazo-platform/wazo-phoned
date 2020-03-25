test-setup: egg-info compile-catalog
	docker build --pull -t wazopbx/wazo-phoned ..
	docker build --no-cache -t wazo-phoned-test -f Dockerfile-phoned-test ..

compile-catalog:
	cd .. && python setup.py compile_catalog

egg-info:
	cd .. && python setup.py egg_info

test:
	pytest -x

.PHONY: test-setup test
