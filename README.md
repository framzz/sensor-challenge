# Description

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
