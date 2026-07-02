"""
Monitor geral (SUBSCRIBER).
Responsável: Marcus

Assina 'sensores/#' (wildcard multinível) e recebe TUDO que qualquer sensor
publicar abaixo de 'sensores/'. Demonstra o desacoplamento do modelo
publish-subscribe: este cliente não precisa saber quantos sensores existem.
"""

import json

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORTA = 1883
TOPICO = "sensores/#"  # '#' casa com qualquer quantidade de níveis


def ao_conectar(client, userdata, flags, reason_code, properties):
    print(f"[monitor] Conectado (rc={reason_code}). Assinando '{TOPICO}'...")
    client.subscribe(TOPICO, qos=1)


def ao_receber(client, userdata, msg):
    try:
        dados = json.loads(msg.payload.decode())
        print(f"[monitor] {msg.topic} -> {dados['valor']}{dados['unidade']} "
              f"(sensor={dados['sensor']}, hora={dados['timestamp']}, qos={msg.qos})")
    except (json.JSONDecodeError, KeyError):
        print(f"[monitor] {msg.topic} -> {msg.payload.decode()} (payload não-JSON)")


def main():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="monitor-geral",
    )
    client.on_connect = ao_conectar
    client.on_message = ao_receber
    client.connect(BROKER, PORTA, keepalive=60)
    print("[monitor] Aguardando mensagens (Ctrl+C para sair)...")
    client.loop_forever()


if __name__ == "__main__":
    main()
