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

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/keys/go-de-zoomcamp-project-2024.json"

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):

    google_app_cred_location = kwargs['google_app_cred_location']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_app_cred_location
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    #bucket_name = 'go-de-zoomcamp-project-2024-bucket'
    bucket_name = kwargs['bucket_name']

    year = kwargs['year']
    programme = kwargs['programme']
    #year = "2019"
    #programme = 'Outer'

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

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    project_id = kwargs['project_id']
    dataset = kwargs['dataset']
    #dataset='london_cycles'
    
    table_id = f'{project_id}.{dataset}.{programme}_cycle_data'

    try:
        client.get_table(table_id)  # Make an API request.
        print("Table {} already exists.".format(table_id))
    except NotFound:
        print("Table {} is not found.".format(table_id))
        schema = [
                bigquery.SchemaField("Date_Time", "DATETIME"),
                bigquery.SchemaField("Year", "STRING"),
                bigquery.SchemaField("UnqID", "STRING"),
                bigquery.SchemaField("Weather", "STRING"),
                bigquery.SchemaField("Day", "STRING"),
                bigquery.SchemaField("Round", "STRING"),
                bigquery.SchemaField("Dir", "STRING"),
                bigquery.SchemaField("Path", "STRING"),
                bigquery.SchemaField("Mode", "STRING"),
                bigquery.SchemaField("Count", "INTEGER"),
                bigquery.SchemaField("Programme", "STRING"),
            ]
            
        table = bigquery.Table(table_id, schema=schema)
        table.clustering_fields = ["Mode"]
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="Date_Time",  # name of column to use for partitioning
            #expiration_ms=1000 * 60 * 60 * 24 * 90, # 90 days
        )  
        table = client.create_table(table)  # Make an API request.
        
        print(
            "Created partitioned and clustered table {}.{}.{}".format(
                table.project, table.dataset_id, table.table_id
            )
        )

    return combined_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
