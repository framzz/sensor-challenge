import re
import os
import sys
from pyspark.sql import SparkSession
from tests import null_tests, sensor_lenght_test

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# Inicia SparkSession
spark = SparkSession.builder \
    .appName("EquipmentFailureAnalysis") \
    .config("spark.driver.memory", "15g") \
    .getOrCreate()

# Criando DFs e TempViews a partir dos arquivos .JSON e .CSV 
equipment_data = spark.read.option("multiline","true") \
      .json("data\equipment.json")
equipment_data.createOrReplaceTempView("equipment")

sensor_data = spark.read.option("header",True) \
     .csv("data\equipment_sensors.csv")

# Chamando a função criada para testar o DF
null_tests(sensor_data, "sensor_data")
sensor_lenght_test(sensor_data)

sensor_data.createOrReplaceTempView("sensor")

failure_data_not_formatted = spark.read.text('data\equipment_failure_sensors.txt')

# Criando um padrão regex para leitura e limpeza dos dados do DF failure_data_not_formatted
pattern = r"\[(\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2})\]\s+ERROR\s+sensor\[(\d+)\]:\s+\(temperature\s+([\d.-]+),\s+vibration\s+([\d.-]+)\)"

# Extraindo e separando em colunas os dados do DF failure_data_not_formatted 
data = []
for row in failure_data_not_formatted.collect():
    line = row["value"]
    match = re.match(pattern, line)
    if match:
        timestamp = match.group(1)
        sensor_id = int(match.group(2))
        temperature = float(match.group(3))
        vibration = float(match.group(4))
        data.append({"timestamp": timestamp, "sensor_id": sensor_id, "temperature": temperature, "vibration": vibration})

# Criando um DF e um TempView a partir dos dados limpos
failure_data = spark.createDataFrame(data)

# Chamando a função criada para testar o DF
null_tests(failure_data, "failure_data")

failure_data.createOrReplaceTempView("failure")

# Fazendo queries para responder cada pergunta:

# Total equipment failures that happened?
total_failures = spark.sql("""
    SELECT COUNT(*) AS total_failure
    FROM failure;
""")
                           
# Which equipment name had most failures?
equipment_with_most_failures = spark.sql("""
    SELECT e.name AS equipment_name, COUNT(f.timestamp) AS total_failure
    FROM equipment e
    JOIN sensor s ON e.equipment_id = s.equipment_id
    LEFT JOIN failure f ON s.sensor_id = f.sensor_id
    GROUP BY e.name
    ORDER BY total_failure DESC
    LIMIT 1;
""")

# Average amount of failures across equipment group, 
# ordered by the number of failures in ascending order?
average_failures_per_group = spark.sql("""
    SELECT group_name, AVG(failure_total) AS fail_avarage
    FROM (
        SELECT e.group_name AS group_name, e.equipment_id, COUNT(f.timestamp) AS failure_total
        FROM equipment e
        JOIN sensor s ON e.equipment_id = s.equipment_id
        LEFT JOIN failure f ON s.sensor_id = f.sensor_id
        GROUP BY e.group_name, e.equipment_id
    ) subquery
    GROUP BY group_name
    ORDER BY fail_avarage ASC;
""")

# Rank the sensors which present the most number 
# of errors by equipment name in an equipment group.
ranked_sensors_by_errors = spark.sql("""
    SELECT e.group_name, e.name AS equipment_name, s.sensor_id, COUNT(*) AS error_num
    FROM failure f
    JOIN sensor s ON f.sensor_id = s.sensor_id
    JOIN equipment e ON s.equipment_id = e.equipment_id
    GROUP BY e.group_name, e.name, s.sensor_id
    ORDER BY error_num DESC
""")

# Mostrando os resultados de cada query
print('Total de falhas:')
total_failures.show()
print('Equipamento com o maior numero de falhas falhas:')
equipment_with_most_failures.show()
print('Média de falhas por grupo de equipamentos:')
average_failures_per_group.show()
print('Ranque de erros por sensor:')
ranked_sensors_by_errors.show()

# Parando a SparkSession
spark.stop()