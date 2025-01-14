PYTHON = python3

all: test doc

test:
	$(PYTHON) -m unittest discover -s Tests -p "*Test.py"

doc:
	doxygen Doxyfile

cloc:
	cloc . --include-lang=Python --exclude-dir=Tests --by-file

clean:
	rm -rf html/