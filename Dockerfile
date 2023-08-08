# Baixa a imagem datamechanics/spark, que conta com Spark, Java, Hadoop e Python.
FROM datamechanics/spark:3.1-latest

USER root

# Cria o diretório "/app" dentro do contêiner com as configurações de variaveis
RUN mkdir -p /app
ENV APP_HOME /app
ENV JAVA_HOME=/usr/local/openjdk-8
ENV SPARK_HOME=/opt/spark

# Define o diretório de trabalho como "/app"
WORKDIR $APP_HOME

# Copia todo o conteúdo do diretório local para o diretório "/app" dentro do contêiner
COPY . ./

# Instala dependencias essenciais
RUN python -m pip install --upgrade pip && pip install essentials

# Instala as dependencias do projeto a partir do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Definine variáveis de ambiente
ENV PYSPARK_PYTHON=python
ENV PYSPARK_DRIVER_PYTHON=python

# Executa a aplicação
CMD ["python", "-u", "main.py"]