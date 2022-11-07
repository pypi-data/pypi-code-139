"""Tests for .helper functions."""
import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
import xarray as xr

from gdptools.helpers import calculate_weights
from gdptools.helpers import finalize_csv
from gdptools.helpers import finalize_netcdf
from gdptools.helpers import run_weights


@pytest.fixture()
def get_gdf() -> gpd.GeoDataFrame:
    """Create GeoDataFrame."""
    return gpd.read_file("./tests/data/DRB/DRB_4326.shp")


@pytest.fixture()
def get_xarray() -> xr.Dataset:
    """Create xarray Dataset."""
    return xr.open_dataset("./tests/data/DRB/o_of_b_test.nc")


@pytest.fixture()
def get_file_path(tmp_path):
    """Get temp file path."""
    return tmp_path / "test.csv"


@pytest.fixture()
def get_out_path(tmp_path):
    """Get temp file output path."""
    return tmp_path


data_crs = 4326
x_coord = "lon"
y_coord = "lat"
t_coord = "time"
sdate = "2021-01-01T00:00"
edate = "2021-01-01T02:00"
var = ["Tair"]
shp_crs = 4326
shp_poly_idx = "huc12"
wght_gen_crs = 6931


def test_calculate_weights(get_xarray, get_gdf, get_file_path, get_out_path):
    """Test calculate weights."""
    wghts = calculate_weights(
        data_file=get_xarray,
        data_crs=data_crs,
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        sdate=sdate,
        edate=edate,
        var=var[0],
        shp_file=get_gdf,
        shp_crs=shp_crs,
        shp_poly_idx=shp_poly_idx,
        wght_gen_file=get_file_path,
        wght_gen_crs=wght_gen_crs,
    )

    assert isinstance(wghts, pd.DataFrame)
    ngdf, vals = run_weights(
        var=var[0],
        x_coord=x_coord,
        y_coord=y_coord,
        t_coord=t_coord,
        ds=get_xarray,
        ds_proj=data_crs,
        wght_file=wghts,
        shp=get_gdf,
        geom_id=shp_poly_idx,
        sdate="2021-01-01T00:00",
        edate="2021-01-02T23:00",
    )
    vallist = [vals]
    gdflist = [ngdf]
    assert isinstance(ngdf, gpd.GeoDataFrame)
    assert isinstance(vals, np.ndarray)

    var_dict = {
        "Tair": {
            "long_name": get_xarray["Tair"].long_name,
            "units": get_xarray["Tair"].units,
            "varname": "Tair",
            "standard_name": " Hourly Temperature",
        },
    }
    dict_new = {
        "dims": {"feature": "nhru", "time": "time", "x": "lon", "y": "lat"},
        "feature": {
            "varname": "nhru",
            "long_name": "local model Hydrologic Response Unit ID (HRU)",
        },
        "lat": {
            "varname": "lat",
            "long_name": "Latitude of HRU centroid",
            "units": "degree_north",
            "standard_name": "latitude",
        },
        "lon": {
            "varname": "lon",
            "long_name": "Longitude of HRU centroid",
            "units": "degree_east",
            "standard_name": "longitude",
        },
        "Tair": {
            "varname": "Tair",
            "long_name": get_xarray["Tair"].long_name,
            "standard_name": " Hourly Temperature",
            "convert": True,
            "native_unit": "degC",
            "convert_unit": "degF",
        },
    }

    with pytest.raises(ValueError):
        fres = finalize_netcdf(
            gdf=gdflist,
            vals=vallist,
            p_opath=get_out_path,
            prefix="gm_tmax",
            start_date=sdate,
            time_interval=1,
            time_type="hours",
            var_dict=var_dict,
            use_opt_dict=True,
            work_dict=dict_new,
        )

    fres = finalize_csv(
        gdf=gdflist,
        vals=vallist,
        vars=var,
        ds=get_xarray,
        p_opath=get_out_path,
        prefix="gm_tmax",
        start_date=sdate,
        time_interval=1,
        time_type="hours",
    )

    assert fres
    ofile = get_out_path / "gm_tmax.csv"
    assert ofile.exists()

    outfile = pd.read_csv(ofile)
    print(outfile.head())
