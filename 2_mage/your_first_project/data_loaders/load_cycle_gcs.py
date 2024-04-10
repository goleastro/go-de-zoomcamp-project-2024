from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import os
from google.cloud import storage
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/keys/go-de-zoomcamp-project-2024.json"

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'go-de-zoomcamp-project-2024-bucket'

    year = kwargs['year']
    programme = kwargs['programme']
    #year = "2019"
    #programme = 'Inner'

    dfs = []

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    for blob in bucket.list_blobs(prefix=f'{programme}_cycle_data/{year}'):
        if blob.name.endswith(".parquet"):
            print(blob.name)

            df = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
                bucket_name,
                blob.name
            )

            dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
