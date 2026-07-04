"""
Sensor de umidade simulado (PUBLISHER).
Responsável: Gabriel

Publica leituras em JSON no tópico 'sensores/sala1/umidade' a cada 3s.
Junto com o sensor de temperatura, demonstra que vários publishers podem
usar o MESMO broker com tópicos diferentes.
"""

import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORTA = 1883
TOPICO = "sensores/sala1/umidade"
INTERVALO_S = 3


def ao_conectar(client, userdata, flags, reason_code, properties):
    print(f"[sensor-umid] Conectado ao broker {BROKER}:{PORTA} (rc={reason_code})")


def main():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="sensor-umidade-sala1",
    )
    client.on_connect = ao_conectar
    client.connect(BROKER, PORTA, keepalive=60)
    client.loop_start()

    try:
        while True:
            leitura = {
                "sensor": "umid-sala1",
                "valor": round(random.uniform(40.0, 90.0), 1),
                "unidade": "%",
                "timestamp": time.strftime("%H:%M:%S"),
            }
            payload = json.dumps(leitura)
            info = client.publish(TOPICO, payload, qos=1)
            info.wait_for_publish()
            print(f"[sensor-umid] Publicado em '{TOPICO}': {payload}")
            time.sleep(INTERVALO_S)
    except KeyboardInterrupt:
        print("\n[sensor-umid] Encerrando...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
