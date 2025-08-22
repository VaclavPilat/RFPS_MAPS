FILE = *.py

all: test doc

test:
	@find maps -name "*.py" -not -name "Blender.py" | sed -e 's/\//./g' -e 's/\.py$$//' | xargs -n 1 python3 -m

doc:
	@doxygen docs/Doxyfile

cloc:
	@cloc maps/ --include-lang=Python --by-file

clean:
	@rm -rf docs/html/
	@find . -type d -name "__pycache__" -exec rm -rf {} +

run:
	@COLOR=1 PYTHONPATH=$(CURDIR) find scripts -name $(FILE) -exec \
		python3 {} \; | less -FRS~# 4

show:
	@PYTHONPATH=$(CURDIR) find scripts -name $(FILE) -exec \
		blender --python-exit-code 2 --disable-abort-handler -P {} >/dev/null \;