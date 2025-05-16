PYTHON = python3
BLENDER = blender
FILE = *.py

all: test doc

test:
	@find maps -name "*.py" -not -name "Blender.py" | sed -e 's/\//./g' -e 's/\.py$$//' | xargs -n 1 $(PYTHON) -m

doc:
	@doxygen Doxyfile

cloc:
	@cloc maps/ --include-lang=Python --by-file

clean:
	@rm -rf docs/html/

run:
	@COLOR=1 PYTHONPATH=$(CURDIR) find scripts -name $(FILE) -exec \
		$(PYTHON) {} \; | less -FRS~# 4

show:
	@PYTHONPATH=$(CURDIR) find scripts -name $(FILE) -exec \
		$(BLENDER) --python-exit-code 2 --disable-abort-handler -P {} >/dev/null \;