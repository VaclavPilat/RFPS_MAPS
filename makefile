PYTHON = python3
BLENDER = blender
FILE = *.py

all: test doc

test:
	@cd src; \
	$(PYTHON) -m unittest discover -s Tests -p "*Test.py"; \
	cd ..

doc:
	@doxygen Doxyfile

cloc:
	cloc src/ --include-lang=Python --exclude-dir=Tests --by-file

clean:
	rm -rf docs/html/

show:
	@cd src; \
	for file in $(FILE); do \
		$(BLENDER) --python-exit-code 2 --disable-abort-handler --python $(FILE); \
	done; \
	cd ..