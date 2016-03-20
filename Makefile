
UIFILES := ui_sarview.py

all : $(UIFILES)

ui_%.py : %.ui
	pyuic4 -i 0 -o $@ $<


clean :
	rm -f *.pyc
	rm  -f $(UIFILES)

