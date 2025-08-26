FILE = *.py

all: test doc

test:
	@PYTHONPATH=$(CURDIR) python3 tests/doctests.py

doc:
	@doxygen docs/Doxyfile

cloc:
	@cloc src/ --include-lang=Python --by-file

clean:
	@rm -rf docs/html/
	@find . -type d -name "__pycache__" -exec rm -rf {} +

run:
	@COLOR=1 PYTHONPATH=$(CURDIR) find scripts -name $(FILE) -exec \
		python3 {} \; | less -FRS~# 4

show:
	@PYTHONPATH=$(CURDIR) find scripts -name $(FILE) -exec \
		blender --python-exit-code 2 --disable-abort-handler -P {} >/dev/null \;