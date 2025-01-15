PYTHON = python3
BLENDER = blender

all: test doc

test:
	$(PYTHON) -m unittest discover -s Tests -p "*Test.py"

doc:
	doxygen Doxyfile

cloc:
	cloc . --include-lang=Python --exclude-dir=Tests --by-file

clean:
	rm -rf html/

show:
	$(BLENDER) --python-exit-code 2 --disable-abort-handler --python $(FILE)