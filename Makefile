.PHONY: start
start:
	serve

layers:
	mkdir -p layers
	bash layers.sh

.PHONY: clean
clean:
	rm -r layers
