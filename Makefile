clean:
	rm -rf dist

dist:
	mkdir -p dist

requirements: dist requirements.txt
	pip3 install -r requirements.txt --target ./dist/ --no-cache-dir
	find ./dist -type d -name '__pycache__' | xargs rm -rf
	rm -rf dist/docutils

viirs: requirements
	cp lambda_function.py ./dist/
	cp geojsons/*.geojson ./dist/
