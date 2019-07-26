.PHONY: test-setup test docker-pull build-ui egg-info

test-setup: docker-pull build-ui egg-info

docker-pull:
	docker pull wazopbx/wait
	docker pull wazopbx/wazo-auth-mock
	docker pull selenium/standalone-firefox

build-ui:
	docker build -t wazopbx/wazo-ui ..
	docker build --no-cache -t wazo-ui-test -f Dockerfile ..

egg-info:
	cd .. && python setup.py egg_info

test:
	nosetests
