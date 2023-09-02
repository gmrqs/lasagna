FROM trinodb/trino

USER root

COPY ./conf/hive.properties etc/trino/catalog/
COPY ./conf/delta.properties etc/trino/catalog/
COPY ./conf/iceberg.properties etc/trino/catalog/

RUN mkdir /etc/hadoop
RUN mkdir /etc/hadoop/conf

COPY  /conf/metastore-site.xml /etc/hadoop/conf/