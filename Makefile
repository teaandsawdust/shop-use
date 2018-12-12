PYTHON := python

RAW_DATA_DIR := src-data
RAW_DATA := $(wildcard $(RAW_DATA_DIR)/*.csv)

DATA_DIR := data
DATA := $(RAW_DATA:$(RAW_DATA_DIR)/%=$(DATA_DIR)/%)

ANALYSIS_DIR := analysis
ANALYSIS := $(ANALYSIS_DIR)/daytallies

.PHONY: all
all: $(ANALYSIS)

.PHONY: clean
clean:
	-rm -r $(DATA_DIR) $(ANALYSIS_DIR)
	-rm *.pyc

.PHONY: clean-analysis
clean-analysis:
	-rm $(ANALYSIS)

.PHONY: test
test:
	$(PYTHON) -m unittest discover

$(ANALYSIS): $(DATA) analyze.py clean-analysis | $(ANALYSIS_DIR)
	$(PYTHON) analyze.py $(DATA) > $@

$(DATA_DIR)/%: $(RAW_DATA_DIR)/% convert.py | $(DATA_DIR) 
	$(PYTHON) convert.py $< > $@

$(DATA_DIR):
	mkdir -p $@

$(ANALYSIS_DIR):
	mkdir -p $@
