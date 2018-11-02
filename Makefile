RAW_DATA_DIR := src-data
RAW_DATA := $(wildcard $(RAW_DATA_DIR)/*.csv)

DATA_DIR := data
DATA := $(RAW_DATA:$(RAW_DATA_DIR)/%=$(DATA_DIR)/%)

all: $(DATA)

.PHONY: clean

clean:
	-rm -r $(DATA_DIR)

.PHONY: foo

foo: $(DATA)

$(DATA_DIR)/%: $(RAW_DATA_DIR)/% | $(DATA_DIR)
	./convert.py $< > $@

$(DATA_DIR):
	mkdir -p $@
