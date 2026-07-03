# Conceitos — MQTT e Publish-Subscribe

Responsável: Alvaro

## O problema que o MQTT resolve

No modelo cliente-servidor tradicional (ex.: HTTP), quem quer um dado precisa
**pedir** (request/response) e precisa **saber o endereço** de quem tem o dado.
Em IoT, com centenas de sensores e vários consumidores de dados, esse
acoplamento não escala bem.

## O modelo publish-subscribe

- **Publisher**: produz dados e os publica em um **tópico** (ex.:
  `sensores/sala1/temperatura`). Não sabe quem vai ler.
- **Subscriber**: assina os tópicos que lhe interessam. Não sabe quem publica.
- **Broker**: intermediário central (no nosso caso, o Mosquitto) que recebe
  todas as publicações e as roteia para os assinantes de cada tópico.

Esse desacoplamento é **em espaço** (ninguém conhece o endereço de ninguém,
só do broker) e **em sincronização** (o publisher não espera resposta do
consumidor final).

## Tópicos e wildcards

Tópicos são hierárquicos, separados por `/`:

- `sensores/sala1/temperatura`
- `+` casa exatamente um nível: `sensores/+/temperatura`
- `#` casa qualquer subárvore: `sensores/#`

## QoS — Quality of Service

| QoS | Garantia          | Pacotes trocados                        |
|-----|-------------------|-----------------------------------------|
| 0   | no máximo uma vez | PUBLISH                                 |
| 1   | pelo menos uma vez| PUBLISH + PUBACK (pode duplicar)        |
| 2   | exatamente uma vez| PUBLISH + PUBREC + PUBREL + PUBCOMP     |

O MQTT roda **sobre TCP** (porta padrão 1883; 8883 com TLS). O QoS é uma
garantia **fim-a-fim na camada de aplicação**, além da confiabilidade que o
TCP já dá no transporte.

## Outros recursos usados no trabalho

- **Retained message**: o broker guarda a última mensagem retida de um tópico
  e a entrega na hora a novos assinantes ("estado atual").
- **Last Will (LWT)**: mensagem que o broker publica em nome do cliente se a
  conexão cair de forma inesperada — detecção de dispositivo offline.
- **Keepalive**: PINGREQ/PINGRESP periódicos mantêm e verificam a conexão.

## Por que MQTT em IoT?

Cabeçalho fixo de apenas 2 bytes, conexão persistente (não refaz handshake a
cada dado, como polling HTTP faria), QoS configurável e LWT tornam o
protocolo leve e adequado a dispositivos com pouca memória, bateria e rede
instável.
