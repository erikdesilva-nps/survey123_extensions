from os import remove
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from keyring import get_credential
from pandas import read_sql_query
from arcgis.gis import GIS, Item


def update_picklists(item_id, sql_schema, table_name, field_map):
    """Updates hosted csv file which is used by Survey123 in select_from_file questions.

    Updates the csv file hosted in ArcGIS Online / Portal. CSV linking must be used for
    'select_x_from_file' question types in the form, and content linking must be enabled on these
    forms. The field map dictionary shoould be constructed using the format {input_field: output_field}.
    Output tables must contain 'name' and 'label' fields at a minimum. Additional optional
    fields may be included to drive cascading select type questions. ArGIS Online or Portal
    login credentials must be saved in the Window Credential Manager as 'Generic Credentials'.
    Note: linked content csvs are currently only supported by the field application. Any changes
    made to picklists contained in linked content csv files will not be reflected in a Survey123 web
    form.

    Parameters
    ----------
    item_id : str
        The item id of the target hosted .csv
    sql_schema : str
        String which represents the name of the schema which owns the SQL table
    table_name : str
        String which represents the name of the SQL table
    field_map : dict
        Dictionary of input SQL field names and their corresponding output csv field names
    """

    portal_url = r'https://nps.maps.arcgis.com'  # Change to portal URL once migrated
    # Windows credentials will need to be updated as well. Maybe make variable?
    agol_credentials = get_credential(portal_url, 'GRCA_GIS')

    # Code to initiate connection to SQL server
    # Update to correct windows credentials. Maybe make variable?
    sql_credential = get_credential('sql_login', 'postgres')
    conn_dict = {
        'drivername': 'postgresql',  # Change drivername to correct driver for target platform
        'username': sql_credential.username,
        'password': sql_credential.password,
        'host': '127.0.0.1',  # set to host IP or path
        'port': '5432'
    }
    conn_url = URL.create(**conn_dict)
    engine = create_engine(conn_url)

    # Fetch item from AGOL/portal
    gis = GIS(url=portal_url,
              username=agol_credentials.username,
              password=agol_credentials.password)
    item = Item(gis, item_id)

    # Construct query string
    field_qry_list = []
    for key, value in field_map.items():
        field_qry_list.append(f'{key} AS {value}')
    field_string = ', '.join(field_qry_list)

    # Query SQL table
    sql_query = f'''SELECT {field_string} FROM {sql_schema}.{table_name};'''
    updated_table = read_sql_query(sql_query, engine)
    # Save to disk. Potential optimization is to use in-memory csv serialization, but I can't get it to work
    output = 'temp_csv.csv'
    updated_table.to_csv(output, index=False)
    # Push table to AGOL
    item.update(data=output)
    # Delete temporary csv file
    remove(output)
