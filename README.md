# Shape's Data Engineering Interview Tech Case
The **FPSO** vessel contains some equipment and each equipment have multiple sensors. Every time a failure happens, we get all the sensors data from the failed equipment, and we store this information in a log file (the time is in GMT time zone).

You are provided 3 files: the log file named “**equipment_failure_sensors.txt**”; the file named “**equipment_sensors.csv**” with the relationships between sensors and equipment’s; and the file named “**equipment.json**” with the equipment data.

### OBS: This test can be done either *BEFORE* or *DURING* the tech interview.

> ## Steps

> - **Fork** or **Clone** this repository before starting the tech test.

> - *Extract **equipment_failure_sensors.rar** to a path/folder so you can read the .txt data.*

> - You **must** structure your data in a way that queries will be optimized according to the data retrieval process regarding equipment, sensors, and dates. Data can also be manipulated in **ACID** transactions.

> - **Use Python, SQL and/or PySpark as the languages/frameworks - you may use other tools if necessary for recommended and/or plus actions.**

> - **You're free to modify the files into any extension, as long as the main data is preserved. If you wish to modify the source data, make sure you use a copy method to keep the new data decoupled from the source data.**


1. Total equipment failures that happened?

2. Which equipment name had most failures?

3. Average amount of failures across equipment group, ordered by the number of failures in ascending order?

4.  Rank the sensors which present the most number of errors by equipment name in an equipment group.

### Recommendations: 

>- Use OOP to structure your pipeline.
>- Use PEP or Black coding style.
>- Use a GIT provider for code versioning.
>- Diagram of your resolution(s).

### Plus:

>- Tests.
>- Simulate a streaming pipeline.
>- Dockerize your app.
>- Orchestration architecture.

# Mariana's Resolution:

## Description

This tech case is the resolution for Shape's interview challenge. I chose to use Pyspark to run this project because it is a great tool to process larges amouts of data (for instance the .txt file). In the next steps, I will show how the project is separated, the ways to run it and a little bit about how we could use orchestration architecture to it. The comments in the files are in portuguese-br.

# Files

**Description**: Repository Files description
## Directory Tree

```bash
├── data
│   └── equipment_failure_sensors.rar
│   └── equipment_sensors.csv
│   └── equipment.json
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
├── setup.py
├── tests.py
```
## Files Description

|Name|Description|
|-------|---------|
|Dockerfile| Requirements to run this project with Docker|
|equipment_failure_sensors.rar| RAR with Log File inside|
|equipment_sensors.csv| File with relationships between sensors and equipments|
|equipment.json| File with equipment data|
|main.py| File with the main code|
|tests.py| File with tests|
|setup.py| File with project setup|
|requirements.txt| File with project requirements|

# How to execute the project

Do not forget to extract equipment_failure_sensors.rar!!!
## System Requirements:

This code was developed using the following system configuration:
- Python 3.8.0
- Java 20.0.2
- pip 19.2.3
- Spark 3.4.1
- Hadoop 3.0.0

## Executing pipeline in a Virtual Enviroment (Windows):

- Create a virtual enviroment in your directory: 
```
python -m venv env
 ```
- Activate the virtual enviroment: 
```
env\scripts\activate
 ```
- Install the project requirements:
```
pip install -r requirements.txt
 ```
- Run `main.py` file:
```
python main.py
```

## Executing pipeline in Docker:

- Change the requirements.txt file to match with datamechanics/spark versions:
```
pyspark==3.2.1
py4j==0.10.9.3
```
- Build your image in the Dockerfile directory:
```
docker build -t project-image .
```
- Run your image to create a container:
```
docker run -it project-image
```

# Orchestration Architecture:
## What to do for this project?
In this project, I did not use the orchestration architecture, but, if we had more time, I could implement the `prefect` python lib or even create an `Apache Airflow` workflow. In the orchestration architecture, I would split the transformation, test and query process into different tasks.

The code is going to look with something like this (Airflow case):

```
default_args = {
    'owner': 'username',
    'depends_on_past': True,
    'start_date': datetime(2023, 8, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'equipment_failure_analysis',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  
)

start_task = PythonOperator(
    task_id='start_task',
    python_callable=start_function,
    provide_context=True,
    dag=dag,
)

transformation_task = PythonOperator(
    task_id='run_transformation_job',
    python_callable=run_transformation_job,
    provide_context=True,
    dag=dag,
)

validation_task = PythonOperator(
    task_id='run_validation_job',
    python_callable=run_validation_job,
    provide_context=True,
    dag=dag,
)

query_task = PythonOperator(
    task_id='run_query_job',
    python_callable=run_query_job,
    provide_context=True,
    dag=dag,
)

end_task = PythonOperator(
    task_id='end_task',
    python_callable=end_function,
    provide_context=True,
    dag=dag,
)

start_task >> transformation_task >> validation_task >> query_task >> end_task
```