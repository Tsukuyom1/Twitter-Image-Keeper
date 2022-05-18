lint:
	pycodestyle main.py src/*.py --show-source --statistics --config=setup.cfg
	flake8 main.py src/*.py --statistics --show-source --config=setup.cfg
	autopep8 main.py src/*.py --diff --aggressive --aggressive --max-line-length=160
