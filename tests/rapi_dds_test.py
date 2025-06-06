from eodms_dds import dds
from eodms_rapi import EODMSRAPI
import click
import os

def get_item(dds_api, collection, item_uuid, out_folder):

    # dds_api.refresh_aaa()

    item_info = dds_api.get_item(collection, item_uuid)

    print(f"Item info: {item_info}")

    # out_folder = "C:\\Working\\Development\\EODMS\\_packages\\py-eodms-api"

    if item_info is None:
        return None

    if 'download_url' not in item_info.keys():
        return None

    dds_api.download_item(os.path.abspath(out_folder))

    return item_info

def extract_uuid(results):

    # print(f"\nresults: {results}")

    mdata_full_name = results.get('metadataFullName')
    uuid = os.path.basename(mdata_full_name)

    return uuid

def run(eodms_user, eodms_pwd, collection, env, out_folder):

    dds_api = dds.DDS_API(eodms_user, eodms_pwd, env)

    rapi = EODMSRAPI(eodms_user, eodms_pwd)

    filters = {'Beam Mode Type': ('LIKE', ['%50m%']),
                'Polarization': ('=', 'HH HV'),
                'Incidence Angle': ('>=', 17)}
    
    rapi.search(collection, filters)

    res = rapi.get_results('full')

    print(f"\nThe following images in Collection {collection} " \
            f"were found using the RAPI:")
    for r in res:
        uuid = extract_uuid(r)
        print(f"  Item UUID: {uuid}")

    uuid = extract_uuid(res[0])
    print(f"\nUsing the first image (UUID: {uuid}) from the list to " \
          f"download using the DDS...\n")

    item_info = get_item(dds_api, collection, uuid, out_folder)

    return dds_api

@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--username', '-u', required=True, help='The EODMS username.')
@click.option('--password', '-p', required=True, help='The EODMS password.')
@click.option('--collection', '-c', required=True, help='The collection name.')
@click.option('--env', '-e', required=False, default='prod', 
              help='The AWS environment.')
@click.option('--out_folder', '-o', required=False, default='.',
              help='The output folder.')
# @click.option('--uuid', '-u', required=True, help='The UUID of the image.')
def cli(username, password, collection, env, out_folder):
    """
    Used for CLI input.
    """

    run(username, password, collection, env, out_folder)

if __name__ == '__main__':
    cli()