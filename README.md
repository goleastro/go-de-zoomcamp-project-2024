# Course Project | de-zoomcamp-project-2024

# Objective
The goal of this project is to apply everything we have learned in this course to build an end-to-end data pipeline.

# Problem statement
One of the things London is known for is it's traffic, and as such, the city has imposed congestion charges on motor vehicles, with penalties for late payers.

We will be using cycle data provided by cycling.data.tfl.gov.uk to analyse the flow of cycle traffic during different quarters of the year, at various boroughs within 3 areas of London, namely, Central, Inner and Outer London.

TfL has mentioned that the cycle data from 2020 is synthetic because of the COVID-19 pandemic, and as such, we will only be using data between 2017 and 2019 for this exercise.

We are a cycle hire company called "London Peddlers", and we would like to use the TfL cycle data to determine what the market share is between private bicycles and rental bicycles, for active cyclists. 

Central data from 2017 to 2019 includes all 4 quarters of the year (Q1 to Q4)
Inner and Outer data from 2017 to 2019 only includes quarter 2 of the year (Q2 only)

We have developed a dashboard with a few tiles by:

- Using cycle data provided by TfL here cycling.data.tfl.gov.uk.
- Creating a pipeline in Mage that processes the dataset and loads it GCS in Parquet format.
- The pipeline also move the data from the data lake to BigQuery.
- We then used DBT to transform the data and partition the data in the data warehouse into a production environment where it is now prepared for the dashboard.
- Looker Studio was then used to present the cycle data information in a dashboard.

# Data Pipeline
The cycle data is made available periodically, and therefore we have created a batch processing pipeline.


# Technologies
The technologies that were used are:

- Cloud: GCP
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Mage
- Data Warehouse: BigQuery
- Batch processing: Pandas, DBT cloud
- Stream processing: None


# Dashboard

The data in the fact table "fact_cycle_trips_partitioned_clustered" was partitioned by "Date_Time" and clustered by "Mode" to improve the dashboard read size and performance respectively. 
- Dashboard: Looker Studio

