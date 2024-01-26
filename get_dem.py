import os
import argparse
import subprocess

def get_dem(bbox, out_dir):

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
    os.system(f"sardem --bbox {bbox} --data-source COP -o {dem_file} --output-format GTiff")

    # Warning: in a Jupyter notebook on NASA MAAP ADE, Steps 1 and 2 must be combined:
    #     !PROJ_DATA={proj_data_path} sardem --bbox {bbox} --data-source COP -o {dem_file} --output-format GTiff
    


if __name__ == "__main__":
    '''
    Take a bounding box and output a geotiff DEM.
    
    This is a thin wrapper around `sardem`: https://github.com/scottstanie/sardem
    
    This script is meant test the MAAP processing pipeline; it is
    hardcoded to fetch the Copernicus DEM from the AWS Open Data registry.
    See: https://registry.opendata.aws/copernicus-dem/
    
    The code will fetch the necessary DEM tiles, stitch them together with GDAL,
    and create a single geotiff DEM as the output.
    
    This script makes a system call to launch `sardem` in a new subprocess.
    Internally, `sardem` uses 4 threads for processing. In brief: there
    are several ways to hack this wrapper to exercise more cores.

    Example cmd line call:
    python get_dem.py 
        --bbox -156 18.8 -154.7 20.3  # bounding box: [left  bottom  right top]
        --out_dir output
    '''
    # Set up and aws permissions to public bucket (copied from iscesat2_boreal product)
    os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'

    parser = argparse.ArgumentParser()
    
    msg = "lat/lon bounding box, with orientation: [left  bottom  right top]. Example: '--bbox -156 18.8 -154.7 20.3'."
    parser.add_argument("-b", "--bbox", type=str, help=msg, nargs=4)
    
    msg = "Path for an existing output directory. The output DEM geotiff will be saved in here."
    parser.add_argument("-o", "--out_dir", type=str, help=msg)
    
    args = parser.parse_args()
    
    bbox = " ".join(args.bbox)
    
    get_dem(bbox, args.out_dir)
