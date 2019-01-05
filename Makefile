PYTHON := python

RAW_DATA_DIR := src-data
RAW_DATA := $(wildcard $(RAW_DATA_DIR)/*.csv)

DATA_DIR := data
DATA := $(RAW_DATA:$(RAW_DATA_DIR)/%=$(DATA_DIR)/%)

ANALYSIS_DIR := analysis

WEEK_DAYS := monday tuesday wednesday thursday friday saturday sunday
DAY_DIRS := $(WEEK_DAYS:%=$(ANALYSIS_DIR)/%)

PLOT_FILES := $(DAY_DIRS:$(ANALYSIS_DIR)/%=$(ANALYSIS_DIR)/%.gnuplot)

PLOT_HEADER := header
PLOT_FOOTER := footer

GRAPH_DIR := graphs
GRAPH_FILES := $(WEEK_DAYS:%=$(GRAPH_DIR)/%.svg)

DIRS := $(DATA_DIR) $(ANALYSIS_DIR) $(GRAPH_DIR)

.PHONY: all
all: $(GRAPH_FILES)

.PHONY: clean
clean: clean-analysis
	-rm -r $(DATA_DIR)
	-rm -r $(GRAPH_DIR)
	-rm *.pyc

.PHONY: clean-analysis
clean-analysis:
	-rm -r $(ANALYSIS_DIR)

.PHONY: test
test:
	$(PYTHON) -m unittest discover

.PHONY: day_dats
day_dats: $(DATA) analyze.py clean-analysis | $(DAY_DIRS)
	$(PYTHON) analyze.py $(DATA)

$(DATA_DIR)/%: $(RAW_DATA_DIR)/% convert.py | $(DATA_DIR) 
	$(PYTHON) convert.py $< > $@

$(DAY_DIRS): $(ANALYSIS_DIR)/%day: | $(ANALYSIS_DIR)
	mkdir $@

$(PLOT_FILES): %.gnuplot: day_dats $(PLOT_HEADER) $(PLOT_FOOTER) Makefile | $(ANALYSIS_DIR)
	m4 -DOUTPUT_FILE=$(GRAPH_DIR)/$(notdir $*).svg \
		-DWEEKDAY=$(notdir $*) $(PLOT_HEADER) > $@
	for file in $*/*; do \
		echo "plot '$${file}' using 1:2 with filledcurves lc \"black\" fs transparent solid 0.10 notitle" >> $@; \
	done
	cat $(PLOT_FOOTER) >> $@

$(GRAPH_FILES): $(GRAPH_DIR)/%.svg: $(ANALYSIS_DIR)/%.gnuplot day_dats | $(GRAPH_DIR)
	gnuplot $<

$(DIRS): %:
	mkdir -p $@
