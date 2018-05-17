clean:
	rm -rf dist

dist:
	mkdir -p dist

requirements: dist requirements.txt
	pip install -r requirements.txt --target ./dist/
	find ./dist -type d -name '__pycache__' | xargs rm -rf
	rm -rf dist/docutils

cumulus-message-adapter.zip: requirements
	cp lambda_function.py ./dist/
