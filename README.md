# Sparkify Data Warehouse

Welcome to the Sparkify Data Warehouse project! Sparkify is a fictional music streaming company looking to enhance its analytical capabilities and better understand user behavior on their platform. The aim of this project is to build a scalable and high-performance cloud-based Data Warehouse using AWS to store and process data related to user activities, songs, and artists.

The Data Warehouse will be built on Amazon Redshift, a highly scalable and high-performance cloud data storage solution designed to handle large volumes of data. Redshift enables Sparkify's data analytics team to run complex queries and analyze user behavior patterns with ease and efficiency.

In this project, we will use the star schema to model the data in the Data Warehouse. The star schema is a common and efficient approach to organizing data in a DWH, as it facilitates the creation of analytical queries and reports. The star schema structure consists of a central fact table, which stores information about log events, and several dimension tables that store information about users, songs, and artists. This approach simplifies the querying process and improves the performance of analytics.

The raw data is stored in Amazon S3, a highly scalable and durable object storage service that enables storing and retrieving large volumes of data. The ETL process will be responsible for extracting the data from S3, transforming it according to business rules, and loading it into the Data Warehouse in Redshift. By utilizing AWS as the foundation for the project, we can ensure scalability, security, and efficiency in managing and processing data.

In summary, this project aims to provide Sparkify with a robust and scalable cloud-based Data Warehouse capable of accommodating its growth and delivering valuable insights into user behavior on the music streaming platform.


