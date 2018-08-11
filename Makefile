python=python3

layers: mapParts/exports/z2-hexmap-2048x2048.png mapParts/exports/dungeonDrawing.png mapParts/legend.json
	mkdir -p layers
	./src/py/tileMap.py mapParts/legend.json

mapParts/exports/%.png: mapParts/%.svg | mapParts/exports
	inkscape -f $< -C -z -e $@

mapParts/exports:
	mkdir -p $@

.PHONY: clean
clean:
	-rm -r layers
	-rm -r temp
	-rm -r mapParts/exports

.PHONY: start
start:
	serve

.PHONY: test
test:
	${python} src/py/tileMap.spec.py
