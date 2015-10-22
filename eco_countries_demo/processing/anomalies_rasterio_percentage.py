import glob
import os
import rasterio
from eco_countries_demo.processing.utils_rasterio import initialize_rasterio_raster
from eco_countries_demo.processing.utils import get_month_by_filename, get_date_by_filename


def calc_anomalies(basepath, layers, filename, epsg="3857"):
    print "-----Anomalies"

    for layer in layers:
        date = get_date_by_filename(layer)
        month = get_month_by_filename(layer)
        avg_path = basepath + "/avg/" + filename + "_" + month + "_" + epsg + ".tif"
        output_path = basepath + "/anomalies/" + filename + "_" + date + "_" + epsg + ".tif"


        # if "201207" in layer:
        print "Processing: ", layer, " ", avg_path
        r = rasterio.open(layer)
        r_avg = rasterio.open(avg_path)
        data, kwargs = initialize_rasterio_raster(r, rasterio.float32)
        r_band = r.read_band(1)
        r_avg_band = r_avg.read_band(1)

        data = ((r_band.astype(float) - r_avg_band.astype(float)) / r_avg_band.astype(float)) * 100

        # writing
        print "Writing: ", output_path
        with rasterio.open(output_path, 'w', **kwargs) as dst:
            dst.write_band(1, data.astype(rasterio.float32))


def process_all():
    basepath = "/media/vortex/LaCie/LaCie/ECO_COUNTRIES/CHIRPS"

    layers = glob.glob(basepath + "/*.tif")
    calc_anomalies(basepath, layers, "CHIRPS")



# process_all()
