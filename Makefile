build:
	bash ./build.sh

deploy: deploy-gnuplot deploy-linear-regression

deploy-%:
	ssh $$REMOTE_HOST "mkdir -p $$REMOTE_DIR/$*"
	scp $*-deploy/* $$REMOTE_HOST:$$REMOTE_DIR/$*

clean:
	rm *-deploy -r

info:
	@echo "remote: $$REMOTE_HOST"
	@echo "destination: $$REMOTE_DIR"

