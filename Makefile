RAW_DATA_DIR := src-data
RAW_DATA := $(wildcard $(RAW_DATA_DIR)/*.csv)

DATA_DIR := data
DATA := $(RAW_DATA:$(RAW_DATA_DIR)/%=$(DATA_DIR)/%)

.PHONY: all
all: analysis

.PHONY: clean
clean:
	-rm -r $(DATA_DIR)
	-rm *.pyc

.PHONY: test
test:
	python -m unittest discover

.PHONY: analysis
analysis: $(DATA)
	python analyze.py $^

$(DATA_DIR)/%: $(RAW_DATA_DIR)/% | $(DATA_DIR)
	python convert.py $< > $@

$(DATA_DIR):
	mkdir -p $@
