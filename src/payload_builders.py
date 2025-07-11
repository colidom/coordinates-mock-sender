import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
from src.utils import load_config

config = load_config()

def create_xml_payload(imei, latitude, longitude, precision, event_type, hour_offset=0, config_xml=None):
    now_adjusted = (datetime.now() - timedelta(hours=abs(hour_offset))).strftime("%Y-%m-%d %H:%M:%S")

    message = ET.Element("Message")
    sender = ET.SubElement(message, "Sender")
    sender.text = config_xml["SENDER"]

    device = ET.SubElement(message, "Device")
    imei_elem = ET.SubElement(device, "Imei")
    imei_elem.text = imei
    battery = ET.SubElement(device, "Battery")
    battery.text = config_xml["BATTERY"]

    bracelet = ET.SubElement(message, "Bracelet")
    battery_b = ET.SubElement(bracelet, "BatteryB")
    battery_b.text = config_xml["BATTERY_B"]
    temp_b = ET.SubElement(bracelet, "TempB")
    temp_b.text = config_xml["TEMP_B"]

    event_type_elem = ET.SubElement(message, "EventType")
    event_type_elem.text = event_type

    time_elem = ET.SubElement(message, "Time")
    time_elem.text = now_adjusted

    position = ET.SubElement(message, "Position")
    lon = ET.SubElement(position, "Longitude")
    lon.text = longitude
    lat = ET.SubElement(position, "Latitude")
    lat.text = latitude
    alt = ET.SubElement(position, "Altitude")
    alt.text = config_xml["ALTITUDE"]
    prec = ET.SubElement(position, "Precision")
    prec.text = precision

    return ET.tostring(message, encoding="utf-8", method="xml").decode("utf-8"), now_adjusted


def create_json_payload(imei, lat, lng, evt, config_json=None):
    timestamp = int(time.time())

    payload = {
        "msg": "loc",
        "wifi": config_json["JSON_WIFI"],
        "evt": evt,
        "temp": int(float(config_json["TEMP_B"]) * 1000),
        "rssi": int(config_json["JSON_RSSI"]),
        "mnc": int(config_json["JSON_MNC"]),
        "sw": config_json["JSON_SW"],
        "rsrp": int(config_json["JSON_RSRP"]),
        "acl": int(config_json["JSON_ACL"]),
        "mcc": int(config_json["JSON_MCC"]),
        "ta": int(config_json["JSON_TA"]),
        "hw": config_json["JSON_HW"],
        "ct": int(config_json["JSON_CT"]),
        "bt": int(float(config_json["BATTERY_B"]) * 100),
        "rsrq": int(config_json["JSON_RSRQ"]),
        "snr": int(config_json["JSON_SNR"]),
        "imei": imei,
        "time": timestamp,
        "up": timestamp,
        "lat": lat,
        "lng": lng,
        "cid": int(config_json["JSON_CID"])
    }
    return payload

