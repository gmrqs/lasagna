![alt text](docs/pastabricks-2.png "Lasagna")
Lasagna (or _pastabricks_) is a interactive development environment I built to learn and practice PySpark.

It's built using Docker Compose template, provisioning a Jupyter Lab, a two-workers Spark Standalone Cluster, MinIO Object Storage, a Hive Standalone Metastore, Trino and a Kafka cluster for simulating events. 

Requisites:
- Docker Desktop
- Docker Compose

To use it you just have to clone this repository and execute the following:

```bash
docker compose up -d
```

<sub><sup>Docker will build the images by itself. I recommend having a wired internet connection for this</sup></sub>

After all container are up and running, execute the following to get Jupyter Lab access link: 

```bash
 docker logs workspace 2>&1 | grep http://127.0.0.1
```

<sub><sup>(you can also the the link in docker desktop logs)</sup></sub>

Clique no link _http://127.0.0.1:8888/lab?token=<token_gigante_super_seguro>_

To start the Kafka broker you need to go to the kafka folder and execute the following:

```bash
docker compose up -d
```

### What does Lasagna creates?

![alt text](docs/analytics-lab.png "Title")

The `docker-compose.yml` template create a series of containers:

#### :orange_book: Workspace
A Jupyter Lab client for interactive development sessions, featuring:
+ A _work_ directory in order to persists your scripts and notebooks;
+ `spark-defaults.conf` pre-configured to make Spark Sessions easier to create;
+ Dedicated kernels for PySpark with Hive, Iceberg or Delta;

> :eyes: Use `%SparkSession` command to easily configure Spark Session

![alt text](docs/kernels.gif "Title")
+ [jupyter_sql_editor](https://github.com/CybercentreCanada/jupyterlab-sql-editor) extension for SQL execution with `%sparksql` and `%trino` magic commands;
+ [jupyterlab_s3_browser](https://github.com/IBM/jupyterlab-s3-browser) extension to easily browse MinIO S3 buckets;

#### :open_file_folder: MinIO Object Storage
A single MinIO instance to serve as object storage:
+ Web UI accessible at localhost:9090 (user: `admin` password: `password`)
+ s3a protocol API available at port 9000;
+ _mount/minio_ and _mount/minio-config_ directories mounted to persist data between sessions.

#### :sparkles: Spark Cluster
A standalone spark cluster for workload processing:
+ 1 Master node (master at port 7077, web-ui at localhost:5050)
+ 2 Worker nodes (web-ui at localhost:5051 and localhost:5052)
+ All the necessary dependencies for MinIO connection;
+ Connectivity with MinIO @ port 9000.

#### :honeybee: Hive Standalone Metastore
A Hive Standalone Metastore instance using PostgreSQL as back-end database allowinto to persist table metadata between sessions.
+ _mount/postgres_ directory to persist tables between development sessions;
+ Connectivity with Spark cluster at through  thift protocol at port 9083;
+ Connectivity with PostgresSQL through JDBC at port 5432.

#### :rabbit: Trino
A single Trino instace to serve as query engine.
+ Hive, Delta e Iceberg catalos configured. All tables created in using PySpark are accessible with Trino;
+ Standar service available at port 8080.

> :eyes: Don't forget you can use the `%trino` magic command in your notebooks!

#### :ocean: Kafka
A separate docker compose template with a zookeper + kafka single-node instance to mock data-streams with a python producer.
+ Uses the same network as the lasagna docker compose creates;
+ A kafka-producer notebook/script is available to create random events with Faker library;
+ Accessible at kafka:29092.