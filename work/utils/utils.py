def get_df_datatypes(df):
    column_names = [field.name for field in df.schema.fields]
    column_types = [re.search('(\w+)\(', str(field.dataType)).group(1) for field in df.schema.fields]
    columns_datatypes =  dict(zip(column_names, column_types))
    
    return columns_datatypes

def unstruct(df):
    
    columns_manifest = get_df_datatypes(df)
    
    dtypes = list(columns_manifest.values())
    cols = list(columns_manifest.keys())

    if 'StructType' not in dtypes:
        return df
    
    elif 'StructType' in dtypes:
        for column in cols:

            if columns_manifest[column] == 'StructType':
                struct_fields = [field.name for field in df.select(f'{column}.*').schema.fields]

                df = df.select(
                        ['*'] +
                        [col(f'{column}.{struct_field}').alias(f'{column}_{struct_field}') for struct_field in struct_fields]
                ).drop(column)
                
    return unstruct(df = df)

def disarray(df, primary_key, prefix):
    
    dims_dict = {}
    
    columns_manifest = get_df_datatypes(df)
    
    dtypes = list(columns_manifest.values())
    cols = list(columns_manifest.keys())

    if 'ArrayType' not in dtypes:
        return df
    
    elif 'ArrayType' in dtypes:
        
        for column in cols:
            if columns_manifest[column] == 'ArrayType':

                dims_dict[f'{prefix}_{column}_df'] = df.select(f'{primary_key}', explode_outer(f'{column}').alias(f'{column}'))

                df = df.drop(f'{column}')
    
    return df, dims_dict

def unnest_struct_array(df, verbose = False):
    
    columns_manifest = get_df_datatypes(df)
    dtypes = list(columns_manifest.values())
    cols = list(columns_manifest.keys())
        
    if 'StructType' not in list(columns_manifest.values()) and 'ArrayType' not in list(columns_manifest.values()):
        if verbose == True:
            print('INFO: Não há colunas StructType nem Array')
            df.printSchema()
        return df
    else:
        if verbose == True:
            print(f'INFO: Colunas a serem avaliadas {cols}')
        
        for column in cols:
            
            if verbose == True:
                print(f'INFO: Avaliando a coluna {column}')
            
            if columns_manifest[column] == 'StructType':
                if verbose == True:
                    print(f"INFO: {column} é um campo StructType")
                    print(f"INFO: Mapeando objetos dentro do struct {column}")
                struct_fields = [field.name for field in df.select(f'{column}.*').schema.fields]
                
                if verbose == True:
                    print(f"INFO: Abrindo Struct {column} nos campos {struct_fields}")
                
                df = df.select(
                        ['*'] +
                        [col(f'{column}.{struct_field}').alias(f'{column}_{struct_field}') for struct_field in struct_fields]
                ).drop(column)
                
                
            elif columns_manifest[column] == 'ArrayType':
                if verbose == True:
                    print(f"INFO: {column} é um campo ArrayType")
                    print(f"INFO: Executando explode_outer() do campo {column}")
                
                df = df.withColumn(f'{column}', explode_outer(f'{column}'))
                
            else:
                if verbose == True:
                    print(f"INFO: {column} não é um campo StructType ou ArrayType")
        if verbose == True:
            print('INFO: RESETANDO O LOOP')
    
    return unnest_struct_array(df = df)

def mapBy(dataframe, map_by, map_col_name, drop_these):
    cols_to_map = [f(x) for x in df.drop(map_by, *drop_these).columns for f in (lit, col) ]
    result_df = df.withColumn(map_col_name, create_map(cols_to_map))
    result_df = result_df.select([map_by, map_col_name])
    return result_df