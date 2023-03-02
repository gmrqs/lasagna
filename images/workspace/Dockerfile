FROM ubuntu:22.10

SHELL ["/bin/bash", "-c"]

RUN apt-get update --fix-missing

RUN apt-get install openjdk-11-jdk -y  

#+-----------------+
#| Instalando cURL |
#+-----------------+

RUN apt-get install curl -y

#+------------------------------+
#| Instalando Python 3.11, pip3 |
#+------------------------------+

RUN apt-get install python3.11 -y

RUN apt-get install python3-pip -y

#+-----------------------------------+
#| Instalando Jupyter Notebook + Lab |
#+-----------------------------------+

RUN pip3 install jupyter notebook

RUN pip3 install jupyterlab

#+--------------------+
#| Instalando PySpark |
#+--------------------+

RUN pip3 install pyspark

ENV SPARK_HOME=/usr/local/lib/python3.10/dist-packages/pyspark

RUN mkdir -p usr/local/spark_dev/work/

#+----------------------------------+
#| Instalando dependências S3/MinIO |
#+----------------------------------+

RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    --output ${SPARK_HOME}/jars/hadoop-aws-3.3.4.jar

RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    --output ${SPARK_HOME}/jars/aws-java-sdk-bundle-1.12.262.jar

RUN curl https://jdbc.postgresql.org/download/postgresql-42.5.0.jar \
    --output ${SPARK_HOME}/jars/postgresql-42.5.0.jar

#+----------------------------------------+
#| Configurações Jupyter e spark-defaults |
#+----------------------------------------+

COPY conf/jupyter_notebook_config.py /root/.jupyter/

COPY conf/spark-defaults.conf ${SPARK_HOME}/conf/