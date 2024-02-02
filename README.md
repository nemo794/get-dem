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
and create a single geotiff DEM in the `out_dir` directory, named `dem.tif`.

If the `--compute` flag is included, it will open the generated dem.tif
file and do compute-intensive, multi-core linear algebra computations
on that DEM raster. There are no changes made to the dem.tif; this command
is simply for benchmarking compute. These computations use NumPy's
linear algebra module, which uses all available CPU cores.

Example cmd line calls:

```
python get_dem.py 
    --bbox -156 18.8 -154.7 20.3  # bounding box: [left  bottom  right top]
    --out_dir output

python get_dem.py 
    --bbox -156 18.8 -154.7 20.3  # bounding box: [left  bottom  right top]
    --compute  # flag to have the compute node perform intense, multi-core computations
    --out_dir output
```
