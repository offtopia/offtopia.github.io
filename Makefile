all: index.html

%.html: %.eww
	python genhtml.py $< > $@

.PHONY: all clean

clean:
	rm *.html
