"""
Sensor de temperatura simulado (PUBLISHER).
Responsável: Gabriel

Publica leituras em JSON no tópico 'sensores/sala1/temperatura' a cada 2s.
O sensor NÃO sabe quem vai receber os dados: ele apenas entrega ao broker.
"""

import json
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORTA = 1883
TOPICO = "sensores/sala1/temperatura"
INTERVALO_S = 2


def ao_conectar(client, userdata, flags, reason_code, properties):
    print(f"[sensor-temp] Conectado ao broker {BROKER}:{PORTA} (rc={reason_code})")


def main():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="sensor-temperatura-sala1",
    )
    client.on_connect = ao_conectar
    client.connect(BROKER, PORTA, keepalive=60)
    client.loop_start()

    try:
        while True:
            leitura = {
                "sensor": "temp-sala1",
                "valor": round(random.uniform(18.0, 34.0), 1),
                "unidade": "C",
                "timestamp": time.strftime("%H:%M:%S"),
            }
            payload = json.dumps(leitura)
            # QoS 1 = o broker confirma o recebimento (PUBACK)
            info = client.publish(TOPICO, payload, qos=1)
            info.wait_for_publish()
            print(f"[sensor-temp] Publicado em '{TOPICO}': {payload}")
            time.sleep(INTERVALO_S)
    except KeyboardInterrupt:
        print("\n[sensor-temp] Encerrando...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
