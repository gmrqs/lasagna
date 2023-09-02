# Get the config
c = get_config()

# Pre-load the sparksql+trino magic
c.InteractiveShellApp.extensions = [
    'jupyterlab_sql_editor.ipython_magic.trino',
    'jupyterlab_sql_editor.ipython_magic.sparksql'
    ]

# Pre-configure the sparksql magic

c.SparkSql.limit=20
c.SparkSql.cacheTTL=3600
c.SparkSql.outputFile='/tmp/sparkdb.schema.json'
c.SparkSql.catalogs='default'

# Pre-configure trino magic

import trino
#c.Trino.auth=trino.auth.BasicAuthentication("admin", "admin")
c.Trino.auth=None
c.Trino.user='root'
# host = trino container name
c.Trino.host='trino'
c.Trino.port=8080
c.Trino.httpScheme='http'
c.Trino.cacheTTL=3600
c.Trino.outputFile='/tmp/trinodb.schema.json'
# comma-separated list of catalogs
c.Trino.catalogs="system,tpch,hive,delta,iceberg"

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_noode_interactivity = 'all'