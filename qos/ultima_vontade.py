"""
Demonstração de Last Will (LWT) e mensagem retida (retained).
Responsável: Pedro

1. RETAINED: publicamos o status "online" com retain=True. O broker guarda a
   última mensagem retida do tópico e a entrega imediatamente a qualquer
   subscriber novo — útil para "estado atual" de um dispositivo IoT.

2. LAST WILL: ao conectar, o cliente registra um "testamento". Se ele cair
   sem se despedir (sem enviar DISCONNECT — ex.: mate o processo com
   'kill -9' ou desligue a rede), o BROKER publica sozinho a mensagem
   "offline (inesperado)" no tópico de status.

Para observar: em outro terminal, assine o tópico de status:
    docker exec -it broker-grupo9 mosquitto_sub -t 'dispositivos/+/status' -v
"""

import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORTA = 1883
TOPICO_STATUS = "dispositivos/sensor01/status"


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="sensor01")

    # Registrado ANTES do connect: o broker publica isso se a conexão cair
    client.will_set(TOPICO_STATUS, "offline (inesperado)", qos=1, retain=True)

    client.connect(BROKER, PORTA, keepalive=15)
    client.loop_start()

    # Mensagem retida: novos subscribers recebem o status na hora
    client.publish(TOPICO_STATUS, "online", qos=1, retain=True)
    print(f"Status 'online' publicado (retained) em '{TOPICO_STATUS}'.")
    print("Simule uma queda abrupta com: kill -9 <pid deste processo>")
    print("e veja o broker publicar o Last Will sozinho.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Saída "educada": publica offline normal e manda DISCONNECT,
        # então o Last Will NÃO é disparado.
        client.publish(TOPICO_STATUS, "offline (normal)", qos=1, retain=True)
        time.sleep(0.5)
        client.loop_stop()
        client.disconnect()
        print("Desconectado normalmente (Last Will não disparado).")


if __name__ == "__main__":
    main()
