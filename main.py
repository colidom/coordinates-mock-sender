from src.utils import choose_devices_to_send, choose_file, load_coordinates, get_next_coordinate, load_config, print_trace
from src.payload_builders import create_xml_payload, create_json_payload
from src.request_handler import send_request
from datetime import datetime
import time

config = load_config()

SEND_REQUESTS = True  # Cambia a True para enviar las peticiones

if __name__ == "__main__":
    selected_devices = choose_devices_to_send()

    path_agresor = None
    path_victima = None
    path_brazalete = None

    if "1" in selected_devices:
        path_agresor = choose_file("Inculpado")
    if "2" in selected_devices:
        path_victima = choose_file("Víctima")
    if "3" in selected_devices:
        path_brazalete = choose_file("Brazalete")

    # Cargar dataframes
    coordinates_a_df = load_coordinates(path_agresor) if path_agresor else None
    coordinates_v_df = load_coordinates(path_victima) if path_victima else None
    coordinates_b_df = load_coordinates(path_brazalete) if path_brazalete else None

    index = 0
    while True:
        if "1" in selected_devices and coordinates_a_df is not None:
            lat_a, lon_a, prec_a = get_next_coordinate(coordinates_a_df, index)
            xml_data_a, time_sent_a = create_xml_payload(config["IMEI_A"], lat_a, lon_a, prec_a, config["EVENT_TYPE"], config)
            print_trace("Inculpado", index + 1, lat_a, lon_a, prec_a, xml_data_a, "XML")
            if SEND_REQUESTS:
                send_request(index + 1, config["IMEI_A"], lat_a, lon_a, xml_data_a, "aggressorMessage", time_sent_a)

        if "2" in selected_devices and coordinates_v_df is not None:
            lat_v, lon_v, prec_v = get_next_coordinate(coordinates_v_df, index)
            xml_data_v, time_sent_v = create_xml_payload(config["IMEI_V"], lat_v, lon_v, prec_v, config["EVENT_TYPE"], config)
            print_trace("Víctima", index + 1, lat_v, lon_v, prec_v, xml_data_v, "XML")
            if SEND_REQUESTS:
                send_request(index + 1, config["IMEI_V"], lat_v, lon_v, xml_data_v, "victimMessage", time_sent_v)

        if "3" in selected_devices and coordinates_b_df is not None:
            lat_b, lng_b, prec_b = get_next_coordinate(coordinates_b_df, index)
            json_data_b = create_json_payload(config["IMEI_B"], lat_b, lng_b, config)
            print_trace("Brazalete", index + 1, lat_b, lng_b, prec_b, json_data_b, "JSON")
            if SEND_REQUESTS:
                send_request(index + 1, config["IMEI_B"], lat_b, lng_b, json_data_b, "receiveMessage", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        index += 1

        time.sleep(config["REQUEST_INTERVAL"])
