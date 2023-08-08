from pyspark.sql.functions import col, length, sum as sum_

# Função para verificar se existem valores nulos
def null_tests(data, data_name):
  if data.count() == 0:
    print(f"{data_name} is empty. No null tests performed.")
    return
  
  null_counts = data.agg(*[sum_(col(c).isNull().cast("int")).alias(c) for c in data.columns]).collect()
  print(f"Null counts in {data_name}:")
  for col_name in data.columns:
      null_count = null_counts[0][col_name]
      print(f"{col_name}: {null_count}")

# Função para verificar se o sensor_id tem comprimento maior que 4
def sensor_lenght_test(sensor_data):
  sensor_id_length_check = sensor_data.filter(length("sensor_id") > 4).count()

  if sensor_id_length_check > 0:
      print("Existem sensor_ids com comprimento maior que 4.")
  else:
      print("Todos os sensor_ids têm comprimento igual ou menor que 4.")