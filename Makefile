.PHONY: start
start:
	serve

layers: mapParts/exports/zoom1-0.0-16x16.png
	mkdir -p layers
	./tileMap.py

mapParts/exports/%.png: mapParts/%.svg | mapParts/exports
	inkscape -f $< -C -z -e $@

mapParts/exports:
	mkdir -p $@

.PHONY: clean
clean:
	rm -r layers
	rm -r temp
	rm -r mapParts/exports
