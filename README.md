# Coordinates-mock-sender

Este script envía periódicamente solicitudes POST con datos XML a un servicio web, utilizando coordenadas y precisión obtenidas de dos archivos Excel. Los datos enviados incluyen información sobre dos dispositivos (por ejemplo, un dispositivo de la víctima y otro del inculpado). El script lee las coordenadas de cada archivo Excel y las envía cada cierto intervalo de tiempo (por defecto, 15 segundos), alternando entre los dispositivos.

## Requisitos

- Python 3.6 o superior
- Librerías:
  - `requests`
  - `pandas`
  - `python-dotenv`
  - `openpyxl` (para leer archivos `.xlsx`)

## Instalación

1. Clona este repositorio o descarga los archivos.
2. Crea un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    ```
3. Activa el entorno virtual:
    - En Windows:
      ```bash
      venv\Scripts\activate
      ```
    - En macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno (sin necesidad de especificar los archivos de coordenadas, ya que se eligen al iniciar el script):

```env
URL=tu_url_del_servicio
APP_KEY=tu_app_key
IMEI_V=imei_del_dispositivo_victima
IMEI_A=imei_del_dispositivo_inculpado
SENDER=Intellicare
BATTERY=84.0
BATTERY_B=80.0
TEMP_B=0.0
EVENT_TYPE=CYC
ALTITUDE=179
REQUEST_INTERVAL=15

Uso

    Asegúrate de que el archivo .env está correctamente configurado.

    Coloca todos los archivos .xlsx con coordenadas en el directorio ./data/.

    Ejecuta el script principal:

    python main.py

    Al iniciar, el script listará los archivos disponibles en la carpeta data y te pedirá que selecciones:

        Un archivo para el dispositivo del inculpado.

        Otro archivo para el dispositivo de la víctima.

    El script comenzará a enviar las solicitudes POST periódicamente, alternando entre las coordenadas de ambos dispositivos.

Ejemplo de salida

=== Selección de archivos ===

Archivos disponibles para Inculpado:
1. ruta_inculpado_01.xlsx
2. ruta_inculpado_02.xlsx
...

Por favor elija el fichero de tipo Inculpado que desea procesar (1-2): 1

Archivos disponibles para Víctima:
1. ruta_victima_01.xlsx
2. ruta_victima_02.xlsx
...

Por favor elija el fichero de tipo Víctima que desea procesar (1-2): 2

Petición: 1
Dispositivo: 352701641669459
Longitud: -1.8317908
Latitud: 41.0714056
Hora de la petición (local): 16:09:31
Hora enviada en XML (ajustada -2h): 14:09:31
Código de respuesta: 200

Notas

    El script usa la librería requests para enviar las solicitudes y xml.etree.ElementTree para generar los datos XML.

    Las coordenadas se extraen dinámicamente de archivos Excel elegidos por el usuario en tiempo de ejecución.

    El campo <Time> dentro del XML se ajusta con el parámetro hour_offset.

    Si no se desea verificar el certificado SSL (por ejemplo en entornos de pruebas), se usa verify=False en la petición.

    Para suprimir las advertencias de seguridad por certificados, se incluye:

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.