#!/bin/sh

$HIVE_HOME/bin/schematool -initSchema -dbType postgres
$HIVE_HOME/bin/start-metastore