"""
Alerta de temperatura (SUBSCRIBER seletivo).
Responsável: Marcus

Assina 'sensores/+/temperatura' (wildcard de UM nível): recebe a temperatura
de qualquer sala, mas ignora umidade e outros tipos de leitura.
Dispara um alerta quando o valor passa de 30°C.

Demonstra a filtragem por tópico: dois subscribers no mesmo broker podem
receber conjuntos diferentes de mensagens.
"""

import json

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORTA = 1883
TOPICO = "sensores/+/temperatura"  # '+' casa com exatamente um nível
LIMITE_C = 30.0


def ao_conectar(client, userdata, flags, reason_code, properties):
    print(f"[alerta] Conectado (rc={reason_code}). Assinando '{TOPICO}'...")
    client.subscribe(TOPICO, qos=1)


def ao_receber(client, userdata, msg):
    dados = json.loads(msg.payload.decode())
    valor = dados["valor"]
    if valor > LIMITE_C:
        print(f"[alerta] *** ALERTA: {msg.topic} = {valor}°C (acima de {LIMITE_C}°C) ***")
    else:
        print(f"[alerta] ok: {msg.topic} = {valor}°C")


def main():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="alerta-temperatura",
    )
    client.on_connect = ao_conectar
    client.on_message = ao_receber
    client.connect(BROKER, PORTA, keepalive=60)
    print("[alerta] Monitorando temperaturas (Ctrl+C para sair)...")
    client.loop_forever()


if __name__ == "__main__":
    main()
