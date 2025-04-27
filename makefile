PYTHON = python3
BLENDER = blender
FILE = *.py

all: test doc

test:
	@$(PYTHON) -m unittest discover -s tests -p *.py

doc:
	@doxygen Doxyfile

cloc:
	@cloc src/ --include-lang=Python --by-file

clean:
	@rm -rf docs/html/

run:
	@cd src; \
	for file in $(FILE); do \
		COLOR=1 $(PYTHON) "$$file" | less -FRS -# 4; \
	done; \
	cd ..

show:
	@cd src; \
	for file in $(FILE); do \
		$(BLENDER) --python-exit-code 2 --disable-abort-handler -P "$$file" >/dev/null; \
	done; \
	cd ..