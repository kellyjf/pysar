
UIFILES := ui_sarview.py ui_export.py

all : $(UIFILES)

test:
	python sarview.py test.sadf

ui_%.py : %.ui
	pyuic4 -i 0 -o $@ $<


clean :
	rm -f *.pyc *svg *.png *.ps *.pdf
	rm  -f $(UIFILES)
	

