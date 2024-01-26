# get-dem
Take a bounding box and output a geotiff DEM.

## Introduction
This is a thin wrapper around `sardem`: https://github.com/scottstanie/sardem

The wrapper is designed for use with the MAAP project; it is meant
to exercise the MAAP processing pipeline.

The source DEM is hardcoded to be the Copernicus DEM,
which is fetched from the AWS Open Data registry.
See: https://registry.opendata.aws/copernicus-dem/

The code will fetch the necessary DEM tiles, stitch them together with GDAL,
and create a single geotiff DEM as the output.

To use more cores, here are some possible code updates:
 - `get-dem` uses an OS system call to launch `sardem` in a new subprocess. 
 Perhaps update `get-dem` to launch multiple calls to `sardem` in parallel?
- `sardem` internally uses 4 threads for processing. Perhaps we could
increase this number? (Issue: this would reduce the runtime of the algorithm.)

Example cmd line call:

```
python get_dem.py 
    --bbox -156 18.8 -154.7 20.3  # bounding box: [left  bottom  right top]
    --out_dir output
```
