import requests
import urllib3
import json
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout, RequestException
from src.utils import load_config


config = load_config()
URL = config["URL"]
URL_BLE = config["URL_BLE"]
HEADERS = config.get("HEADERS", {})

def send_request(iteration, imei, latitude, longitude, payload, request_type, time_sent):
    """Envía la solicitud POST con XML o JSON y traza los datos enviados."""
    if "receiveMessage" == request_type:
        endpoint = f"/services/{request_type}?postParameter=json"
        full_url = f"{URL_BLE}{endpoint}"
    else:
        endpoint = f"/services/{request_type}?postParameter=payload"
        full_url = f"{URL}{endpoint}"
    now_local = datetime.now().strftime("%H:%M:%S")

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        # Ajustar Content-Type según tipo de payload
        headers = HEADERS.copy()
        if isinstance(payload, dict):
            headers["Content-Type"] = "application/json"
            response = requests.post(full_url, headers=headers, json=payload, verify=False)
        else:
            headers["Content-Type"] = "application/xml"
            response = requests.post(full_url, headers=headers, data=payload, verify=False)

        # Logging
        print(f"\nPetición: {iteration}")
        print(f"\nEndpoint: {full_url}")
        print(f"Dispositivo: {imei}")
        print(f"Longitud: {longitude}")
        print(f"Latitud: {latitude}")
        print(f"Hora de la petición (local): {now_local}")
        print(f"Hora enviada en XML/JSON (ajustada): {time_sent}")
        print(f"Código de respuesta: {response.status_code}\n")

    except ConnectionError:
        print(f"\n❌ Error de conexión en la petición {iteration}. Posiblemente se ha caído la red o la VPN.")
    except Timeout:
        print(f"\n⏳ Tiempo de espera agotado en la petición {iteration}.")
    except RequestException as e:
        print(f"\n⚠️ Error inesperado en la petición {iteration}: {e}")
