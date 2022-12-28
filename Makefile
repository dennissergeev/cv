# Compile CV with LaTeX
TEX = xelatex
BIB = biber
CV_FULL = sergeev_cv_full.pdf
SRC_MAIN = sergeev_cv_full.tex
SRC_HEADER = header.tex
DATA = data
SCRIPTS = scripts

all: $(CV_FULL)

$(DATA): $(SCRIPTS)
	@echo "Get data"
	$(SCRIPTS)/get_bibcodes.py --clobber
	$(SCRIPTS)/get_metrics.py --clobber
	$(SCRIPTS)/plot_metrics.py --year_start 2014

$(CV_FULL): $(SRC_HEADER) $(SRC_MAIN) $(DATA)
	@echo "Run TeX"
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	$(BIB) $(basename $(SRC_MAIN)).bcf
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error

.PHONY: clean
clean:
	@echo "Remove temporary TeX files"
	-rm -f $(CV_FULL) *.out *.bbl *.bcf *.log *.blg *.log *.synctex.gz *.aux *.xml
