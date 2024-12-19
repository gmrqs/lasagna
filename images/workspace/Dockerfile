FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]
RUN apt update
RUN apt-get update --fix-missing
RUN apt-get install openjdk-18-jdk -y  

#+-----------------+
#| Installing cURL |
#+-----------------+

RUN apt-get install curl -y

#+------------------------+
#| Installing Python pip |
#+------------------------+

RUN apt-get install python3-pip -y
RUN pip install --upgrade pip

#+-----------------------+
#| Installing JupyterLab |
#+-----------------------+

RUN pip install jupyterlab

#+--------------------+
#| Installing PySpark |
#+--------------------+

RUN pip install pyspark==3.5.3

ENV SPARK_HOME=/usr/local/lib/python3.10/dist-packages/pyspark

RUN mkdir -p usr/local/spark_dev/work/

#+----------------------------------+
#| Installing S3/MinIO dependencies |
#+----------------------------------+

RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    --output $SPARK_HOME/jars/hadoop-aws-3.3.4.jar
RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    --output $SPARK_HOME/jars/aws-java-sdk-bundle-1.12.262.jar
RUN curl https://jdbc.postgresql.org/download/postgresql-42.5.0.jar \
    --output $SPARK_HOME/jars/postgresql-42.5.0.jar

#+--------------------------------------------------+
#| Downloading Hive Metastore 3.0.0 dependencies    |
#|                                                  |
#|   Obtained using these configurations:           |
#|                                                  |
#|    spark.sql.hive.metastore.jars=maven           |
#|    spark.sql.hive.metastore.version=3.0.0        |
#|                                                  |
#|   start a SparkSession with these configs        |
#|   and execute any spark.sql() command            |
#|                                                  |
#+--------------------------------------------------+

RUN mkdir -p ${SPARK_HOME}/hms-3.0.0/jars
COPY conf/hms-3.0.0-deps.txt ${SPARK_HOME}/hms-3.0.0/jars
RUN cd $SPARK_HOME/hms-3.0.0/jars && xargs -n1 -P1 curl --remote-name < hms-3.0.0-deps.txt


#+------------------------------------+
#| Instalando NodeJS (para extensões) |
#+------------------------------------+

RUN apt-get install nodejs -y
RUN apt-get install npm -y

#+--------------------------------------------+
#| Installing SQL Magics for Trino e SparkSQL |
#+--------------------------------------------+

RUN npm install -g sql-language-server

RUN pip install jedi-language-server
RUN pip install jupyterlab-lsp jupyterlab-sql-editor trino
RUN pip install dbt-core==1.01
RUN pip install bokeh

#+---------------------------------------------+
#| Installing Jupyter Lab S3 Browser extension |
#+---------------------------------------------+

RUN pip install jupyterlab-s3-browser
#RUN jupyter serverextension enable --py jupyterlab_s3_browser
ENV JUPYTERLAB_S3_ENDPOINT=http://minio:9000
ENV JUPYTERLAB_S3_ACCESS_KEY_ID=admin
ENV JUPYTERLAB_S3_SECRET_ACCESS_KEY=password

#+----------------+
#| Installing Git |
#+----------------+

RUN apt-get install git -y
RUN pip install jupyterlab-git

#+--------------------------------------------------+
#| Creating Kernels for Hive and Open Table Formats |
#+--------------------------------------------------+

# Apache Hive

# Create IPython profile
RUN ipython profile create pyspark_hive
# Create PySpark + Hive kernel based on IPython profile
RUN python3 -m ipykernel install --user --name pyspark_hive --display-name "PySpark (Hive)" --profile pyspark_hive
COPY kernels/hive/media/logo-svg.svg /root/.local/share/jupyter/kernels/pyspark_hive/
# Copy startup Script
COPY kernels/hive/conf/00_startup_pyspark_hive_kernel.py /root/.ipython/profile_pyspark_hive/startup/
# Configure PySPark + Hive kernel
COPY kernels/hive/conf/ipython_config.py /root/.ipython/profile_pyspark_hive/
COPY kernels/hive/conf/ipython_kernel_config.py /root/.ipython/profile_pyspark_hive/

# Apache Iceberg

# Create IPython profile
RUN ipython profile create pyspark_iceberg
# Create PySpark + Iceberg kernel based on IPython profile
RUN python3 -m ipykernel install --user --name pyspark_iceberg --display-name "PySpark (Iceberg)" --profile pyspark_iceberg
COPY kernels/iceberg/media/logo-svg.svg /root/.local/share/jupyter/kernels/pyspark_iceberg/
# Copy startup script
COPY kernels/iceberg/conf/00_startup_pyspark_iceberg_kernel.py  /root/.ipython/profile_pyspark_iceberg/startup/
# Configure PySPark + Hive kernel
COPY kernels/iceberg/conf/ipython_config.py /root/.ipython/profile_pyspark_iceberg/
COPY kernels/iceberg/conf/ipython_kernel_config.py /root/.ipython/profile_pyspark_iceberg/

# Delta Lake

# Create IPython profile
RUN ipython profile create pyspark_delta
# Create PySpark + Delta kernel based on IPython profile
RUN python3 -m ipykernel install --user --name pyspark_delta --display-name "PySpark (Delta)" --profile pyspark_delta
COPY kernels/delta/media/logo-svg.svg /root/.local/share/jupyter/kernels/pyspark_delta/
# Copy startup script
COPY kernels/delta/conf/00_startup_pyspark_delta_kernel.py  /root/.ipython/profile_pyspark_delta/startup/
# Configure PySPark + Delta kernel
COPY kernels/delta/conf/ipython_config.py /root/.ipython/profile_pyspark_delta/
COPY kernels/delta/conf/ipython_kernel_config.py /root/.ipython/profile_pyspark_delta/

#+-----------------------------------------------+
#| Configurations for Jupyter and spark-defaults |
#+-----------------------------------------------+

COPY conf/jupyter_notebook_config.py /root/.jupyter/
COPY conf/spark-defaults.conf ${SPARK_HOME}/conf/
COPY conf/ipython_config.py /root/.ipython/profile_default/
COPY conf/plugin.jupyterlab-settings /root/.jupyter/lab/user-settings/@jupyter-lsp/jupyterlab-lsp/

RUN chmod -R 777 /usr/local/spark_dev/work
USER root
