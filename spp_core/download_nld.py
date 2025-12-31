import os
import pandas as pd


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


def sample_nld():
    '''
    Sample function to download NLD data
    '''
    # Levee_2025
    wdir = './'
    levee_name = 'FEMA_region_levees'
    # Specify levee ids from a csv file
    levee_info_fname = f'{wdir}/System.csv'
    df = pd.read_csv(levee_info_fname)
    system_ids = df['SYSTEM ID'].to_numpy().astype(int).tolist()
    # ----------------------------------------------------------------------

    # Download profiles
    download_nld(output_dir=wdir, output_fname=levee_name, levee_id_list=system_ids)
    # which extracts the downloaded *.zip to *.geojson and saved to wdir/{levee_name}
    # LeveedArea.geojson, SystemRoute.geojson, and other files


if __name__ == '__main__':
    sample_nld()
    print('Done')
