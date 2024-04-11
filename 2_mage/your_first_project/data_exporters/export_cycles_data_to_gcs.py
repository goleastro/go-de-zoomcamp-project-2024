import pyarrow as pa #used parition the data set
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/keys/go-de-zoomcamp-project-2024.json"

bucket_name = 'go-de-zoomcamp-project-2024-bucket'
project_id = 'go-de-zoomcamp-project-2024'

@data_exporter
def export_data(data, *args, **kwargs):

    year = kwargs['year']
    programme = kwargs['programme']
    #year = "2019"
    #programme = 'Outer'
    table_name=f'{programme}_cycle_data'
    root_path= f'{bucket_name}/{table_name}/{year}'

    data['Year_Quarter'] = data['Year'].str[0:7] # defining a new column to partition on

    table = pa.Table.from_pandas(data) # reading our data to pyarrow table (defining our table)

    gcs = pa.fs.GcsFileSystem() #defines a file system object and automatically uses our GOOGLE_APPLICATION_CREDENTIALS environment variable (defining what our file system is)

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['Year_Quarter'],
        filesystem=gcs,
        existing_data_behavior='overwrite_or_ignore' #this is currently not doing anything, try fix it
    )