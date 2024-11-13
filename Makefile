
#########################################################################################
#  grav_giant_test environment tasks

OPEN_EDGE := open -a "Microsoft Edge"
OPEN_SKIM := open -a "skim"
GSDOC_PATH ?= /Users/garysiaw/Documents/Work_related/Jobhunt/JobHunt2024/11_nov/gravie.nov12/grav_giant_test/gsdoc

##@ Help

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\.].*+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


##@ Setup

.PHONY: rye.setup
rye.setup:  ## install python dependencies
	@( 	rye sync; \
	  	source .venv/bin/activate; \
	)


run.local: ## run locally
	uvicorn src.grav_giant_test.main:app --reload


##@ Docker
.PHONY: docker.build
docker.build: ## build image
	docker build -t postmodern-image -f docker/Dockerfile .

.PHONY: docker.shell
docker.shell: ## shell into container
	docker run --rm -it --name localpostmodern --entrypoint bash postmodern-image


.PHONY: docker.run
docker.run: ## run image
	docker run --rm --name localpostmodern -p 8000:8000 postmodern-image