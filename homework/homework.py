"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

#librerias
import os
import glob
import pandas as pd
import zipfile

def clean_campaign_data():
    # Entrada
    input_directory = "files/input"
    #creado
    os.makedirs("files/output", exist_ok=True)

    # DataFrame
    clients = pd.DataFrame(columns=["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"])
    campaign = pd.DataFrame(columns=["client_id", "number_contacts", "contact_duration","previous_campaign_contacts", "previous_outcome","campaign_outcome", "last_contact_date"])
    economics = pd.DataFrame(columns=["client_id", "cons_price_idx", "euribor_three_months"])

    #Entrada
    zip_files = glob.glob(f"{input_directory}/*.zip")
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as z:
            for file_name in z.namelist():
                with z.open(file_name) as f:
                    DataFrame = pd.read_csv(f, delimiter=",", header=0)
                    
                    # Visualizar
                    if len(DataFrame) > 0:
                        print(DataFrame.head(), "\n")
                    
                    # Clients
                    client_columns = clients.columns.intersection(DataFrame.columns)
                    clients = pd.concat([clients, DataFrame[client_columns]], ignore_index=True)
                    
                    # Campaign
                    DataFrame["last_contact_date"] = "2022-" + DataFrame["month"].map(str) + "-" + DataFrame["day"].map(str)
                    campaign_columns = campaign.columns.intersection(DataFrame.columns)
                    campaign = pd.concat([campaign, DataFrame[campaign_columns]], ignore_index=True)
                    
                    # Economics
                    econ_columns = economics.columns.intersection(DataFrame.columns)
                    economics = pd.concat([economics, DataFrame[econ_columns]], ignore_index=True)

    # Cambios
    # Clients
    clients["job"] = clients["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    clients["education"] = clients["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    clients["credit_default"] = clients["credit_default"].map(lambda x: 1 if x == "yes" else 0)
    clients["mortgage"] = clients["mortgage"].map(lambda x: 1 if x == "yes" else 0)

    #Cambios
    # campaign
    campaign["previous_outcome"] = campaign["previous_outcome"].map(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].map(lambda x: 1 if x == "yes" else 0)
    campaign["last_contact_date"] = pd.to_datetime(campaign["last_contact_date"], format='%Y-%b-%d')

    # Guardar
    clients.to_csv("files/output/client.csv", index=False)
    campaign.to_csv("files/output/campaign.csv", index=False)
    economics.to_csv("files/output/economics.csv", index=False)

if __name__ == "__main__":
    clean_campaign_data()





"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
            


if __name__ == "__main__":
    clean_campaign_data()
