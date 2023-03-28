FROM openjdk:16-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update
RUN apt-get install curl -y

# Instalar Hadoop Common https://archive.apache.org/dist/hadoop/common/

RUN curl https://archive.apache.org/dist/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz \
    --output /usr/local/hadoop-3.3.4.tar.gz
RUN tar xfz /usr/local/hadoop-3.3.4.tar.gz \
    -C /usr/local/
RUN rm /usr/local/hadoop-3.3.4.tar.gz
RUN ln -s /usr/local/hadoop-3.3.4 /usr/local/hadoop

ENV HADOOP_HOME=/usr/local/hadoop

# Instalar Hadoop Standalone Metastore https://archive.apache.org/dist/hive/

RUN curl https://archive.apache.org/dist/hive/hive-standalone-metastore-3.0.0/hive-standalone-metastore-3.0.0-bin.tar.gz \
    --output /usr/local/hive-standalone-metastore-3.0.0-bin.tar.gz
RUN tar xfz /usr/local/hive-standalone-metastore-3.0.0-bin.tar.gz \
    -C /usr/local/
RUN rm /usr/local/hive-standalone-metastore-3.0.0-bin.tar.gz
RUN ln -s /usr/local/apache-hive-metastore-3.0.0-bin /usr/local/hive-metastore

ENV HIVE_HOME=/usr/local/hive-metastore

# Consertar dependência do Guava

RUN rm /usr/local/hive-metastore/lib/guava-19.0.jar
RUN cp ${HADOOP_HOME}/share/hadoop/hdfs/lib/guava-27.0-jre.jar ${HIVE_HOME}/lib/

# Instalar conector JDBC Postgres

RUN curl https://jdbc.postgresql.org/download/postgresql-42.5.0.jar \
    --output /usr/local/postgresql-42.5.0.jar
RUN ln -s /usr/local/postgresql-42.5.0.jar ${HIVE_HOME}/lib/

# RUN apt-get install libpostgresql-jdbc-java
# RUN ln -s /usr/share/java/postgresql-jdbc4.jar /usr/local/hive-metastore/lib/
# RUN chmod 777 /usr/share/java/postgresql-jdbc4.jar

RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    --output ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws-3.3.4.jar

RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    --output ${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk-bundle-1.12.262.jar

RUN curl https://github.com/delta-io/connectors/releases/download/v0.2.0/delta-hive-assembly_2.11-0.2.0.jar \
    --output /usr/local/delta-hive-assembly_2.11-0.2.0.jar
RUN cp /usr/local/delta-hive-assembly_2.11-0.2.0.jar ${HIVE_HOME}/lib/
RUN cp /usr/local/delta-hive-assembly_2.11-0.2.0.jar ${HADOOP_HOME}/share/hadoop/tools/lib/
RUN rm /usr/local/delta-hive-assembly_2.11-0.2.0.jar

ENV HADOOP_CLASSPATH=${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk-bundle-1.12.262.jar:${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws-3.3.4.jar:${HADOOP_HOME}/share/hadoop/tools/lib/delta-hive-assembly_2.11-0.2.0.jar

COPY conf/metastore-site.xml ${HIVE_HOME}/conf
COPY conf/entrypoint.sh /entrypoint.sh

EXPOSE 9083

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]

USER root