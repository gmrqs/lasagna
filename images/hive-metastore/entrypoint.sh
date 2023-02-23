#!/bin/sh

/usr/local/hive-metastore/bin/schematool -initSchema -dbType postgres
/usr/local/hive-metastore/bin/start-metastore