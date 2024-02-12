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
    --bbox -118.06817 34.22169 -118.05801 34.22822  # bounding box: [left  bottom  right top]
    --out_dir output

python get_dem.py 
    --bbox -118.06817 34.22169 -118.05801 34.22822  # bounding box: [left  bottom  right top]
    --compute  # flag to have the compute node perform intense, multi-core computations
    --out_dir output
```

## The three test `bbox`'s

Let's use these three bounding boxes for development and to compare between platforms:

1) "Mount Wilson"
   - `--bbox -118.06817 34.22169 -118.05801 34.22822`
   - Very small (24 x 37 pixels)
   - Should take ~5-8 seconds to complete the algorithm*

2) "California and Nevada"
   - `--bbox -124.81360 32.44506 -113.75989 42.24498`
   - 35280 x 39793 pixels
   - With 8 cores on NASA DPS, takes 9-10 min to fetch+stitch DEM, and ~13-14 min for computations*
   - Warning: Please be mindful of memory usage

3) Italy
   - `--bbox 6.26868 36.00380 18.57179 47.28139`
   - 40599 x 44291 pixels
   - With 8 cores on NASA DPS, takes 9-10 min to fetch+stitch DEM, and ~23-25 min for computations*
   - Warning: Please be mindful of memory usage
   
* Time estimates are for timings internal to the algorithm; they do not include DPS packaging time, etc.
