# Captura e análise de tráfego MQTT

Responsável: Alvaro

## Wireshark

1. Abra o Wireshark e capture na interface **loopback** (`lo` no Linux,
   "Loopback/Npcap Loopback" no Windows), já que broker e clientes rodam na
   mesma máquina.
2. Aplique o filtro de exibição:

   ```
   mqtt
   ```

   Para ver também o TCP por baixo: `tcp.port == 1883`.

3. Rode os scripts do projeto e observe, em ordem:

| Pacote MQTT        | Quando aparece                                        |
|--------------------|-------------------------------------------------------|
| CONNECT / CONNACK  | Cliente abre sessão com o broker (após handshake TCP) |
| SUBSCRIBE / SUBACK | Subscriber assina um tópico                           |
| PUBLISH            | Sensor envia leitura (payload JSON visível em claro!) |
| PUBACK             | Confirmação de QoS 1                                  |
| PUBREC/PUBREL/PUBCOMP | Handshake de 4 vias do QoS 2 (rodar `qos/teste_qos.py`) |
| PINGREQ / PINGRESP | Keepalive periódico                                   |
| DISCONNECT         | Encerramento educado (Ctrl+C nos scripts)             |

## Pontos para destacar na demonstração

- Antes do CONNECT existe o **handshake TCP (SYN, SYN-ACK, ACK)**: o MQTT
  roda sobre TCP.
- No PUBLISH dá para expandir o pacote e ler o **tópico e o JSON em texto
  claro** — evidência de que, sem TLS, não há confidencialidade.
- Comparar a quantidade de pacotes de um PUBLISH com QoS 0, 1 e 2.
- Observar que um único PUBLISH do sensor gera **duas entregas** do broker
  (uma para cada subscriber) — o roteamento por tópico acontecendo.

## Alternativa por linha de comando

```bash
# assinar tudo e ver as mensagens chegando
docker exec -it broker-grupo9 mosquitto_sub -t '#' -v

# publicar manualmente uma mensagem de teste
docker exec -it broker-grupo9 mosquitto_pub -t 'sensores/sala2/temperatura' \
  -m '{"sensor":"manual","valor":99,"unidade":"C","timestamp":"agora"}'
```

O `tcpdump` também serve para gravar a captura e abrir depois no Wireshark:

```bash
sudo tcpdump -i lo port 1883 -w captura_mqtt.pcap
```
