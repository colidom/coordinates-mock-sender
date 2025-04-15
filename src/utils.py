import os
import pandas as pd
from dotenv import load_dotenv


def load_config():
    """Carga las variables de entorno y devuelve un diccionario con la configuración."""
    load_dotenv()

    return {
        "URL": os.getenv("URL"),
        "APP_KEY": os.getenv("APP_KEY"),
        "IMEI_V": os.getenv("IMEI_V"),
        "IMEI_A": os.getenv("IMEI_A"),
        "DATA_PATH_V": os.getenv("DATA_PATH_V"),
        "DATA_PATH_A": os.getenv("DATA_PATH_A"),
        "SENDER": os.getenv("SENDER"),
        "BATTERY": os.getenv("BATTERY"),
        "BATTERY_B": os.getenv("BATTERY_B"),
        "TEMP_B": os.getenv("TEMP_B"),
        "EVENT_TYPE": os.getenv("EVENT_TYPE"),
        "ALTITUDE": os.getenv("ALTITUDE"),
        "REQUEST_INTERVAL": int(os.getenv("REQUEST_INTERVAL", 15)),
        "HEADERS": {
            "appKey": os.getenv("APP_KEY"),
            "Content-Type": "text/xml"
        }
    }

def load_coordinates(data_path):
    """Carga las coordenadas desde el archivo Excel."""
    df = pd.read_excel(data_path)
    return df[["precision", "location"]]

def get_next_coordinate(df, index):
    """Obtiene la siguiente coordenada del DataFrame."""
    row = df.iloc[index % len(df)]
    precision = str(row["precision"])
    latitude, longitude = row["location"].split(",")
    return latitude.strip(), longitude.strip(), precision

def list_data_files():
    data_folder = "./data"
    files = [f for f in os.listdir(data_folder) if f.endswith(".xlsx")]
    return files


def choose_file(file_type):
    files = list_data_files()
    print(f"\nFicheros disponibles de {file_type}:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")

    while True:
        try:
            choice = int(input(f"Por favor elige el fichero de tipo {file_type} a procesar (1-{len(files)}): "))
            if 1 <= choice <= len(files):
                return os.path.join("data", files[choice - 1])
        except ValueError:
            pass
        print("⚠️ Invalid option. Please try again.")
