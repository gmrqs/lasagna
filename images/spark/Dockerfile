FROM ubuntu:22.10

SHELL ["/bin/bash", "-c"]

RUN apt-get update --fix-missing

#+-----------------+
#| Instalando cURL |
#+-----------------+

RUN apt-get install curl -y

#+--------------------+
#| Instalando Java 11 |
#+--------------------+

RUN apt-get install openjdk-11-jdk -y                                           && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> ~/.bashrc     && \
    echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH "${JAVA_HOME}/bin:$PATH"

 #+------------------------+
 #| Instalando Spark 3.3.2 |
 #+------------------------+

RUN curl -O https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz &&\
    tar xvzf spark-3.3.2-bin-hadoop3.tgz -C /usr/local &&\
    rm spark-3.3.2-bin-hadoop3.tgz &&\
    cd /usr/local &&\
    ln -sT spark-3.3.2-bin-hadoop3 spark

RUN echo "export SPARK_HOME=/usr/local/spark" >> ~/.bashrc
RUN echo "export PATH=\$SPARK_HOME/bin:\$PATH" >> ~/.bashrc

ENV SPARK_HOME /usr/local/spark
ENV PATH "${SPARK_HOME}/bin:$PATH" 

#+---------------------------------------+
#| Instalando dependências para S3/MinIO |
#+---------------------------------------+

RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar \
    --output ${SPARK_HOME}/jars/hadoop-aws-3.3.4.jar

RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar \
    --output ${SPARK_HOME}/jars/aws-java-sdk-bundle-1.12.262.jar

RUN curl https://jdbc.postgresql.org/download/postgresql-42.5.0.jar \
    --output ${SPARK_HOME}/jars/postgresql-42.5.0.jar

