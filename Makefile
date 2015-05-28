PY_SRC_DIRS := opbeat_hipchat tests main.py

test:
	nosetests
	flake8 $(PY_SRC_DIRS)

.PHONY: test
