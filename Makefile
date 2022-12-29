# Compile CV with LaTeX
TEX = xelatex
BIB = biber
CV_FULL = sergeev_cv_full.pdf
SRC_MAIN = sergeev_cv_full.tex
SRC_HEADER = header.tex
SRC_STATS = stats.tex
DATA = \
    data/bibcodes.json \
    data/metrics.json \
    data/publications.json
METRICS_FIG = images/sergeev_ads_metrics.pdf
SCRIPTS = scripts

cv: $(CV_FULL)

inputs: $(METRICS_FIG) $(SRC_STATS)

$(METRICS_FIG): $(DATA)
	@echo "Make the figure"
	$(SCRIPTS)/plot_metrics.py --year_start 2014

$(SRC_STATS): $(DATA)
	@echo "Make stats"
	$(SCRIPTS)/write_stats.py

$(DATA): $(SCRIPTS)/*.py
	@echo "Make data"
	$(SCRIPTS)/get_bibcodes.py --clobber
	$(SCRIPTS)/get_metrics.py --clobber
	$(SCRIPTS)/get_publications.py --clobber

$(CV_FULL): $(SRC_HEADER) $(SRC_MAIN) $(SRC_STATS)
	@echo "Make TeX"
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	$(BIB) $(basename $(SRC_MAIN)).bcf
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error

.PHONY: clean
clean:
	@echo "Remove temporary TeX files"
	-rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.synctex.gz *.xml
	-rm -f $(DATA)
	-rm -f $(METRICS_FIG)
	-rm -f $(CV_FULL)
