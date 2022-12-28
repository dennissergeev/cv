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

all: $(CV_FULL)

$(METRICS_FIG): $(DATA)
	@echo "Make the figure"
	$(SCRIPTS)/plot_metrics.py --year_start 2014

$(SRC_STATS): $(DATA)
	@echo "Save the stats"
	$(SCRIPTS)/write_stats.py

$(DATA): $(SCRIPTS)/*.py
	@echo "Get data"
	$(SCRIPTS)/get_bibcodes.py --clobber
	$(SCRIPTS)/get_metrics.py --clobber
	$(SCRIPTS)/get_publications.py --clobber

$(CV_FULL): $(SRC_HEADER) $(SRC_MAIN) $(SRC_STATS)
	@echo "Run TeX"
	# $(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	# $(BIB) $(basename $(SRC_MAIN)).bcf
	# $(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	# $(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error

.PHONY: clean
clean:
	@echo "Remove temporary TeX files"
	-rm -f $(CV_FULL) *.aux *.bbl *.bcf *.blg *.log *.out *.synctex.gz *.xml
	-rm -f $(DATA)
