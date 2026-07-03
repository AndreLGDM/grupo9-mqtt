"""
Demonstração dos níveis de QoS do MQTT.
Responsável: Pedro

Publica a mesma mensagem três vezes, com QoS 0, 1 e 2, no tópico
'demo/qos'. Com o Wireshark aberto (filtro 'mqtt'), dá para ver a
diferença no número de pacotes trocados:

  QoS 0 (no máximo 1x): PUBLISH                            -> "fire and forget"
  QoS 1 (pelo menos 1x): PUBLISH + PUBACK                  -> pode duplicar
  QoS 2 (exatamente 1x): PUBLISH + PUBREC + PUBREL + PUBCOMP -> handshake de 4 vias
"""

import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORTA = 1883
TOPICO = "demo/qos"


def ao_publicar(client, userdata, mid, reason_code, properties):
    print(f"  -> confirmação do broker recebida (mid={mid})")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="demo-qos")
    client.on_publish = ao_publicar
    client.connect(BROKER, PORTA, keepalive=60)
    client.loop_start()
    time.sleep(0.5)

    for qos in (0, 1, 2):
        print(f"\nPublicando com QoS {qos}...")
        info = client.publish(TOPICO, f"mensagem de teste com QoS {qos}", qos=qos)
        info.wait_for_publish()
        time.sleep(1)  # pausa para separar os pacotes na captura

    print("\nAbra o Wireshark e compare a quantidade de pacotes MQTT por QoS.")
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