![image](https://github.com/goleastro/go-de-zoomcamp-project-2024/assets/20685550/2d6f2c47-b68d-4b9e-aaa5-99ffc5e42f45)

![image](https://github.com/goleastro/go-de-zoomcamp-project-2024/assets/20685550/f89fd1b9-33d0-4aa9-8bd6-567cc5e97cbd)


[Link to report in Looker Studio: Bicycle Type](https://lookerstudio.google.com/embed/reporting/ceeb797d-56f9-4f4f-8444-01dcef35ab73/page/p_dugtlfrdgd)

[Link to report in Looker Studio: Programme Distribution](https://lookerstudio.google.com/embed/reporting/ceeb797d-56f9-4f4f-8444-01dcef35ab73/page/zylwD)


# Instructions

## Prerequisites
Assuming that a GitHub CodeSpace will be used to run this project.
- GCP project
- GCP credentials file capable of modifyng GCS buckets
- GCP credentials file capable of modyfing BigQuery datasets

### Infrastructure with Terraform and GCP
1. Fork this repository
2. Install Terraform [Terraform install instructions](https://developer.hashicorp.com/terraform/install)
3. Install Jupyter `pip install jupyter` (optional - not required to run the project)
4. Place your GCP credentials file within a directory of the project, example `1_terraform/keys/go-de-zoomcamp-project-2024.json`
5. Modify the **variables.tf** file found here `1_terraform/variables.tf`
     - **credentials:** this should be the path to your GCP credentials file. i.e. "./keys/go-de-zoomcamp-project-2024.json""
     - **project:** this should be the name of your GCP project
     - **bq_dataset_name:** you can leave this as "london_cycles"
     - **gcs_bucket_name:** this should be the name of your GCS bucket
6. Run `Terraform init`
7. Run `Terraform apply` and hit "y" if you are happy with the plan
     - Check GCP and make sure your GCS storage bucket and BigQuery dataset was created
### Orchestration with Mage
9. Start the Mage container by navigating to the `2_mage` directory and then running `run docker-compose up`
10. Make sure port 6789 is open and access Mage here http://localhost:6789/ 
11. Update **io_config.yaml** file found here `2_mage/io_config.yaml`
     - Update **GOOGLE_SERVICE_ACC_KEY_FILEPATH** to point to the location of your GCP file. Keep in mind that we are running Mage in a docker contain with a volume mounted for storage. The folder _2_mage_ is equivalent to the location _/home/src/_.
     - Therefore `"/home/src/keys/go-de-zoomcamp-project-2024.json"` on the docker container would translate to on our VM `"2_mage/keys/go-de-zoomcamp-project-2024.json"`
12. Update **metada.yaml** file found here `2_mage/your_first_project/pipelines/cycles_data_pipeline/metadata.yaml`
     - Update the following variables
          - **bucket_name:** this should be your GCS bucket name
          - **dataset:** you can leave this name as is (must be the same as your dataset name that you created in above with Terraform)
          - **google_app_cred_location:** point this to the location of your GCP credential file (similar to step 7 above)
          - **project_id:** this should your GCP projectID
          - **year:** this variable is used to pick which year we download data for _(this value can be between 2014 and 2019)_
          - **programme:** this is the cycle count programme type to download _(this value can be either Central, Inner or Outer. NB the first letter of the word must be capital)_
### Pipeline = API --> GCS (as partitioned parquet) --> Google BigQuery (partitioned and clustered)
13. Mage should have a few Triggers already setup. Manually execute all the triggers. The triggers run the pipe line for each programme `(Outer, Central, Inner)` once for each of the years `2017, 2018, 2019`
     - if there are no triggers setup for some reason, then setup and execute the triggers
     - The cycle data will have loaded to the GCS bucket, partitioned by year
     - The cycle data will have been read from the GCS bucket to BigQuery, to a dataset for each programme, `(Outer, Central, Inner)`.
          - The datasets are created with a partition on the "Date_Time" field per day and clusters the tables pm the "Mode" field.
               - Partitioning was done to reduce the read size by upstream DBT processes.
               - Clustering was done to improve performance when filtering on the "Mode" field.
### Transformation with DBT
14. Create a new or use an existing DBT cloud account - [dbt cloud](https://www.getdbt.com/)
     - Create a connection to BigQuery and upload your GCP key file to create the connection between DBT cloud and BigQuery.
          - Pick your dataset name (we will use this as your 'dev' environment) it does not need to be the same as the dataset that your pipeline wrote to.
     - Link your DBT cloud account to this forked repository by adding the SSH key generated by DBT to the SSH and GPG keys section under the settings of your GITHUB profile. Make sure to allow read and write access.          
15. Next run `dbt build` with DBT cloud.
     - Check that the models have written to your dataset
          - dim_locations
          - fact_cycle_trips
          - monitoring_locations_lookup
          - stg_Inner_cycle_data
          - stg_Outer_cycle_data
          - stg_central_cycle_data  
16. (Optional) Next we want to deploy the models to a 'production' environment.
     - To do this, setup a 'Deploy Job' in DBT
     - Point to the production environment
     - Run the job
     - Check your dataset and confirm that the deployment to 'production' was successful. All models from point 15 above should be present in the production.
### Dashboard with Looker Studio
17. In Google's Looker Studio
     - Create a new Big Query data source
     - Point to the fact_cycle_trips table in your production (or dev) dataset
     - Add a control `date filter`, set Date_Time as the dimension
     - Add a control `drop down`, set Year as the dimension
     - Bicycle type distribution: Add a pie chart, dimension = "mode"; metric = sum(count)
     - Bicycle type per borough: Add stacked bar chart, dimension = dimension = "mode"; metric = sum(count)
     - Bicycle type per quarter: Add stacked bar chart, dimension = "year"; break down dimension = "mode"; metric = sum(count)

Instead of creating your own dashboard, I have created a link to view my dashboard, however, my GCP service will expire before the end of April 2024 and therefore no connection to BigQuery will be available.

[Link to report in Looker Studio: Bicycle Type](https://lookerstudio.google.com/embed/reporting/ceeb797d-56f9-4f4f-8444-01dcef35ab73/page/p_dugtlfrdgd)

[Link to report in Looker Studio: Programme Distribution](https://lookerstudio.google.com/embed/reporting/ceeb797d-56f9-4f4f-8444-01dcef35ab73/page/zylwD)