1. [Getting Started](#getting-started)
2. [Technologies Used](#technologies-used)
3. [DWH Architecture](#dwh-architecture)
4. [Data Modeling](#data-modeling)
   - [Staging Tables](#staging-tables)
   - [Star Schema](#star-schema)
   - [Data Modeling Process](#data-modeling-process)
5. [AWS Permissions](#aws-permissions)
   - [Required AWS Permissions](#required-aws-permissions)
   - [Granting AWS Permissions](#granting-aws-permissions)

## Getting Started

1. Fill in `KEY` and `SECRET` in dwh.cfg

2. Run `create_dwh.py` to create a Data Warehouse

3. Run `create_table.py` to create tables

4. Run `etl.py` to run ETL process

5. If you no longer need the Data Warehouse, you can delete it with `delete_dwh.py`

## Technologies Used

This section provides an overview of the key technologies, tools, and programming languages used in the Sparkify Data Warehouse project. These technologies have been carefully selected to ensure scalability, efficiency, and ease of use throughout the project lifecycle.

1. **Amazon Web Services (AWS)**: The project relies on several AWS services for data storage, processing, and management. AWS provides a robust, secure, and scalable cloud infrastructure for building and maintaining the Data Warehouse.

   - **Amazon S3**: S3 (Simple Storage Service) is a highly-scalable and durable object storage service used for storing the raw data, including log files and metadata related to users, songs, and artists.

   - **Amazon Redshift**: Redshift is a fully-managed, petabyte-scale data warehouse service that enables fast and efficient querying and analysis of large volumes of data. In this project, Redshift serves as the primary storage solution for the processed data.

2. **ETL Tools**: Custom ETL scripts are used to extract, transform, and load the data from S3 into the Redshift Data Warehouse. These scripts are written in Python, utilizing the following libraries:

   - **Boto3**: Boto3 is the official AWS SDK for Python, used for interacting with AWS services such as S3 and Redshift.

   - **Psycopg2**: Psycopg2 is a popular PostgreSQL adapter for Python, used to connect to and interact with the Redshift cluster, which is based on PostgreSQL.

3. **SQL**: SQL (Structured Query Language) is used for defining the schema, querying the data, and managing the Data Warehouse. SQL scripts are utilized for creating tables, defining relationships, and populating the tables with data.

4. **Python**: Python is a versatile programming language used in this project for developing the ETL scripts and interacting with AWS services. Python's extensive library ecosystem and readability make it an excellent choice for handling data processing tasks.

5. **Version Control**: Git and GitHub are used for version control and collaboration, ensuring the codebase remains organized, up-to-date, and accessible to all team members.

By leveraging these technologies, the Sparkify Data Warehouse project is well-equipped to handle the challenges of large-scale data storage, processing, and analysis.


## DWH Architecture

The Data Warehouse (DWH) architecture for the Sparkify project is designed to provide a scalable, efficient, and easy-to-use environment for storing and analyzing large volumes of data. The architecture consists of several key components that work together to ensure seamless data processing, storage, and analysis.

![DWH Architecture Diagram](img/dwh_architecture.drawio.svg)

### Components of the DWH Architecture

1. **Data Sources**: Data sources are the origin systems that provide data to be stored in the DWH. In the Sparkify project, these sources include log files and metadata related to users, songs, and artists, which are stored in Amazon S3.

2. **ETL Process**: The ETL (Extract, Transform, Load) process extracts data from the data sources, transforms it according to the business rules and requirements, and loads it into the Data Warehouse. The ETL process is implemented using custom Python scripts that leverage Boto3 for interacting with AWS services and Psycopg2 for managing data in the Redshift cluster.

3. **Amazon Redshift**: Amazon Redshift serves as the primary Data Warehouse storage solution, providing a highly-scalable and high-performance environment for storing and querying large volumes of data. Redshift is designed to handle complex analytical queries and work seamlessly with other AWS services.

4. **Data Modeling**: The data is organized using the star schema, which is an efficient and intuitive approach for designing Data Warehouse structures. The star schema consists of a central fact table containing log event information, and several dimension tables for storing data about users, songs, and artists. This organization simplifies querying and improves analytics performance.

5. **Data Analytics Tools**: The Data Warehouse is designed to work seamlessly with various data analytics tools, such as BI tools, SQL clients, or custom-built applications, enabling users to easily access, analyze, and visualize data from the DWH.

6. **Security and Maintenance**: Security and maintenance processes are in place to ensure the integrity, performance, and security of the Data Warehouse. These processes include monitoring, backup, recovery, and optimization tasks.

By combining these components, the Sparkify DWH architecture provides a robust and scalable solution for managing and analyzing large volumes of data, ultimately delivering valuable insights into user behavior on the music streaming platform.


## Data Modeling

Data modeling is the process of defining and organizing the structure of the data within the Data Warehouse. In the Sparkify project, we use the star schema to model the data, as it is an efficient and intuitive approach for organizing data in a DWH. The star schema simplifies querying and improves analytics performance by minimizing the number of joins required for analytical queries.


### Staging Tables

In the Sparkify Data Warehouse, we also use two staging tables to temporarily store the raw data extracted from the source files before it is transformed and loaded into the fact and dimension tables. These staging tables are:

1. **staging_songs**: This table stores raw data about songs and artists, extracted from the JSON files located in the `songs_data` folder in Amazon S3.

2. **staging_events**: This table stores raw data about user activities, such as song plays, extracted from the JSON files located in the `log_data` folder in Amazon S3.

Using staging tables simplifies the ETL process, as it allows for data validation, cleansing, and transformation to be performed efficiently before the data is loaded into the final fact and dimension tables.

![Data Modeling Diagram](img/sparkify_staging_tables.png)


### Star Schema

The star schema consists of a central fact table and multiple dimension tables that are connected to the fact table. The fact table contains quantitative information about events, while the dimension tables store descriptive attributes related to the events.

In the context of the Sparkify project, the fact table and dimension tables are as follows:

1. **Fact Table - songplays**: This table stores information about individual song plays, including the user ID, song ID, artist ID, session ID, and playback start time. Each row in the table represents a unique song play event.

2. **Dimension Table - users**: This table stores information about the users of the Sparkify platform, such as their unique user ID, first name, last name, gender, and level of subscription (free or paid).

3. **Dimension Table - songs**: This table contains information about the songs available on the platform, including the song ID, title, artist ID, year of release, and duration.

4. **Dimension Table - artists**: This table stores information about the artists associated with the songs on the platform, such as their unique artist ID, name, location, latitude, and longitude.

5. **Dimension Table - time**: This table breaks down the timestamp information of song plays into various time-based attributes, such as hour, day, week, month, year, and weekday.


![Data Modeling Diagram](img/sparkify_star_schema.png)

### Data Modeling Process

The data modeling process for the Sparkify project includes the following steps:

1. **Define the schema**: The first step is to define the structure of the fact and dimension tables, including the column names, data types, and constraints.

2. **Create the tables**: Using the defined schema, create the fact and dimension tables in the Redshift cluster using SQL.

3. **Load data**: Extract the data from the source files (stored in Amazon S3) and load it into the appropriate fact and dimension tables using the ETL process.

4. **Optimize performance**: Indexing and partitioning strategies can be applied to the tables to improve query performance and reduce the time required to analyze the data.

By following these steps, the data modeling process ensures that the data in the Sparkify Data Warehouse is organized in a way that is efficient, easy to query, and ready for analysis.

## AWS Permissions

To set up and run the Sparkify Data Warehouse project, grant certain permissions to
the AWS Identity and Access Management (IAM) role associated with your Amazon
Redshift cluster. These permissions are necessary for the project to access and
interact with the required AWS services, such as Amazon S3 and Amazon Redshift.

### Required AWS Permissions

To set up the Sparkify Data Warehouse project, the following permissions are required:

1. **AmazonS3ReadOnlyAccess**: This permission allows the IAM role to read data
   from Amazon S3, which is necessary for the ETL process to extract the raw data
   stored in the S3 bucket.

2. **AmazonRedshiftFullAccess**: This permission grants the IAM role full access
   to Amazon Redshift, allowing it to create, modify, and manage Amazon Redshift
   clusters, as well as execute SQL queries and load data into the Data Warehouse.

### Granting AWS Permissions

To grant the required permissions to the IAM role associated with your Amazon
Redshift cluster, follow these steps:

1. Sign in to the AWS Management Console and open the IAM console at
   [https://console.aws.amazon.com/iam/](https://console.aws.amazon.com/iam/).

2. In the navigation pane, click **Roles**.

3. Find the IAM role associated with your Amazon Redshift cluster. You can
   identify this role by its name, which should include "Redshift" or "redshift"
   as a part of the name.

4. Click the role name to view its details.

5. In the **Permissions** tab, click **Attach policies**.

6. In the search box, type "AmazonS3ReadOnlyAccess" and select the
   **AmazonS3ReadOnlyAccess** policy from the list.

7. Similarly, search for "AmazonRedshiftFullAccess" and select the
   **AmazonRedshiftFullAccess** policy from the list.

8. Click **Attach policy** to attach the selected policies to the IAM role.

With the required permissions granted, you can now proceed to set up and run the
Sparkify Data Warehouse project on AWS. Ensure that your Amazon Redshift cluster
is configured to use the IAM role with the appropriate permissions, and update
the `dwh.cfg` file with your AWS access key and secret key.


