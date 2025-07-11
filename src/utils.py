import os
import sys
import pandas as pd
import pprint
from dotenv import load_dotenv


import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        "URL": os.getenv("URL"),
        "URL_BLE": os.getenv("URL_BLE"),
        "APP_KEY": os.getenv("APP_KEY"),

        "IMEI_A": os.getenv("IMEI_A"),
        "IMEI_B": os.getenv("IMEI_B"),
        "IMEI_V": os.getenv("IMEI_V"),

        # XML
        "SENDER": os.getenv("SENDER"),
        "BATTERY": os.getenv("BATTERY"),
        "BATTERY_B": os.getenv("BATTERY_B"),
        "TEMP_B": os.getenv("TEMP_B"),
        "EVENT_TYPE": os.getenv("EVENT_TYPE"),
        "ALTITUDE": os.getenv("ALTITUDE"),

        # JSON (brazalete)
        "JSON_WIFI": os.getenv("JSON_WIFI"),
        "JSON_RSSI": os.getenv("JSON_RSSI"),
        "JSON_MNC": os.getenv("JSON_MNC"),
        "JSON_SW": os.getenv("JSON_SW"),
        "JSON_LNG": os.getenv("JSON_LNG"),
        "JSON_RSRP": os.getenv("JSON_RSRP"),
        "JSON_ACL": os.getenv("JSON_ACL"),
        "JSON_MCC": os.getenv("JSON_MCC"),
        "JSON_TA": os.getenv("JSON_TA"),
        "JSON_HW": os.getenv("JSON_HW"),
        "JSON_CT": os.getenv("JSON_CT"),
        "JSON_RSRQ": os.getenv("JSON_RSRQ"),
        "JSON_SNR": os.getenv("JSON_SNR"),
        "JSON_CID": os.getenv("JSON_CID"),

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

def list_data_files(data_folder):
    """Lista los archivos de datos en la carpeta especificada."""
    files = [f for f in os.listdir(data_folder) if f.endswith(".xlsx")]
    return files

def choose_file(file_type):
    """Permite al usuario elegir un archivo de datos de un tipo específico."""
    files = list_data_files("data")
    print(f"\nFicheros disponibles de {file_type}:")
    for i, f in enumerate(files):
        print(f"{i + 1}. {f}")
    print("0. Salir")

    while True:
        try:
            choice = int(input(f"Por favor elige el fichero de tipo {file_type} a procesar (1-{len(files)} o 0 para salir): "))
            if choice == 0:
                print("👋 Saliendo de la aplicación...")
                sys.exit(0)
            elif 1 <= choice <= len(files):
                print(f"Has elegido el fichero: {files[choice - 1]}")
                return os.path.join("data", files[choice - 1])
        except ValueError:
            pass
        print("⚠️ Opción inválida. Por favor inténtalo de nuevo.")


def choose_devices_to_send():
    """Pregunta al usuario qué dispositivos desea simular."""
    print("\n¿Qué dispositivos deseas enviar?")
    print("1. Inculpado")
    print("2. Víctima")
    print("3. Brazalete")
    print("Puedes elegir múltiples separados por coma, ejemplo: 1,3 o 1,2,3")

    while True:
        choice = input("Selecciona opciones: ").replace(" ", "")
        selections = choice.split(",")
        valid = {"1", "2", "3"}
        if all(c in valid for c in selections):
            return set(selections)
        print("⚠️ Opción inválida. Intenta de nuevo.")

import pprint

def print_trace(device_type, index, lat, lon, precision, payload, payload_type="XML"):
    print(f"[{device_type}] Índice: {index} - Lat: {lat}, Lon: {lon}, Prec: {precision}")
    if payload_type.upper() == "JSON":
        pprint.pprint(payload)
    else:
        print(payload)
    print()  # Línea en blanco para separar
