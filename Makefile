# Compile CV with LaTeX
TEX = xelatex
BIB = biber
CV_FULL = sergeev_cv_full.pdf
CV_SHORT = sergeev_cv_short.pdf
SRC_FULL = sergeev_cv_full.tex
SRC_SHORT = sergeev_cv_short.tex
SRC_HEADER = header.tex
SRC_STATS = stats.tex
SRC_PUBS = pubs.tex pubs_short.tex
DATA = \
    data/bibcodes.json \
    data/metrics.json \
    data/publications.json
METRICS_FIG = images/sergeev_ads_metrics.pdf
SCRIPTS = scripts
JOURNALS = static/journal_abbr.json

all: cv cv_short

cv: $(CV_FULL)

cv_short: $(CV_SHORT)

inputs: $(METRICS_FIG) $(SRC_STATS) $(SRC_PUBS)

data: $(DATA)

$(METRICS_FIG): $(DATA)
	@echo "Make the figure"
	$(SCRIPTS)/plot_metrics.py --year_start 2014

$(SRC_STATS): $(DATA)
	@echo "Make stats"
	$(SCRIPTS)/write_stats.py

$(SRC_PUBS): $(DATA) $(JOURNALS)
	@echo "Make pubs"
	$(SCRIPTS)/format_publications.py

$(DATA): $(SCRIPTS)/*.py
	@echo "Make data"
	$(SCRIPTS)/get_bibcodes.py --clobber
	$(SCRIPTS)/get_metrics.py --clobber
	$(SCRIPTS)/get_publications.py --clobber

$(CV_FULL): $(SRC_HEADER) $(SRC_FULL) $(SRC_PUBS) inputs
	@echo "Make TeX"
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error

$(CV_SHORT): $(SRC_HEADER) $(SRC_SHORT) $(SRC_PUBS) inputs
	@echo "Make TeX"
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error
	$(TEX) $(filter-out $<,$^) -interaction=nonstopmode -halt-on-error

.PHONY: clean
clean:
	@echo "Remove temporary TeX files and data"
	-rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.synctex.gz *.xml
	-rm -f $(DATA)
	-rm -f $(METRICS_FIG)
	-rm -f $(SRC_STATS)
	-rm -f $(SRC_PUBS)
	-rm -f $(CV_FULL)
	-rm -f $(CV_SHORT)
