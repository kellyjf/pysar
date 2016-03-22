
ifeq ($(DESTDIR),)
DESTDIR=$(HOME)
endif

UIFILES := ui_sarview.py ui_export.py

all : $(UIFILES)

test: $(UIFILES)
	python sarview.py test.sadf

ui_%.py : %.ui
	pyuic4 -i 0 -o $@ $<

install: $(UIFILES)
	rm -rf $(DESTDIR)/lib/python/pysar || true
	mkdir -p $(DESTDIR)/lib/python/pysar
	cp *.py $(DESTDIR)/lib/python/pysar

clean :
	rm -f *.pyc *svg *.png *.ps *.pdf
	rm  -f $(UIFILES)
	

