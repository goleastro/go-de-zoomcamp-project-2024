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
- We then used DBT to transform the data in the data warehouse into a production environment where it is now prepared for the dashboard.
- Looker Studio was then used to present the cycle data information in a dashboard.

# Data Pipeline
The cycle data is made available periodically, and therefore we have created a batch processing pipeline.

# Technologies
The technologies that were used are

- Cloud: GCP
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Mage
- Data Warehouse: BigQuery
- Batch processing: Pandas, DBT cloud
- Stream processing: None


# Dashboard

- Dashboard: Looker Studio
You can use any of the tools shown in the course (Data Studio or Metabase) or any other BI tool of your choice to build a dashboard. If you do use another tool, please specify and make sure that the dashboard is somehow accessible to your peers.

Your dashboard should contain at least two tiles, we suggest you include:

1 graph that shows the distribution of some categorical data
1 graph that shows the distribution of the data across a temporal line
Ensure that your graph is easy to understand by adding references and titles.

Example dashboard:
