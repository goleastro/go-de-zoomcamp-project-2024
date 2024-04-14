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

![image](https://github.com/goleastro/go-de-zoomcamp-project-2024/assets/20685550/79a0f9ba-480f-4ed0-897f-17fb47e11517)

# Instructions

## Prerequisites
Assuming that a GitHub CodeSpace will be used to run this project.
- GCP project
- GCP credentials file capable of modifyng GCS buckets
- GCP credentials file capable of modyfing BigQuery datasets

1. Install Terraform [](https://developer.hashicorp.com/terraform/install)
2. Install Jupyter `pip install jupyter` (optional - not required to run the project)
3. In the folder "1_terraform" 
