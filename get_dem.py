import os
import argparse
import subprocess
from osgeo import gdal
import numpy as np
from time import time

__version__ = "0.2.0"

def get_dem(bbox: str, out_dir: str) -> str:
    """
    Generate a COP DEM Gtiff for the given bounding box.
    
    Parameters
    ----------
    bbox : str
        lat/lon bounding box, with orientation: [left  bottom  right top].
        Example: '-156 18.8 -154.7 20.3'.
    out_dir : str
        Path to an existing directory to store the generated DEM Gtiff in.
        
    Returns
    -------
    dem_file : str
        Filepath to the generated DEM Gtiff.
        In practise, this will be: "<out_dir>/dem.tif"
    """

    dem_file = os.path.join(out_dir, "dem.tif")

    # Annoyingly, rasterio cannot find the PROJ_DATA directory
    # when running in the NASA MAAP ADE.
    # So, we need to manually set the environment variable, and
    # then run sardem

    # Step 1: Get the path to PROJ_DATA.
    #     From Command Line, use the command: echo $PROJ_DATA
    #     Example outputs:
    #       In conda base environment in MAAP ADE, this produces: /opt/conda/share/proj
    #       In a custom conda environment named 'dem', this produces: '/opt/conda/envs/dem/share/proj'
    result = subprocess.run(['echo $PROJ_DATA'], stdout=subprocess.PIPE, shell=True)
    proj_data_path = result.stdout.decode('utf-8').strip()
    
    os.environ['PROJ_DATA'] = proj_data_path
    
    # Step 2: Run sardem
    start = time()
    
    os.system(f"sardem --bbox {bbox} --data-source COP -o {dem_file} --output-format GTiff")
    
    print(f"Time to fetch and create dem.tif: {time()-start} seconds")

    # Warning: in a Jupyter notebook on NASA MAAP ADE, Steps 1 and 2 must be combined:
    #     !PROJ_DATA={proj_data_path} sardem --bbox {bbox} --data-source COP -o {dem_file} --output-format GTiff
    

    return dem_file

def do_computations(dem_file: str) -> None:
    """
    Open the DEM raster and do compute-intensive, multicore computations.

    This function produces no meaningful output, and does NOT
    modify the dem file. What it does do is exercise the underlying
    compute nodes by using the maximum number of CPUs allowed by BLAS,
    for an extended period of time, and using a significant amount of memory.
    
    By default, BLAS uses all available CPUs on a system.
    To set this manually, from CLI use:
        export OPENBLAS_NUM_THREADS = 20
    
    Parameters
    ----------
    dem_file : str
        Filepath to the generated DEM Gtiff.
        In practise, this will be: "<out_dir>/dem.tif"
    """
    # Read the DEM into a numpy array
    ds = gdal.Open(dem_file)
    dem = ds.GetRasterBand(1).ReadAsArray()
    
    # Truncate to make it a square array
    min_edge = min(np.shape(dem))
    dem = dem[:min_edge, :min_edge]
    
    print("Number of CPU cores available on instance: ", os.cpu_count())
    
    # Multi-core section:
    start = time()
    result = np.dot(np.linalg.inv(dem), dem)
    print(f"Time to perform multicore computations: {time()-start} seconds")


if __name__ == "__main__":
    """
    Take a bounding box and output a geotiff DEM.
    
    This is a thin wrapper around `sardem`: https://github.com/scottstanie/sardem
    
    This script is meant test the MAAP processing pipeline; it is
    hardcoded to fetch the Copernicus DEM from the AWS Open Data registry.
    See: https://registry.opendata.aws/copernicus-dem/
    
    The code will fetch the necessary DEM tiles, stitch them together with GDAL,
    and create a single geotiff DEM in the `out_dir` directory, named `dem.tif`.

    If the `--compute` flag is included, it will open the generated dem.tif
    file and do compute-intensive, multi-core linear algebra computations
    on that DEM raster. There are no changes made to the dem.tif; this command
    is simply for benchmarking compute.

    Example cmd line call:
    python get_dem.py 
        --bbox -156 18.8 -154.7 20.3  # bounding box: [left  bottom  right top]
        --out_dir output

    python get_dem.py 
        --bbox -156 18.8 -154.7 20.3  # bounding box: [left  bottom  right top]
        --compute  # flag to have the compute node perform intense, multi-core computations
        --out_dir output
    """
    # Set up and aws permissions to public bucket (copied from iscesat2_boreal product)
    os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'

    # Step 1: Parse Arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="version", version=__version__)
    
    msg = "lat/lon bounding box, with orientation: [left  bottom  right top]. Example: '--bbox -156 18.8 -154.7 20.3'."
    parser.add_argument("-b", "--bbox", type=str, help=msg, nargs=4)

    msg = "Flag to crunch numbers, exercise multiple cores, and use a LOT of memory."
    parser.add_argument("-c", "--compute", action='store_true', help=msg)  # default to False

    msg = "Path for an existing output directory. The output DEM geotiff will be saved in here."
    parser.add_argument("-o", "--out_dir", type=str, help=msg)
    
    args = parser.parse_args()
    
    bbox = " ".join(args.bbox)
    
    # Step 2: Make dem.tif
    dem_file = get_dem(bbox, args.out_dir)
    
    # Step 3: Perform compute-intensive, multicore operations
    if args.compute:
        do_computations(dem_file)
