python=python3

layers: mapParts/legend.json | svg2png
	mkdir -p layers
	./src/py/tileMap.py mapParts/legend.json

.PHONY: svg2png
svg2png: mapParts/exports/z2-hexmap-2048x2048.png mapParts/exports/dungeonDrawing.png

mapParts/exports/%.png: mapParts/%.svg mapParts/exports
	inkscape -f $< -C -z -e $@

mapParts/exports:
	mkdir -p $@

.PHONY: clean
clean: clean-temp
	-rm -r layers
.PHONY: clean-temp
clean-temp:
	-rm -r temp
	-rm -r mapParts/exports

.PHONY: start
start:
	${python} -m http.server

.PHONY: test
test:
	${python} src/py/tileMap.spec.py
