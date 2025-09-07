import os
import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
from glob import glob

from spp_core.Grid.SMS import SMS_ARC, SMS_MAP
from spp_core.Utilities.util import get_list_depth


def download_nld(output_dir=None, output_fname=None, levee_id_list=None):
    """
    Donwload data from the National Levee Database
    for the specified levee IDs
    """
    if output_dir is None:
        output_dir = './'
    if output_fname is None:
        output_fname = 'test'
    if levee_id_list is None:
        raise ValueError('no levee IDs specified')

    full_name = f'{output_dir}/{output_fname}'
    if not os.path.exists(f'{full_name}.zip'):
        curl_cmd = (
            'curl -X POST '
            '"https://levees.sec.usace.army.mil:443/api-local/download/dataset/geojson.zip"'
            ' -H "accept: application/json" -H "Content-Type: application/json"'
            f' -d "{levee_id_list}" --output {full_name}.zip'
        )
        os.system(curl_cmd)
    if not os.path.isdir(full_name):
        os.system(f'unzip {full_name}.zip -d {full_name}')


def nld2map(nld_fname=None):
    '''
    Convert National Levee Database (NLD) geojson to SMS map
    '''
    data = pd.read_json(nld_fname)

    arc_list = []
    # arc_hat_list = []
    xyz = np.zeros((0, 3), dtype=float)

    for feature in data['features']:
        feature_coordinates = feature['geometry']['coordinates']
        # multi-linestring or linestring
        if get_list_depth(feature_coordinates) == 2 or get_list_depth(feature_coordinates) == 3:
            if get_list_depth(feature_coordinates) == 2:  # if only one arc, convert to list
                feature_coordinates = [feature_coordinates]
            for arc in feature_coordinates:  # record arcs
                points = np.squeeze(np.array(arc))
                my_arc = SMS_ARC(points=points, src_prj='epsg:4326')
                arc_list.append(my_arc)
                # record arc vertices
                xyz = np.r_[xyz, my_arc.points[:, :3]]
        elif get_list_depth(feature['geometry']['coordinates']) == 1:  # point
            point = np.array(feature_coordinates).reshape(-1, 3)
            # record stand-alone points
            xyz = np.r_[xyz, point]

    return SMS_MAP(arcs=arc_list), xyz


def nld2map2(nld_fname=None):
    '''
    Convert National Levee Database (NLD) geojson to SMS map
    '''
    data = gpd.read_file(nld_fname)

    arc_list = []
    xyz = np.zeros((0, 3), dtype=float)

    for _, row in data.iterrows():
        if row['geometry'].geom_type == 'LineString':
            points = np.array(row['geometry'].coords)
            my_arc = SMS_ARC(points=points, src_prj='epsg:4326')
            arc_list.append(my_arc)
            xyz = np.r_[xyz, my_arc.points[:, :3]]
        elif row['geometry'].geom_type == 'Point':
            point = np.array(row['geometry'].coords).reshape(-1, 3)
            xyz = np.r_[xyz, point]
        else:
            raise ValueError(f'Unsupported geometry type: {row["geometry"].geom_type}')

    return SMS_MAP(arcs=arc_list), xyz


def json2shapefile(json_dir):
    '''Convert all geojson files of the NLD data
    in the directory to shapefiles and xyz files'''
    output_dir = f'{Path(json_dir).parent}/shapefiles/'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    json_files = glob(f'{json_dir}/*json')
    for json_file in json_files:
        gdf = gpd.read_file(json_file)
        gdf['geometry'].to_file(f'{output_dir}/{Path(json_file).stem}.shp')

        my_map, xyz = nld2map2(nld_fname=json_file)
        np.savetxt(f'{output_dir}/{Path(json_file).stem}.xyz', xyz, fmt='%.10f')


def sample_nld():
    '''
    Sample function to download NLD data and convert to SMS map
    '''
    # json2shapefile(
    #     json_dir='/sciclone/schism10/Hgrid_projects/Levees/Levee_v4/4405000518/levee_4405000518/'
    # )
    # pass

    # -------------------------- input levee IDs --------------------------
    # Levee _v3, Aug, 2023
    # wdir = '/sciclone/schism10/Hgrid_projects/Levees/Levee_v3/FEMA_regions/'
    # levee_name = 'FEMA_region_levees'

    # # Specify levee ids from a csv file
    # levee_info_fname = f'{wdir}/System.csv'
    # df = pd.read_csv(levee_info_fname)
    # system_ids = df['SYSTEM ID'].to_numpy().astype(int).tolist()

    # Test
    wdir = '/sciclone/schism10/Hgrid_projects/Levees/Levee_v4/4405000518/'
    levee_name = 'levee_4405000518'
    system_ids = [4405000518]

    # Levee_2025
    wdir = '/sciclone/schism10/Hgrid_projects/Levees/Levee_2025/FEMA_regions/'
    levee_name = 'FEMA_region_levees'
    # Specify levee ids from a csv file
    levee_info_fname = f'{wdir}/System.csv'
    df = pd.read_csv(levee_info_fname)
    system_ids = df['SYSTEM ID'].to_numpy().astype(int).tolist()
    # ----------------------------------------------------------------------

    # Download profiles
    download_nld(output_dir=wdir, output_fname=levee_name, levee_id_list=system_ids)
    # which extracts the downloaded *.zip to *.geojson and saved to wdir/{levee_name}
    # LeveedArea.geojson and SystemRoute.geojson

    # convert to sms map
    my_map, xyz = nld2map2(nld_fname=f'{wdir}/{levee_name}/SystemRoute.geojson')
    my_map.writer(filename=f'{wdir}/{levee_name}/{levee_name}.map')
    np.savetxt(f'{wdir}/{levee_name}/{levee_name}.xyz', xyz, fmt='%.10f')

    # convert to shapefile
    gdf = gpd.read_file(f'{wdir}/{levee_name}/LeveedArea.geojson')
    gdf['geometry'].to_file(f'{wdir}/{levee_name}/LeveedArea.shp')

    gdf = gpd.read_file(f'{wdir}/{levee_name}/SystemRoute.geojson')
    gdf['geometry'].to_file(f'{wdir}/{levee_name}/SystemRoute.shp')


if __name__ == '__main__':
    sample_nld()
    print('Done')
