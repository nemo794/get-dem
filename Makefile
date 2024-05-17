.PHONY: build-esa clean run-esa run-nasa compare-outputs test

BBOX?=-156 18.8 -154.7 20.3
ESA_OUTDIR=output/esa
ESA_TIF=$(ESA_OUTDIR)/dem.tif
NASA_TIF=output/dem.tif

build-esa:
	docker build -t esa-get-dem -f esa/Dockerfile .

# Ideally this would depend on the esa-get-dem Docker image, rather than the
# `build-esa` target to avoid running the algorithm unnecessarily, but locating
# the image file, or comparing its creation date to the tif date is non-trivial.
$(ESA_TIF): build-esa get_dem.py esa/Dockerfile esa/build/entrypoint.sh
	docker run -t -v ./$(ESA_OUTDIR):/projects/data/output esa-get-dem --bbox '$(BBOX)' --compute true

$(NASA_TIF): get_dem.py
	nasa/run.sh '$(BBOX)' true

run-esa: $(ESA_TIF)

run-nasa: $(NASA_TIF)

compare-outputs: run-nasa run-esa
	@cksum "$(ESA_TIF)" "$(NASA_TIF)"
	@if [[ $$(cksum "$(ESA_TIF)" | cut -d ' ' -f 1) == $$(cksum "$(NASA_TIF)" | cut -d ' ' -f 1) ]]; then \
		echo "outputs are the same"; \
	else \
		echo "outputs are different"; \
		exit 1; \
	fi

clean:
	rm -rf output
