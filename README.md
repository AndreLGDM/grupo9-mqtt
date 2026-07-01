# Grupo 9 — Publish-Subscribe com MQTT

Sistema de sensores simulados que publicam dados em um broker MQTT (Mosquitto),
com múltiplos clientes assinando tópicos diferentes.

**Integrantes:** André, Gabriel, Marcus, Pedro e Alvaro

## Arquitetura

```
[sensor_temperatura.py] ──┐                      ┌──> [monitor_geral.py]      (assina sensores/#)
                          ├──> [Broker Mosquitto]┤
[sensor_umidade.py] ──────┘        (porta 1883)  └──> [alerta_temperatura.py] (assina sensores/+/temperatura)
```

Os publishers **não conhecem** os subscribers e vice-versa. Toda a comunicação
passa pelo broker, que roteia as mensagens com base nos **tópicos**.

## Requisitos

- Docker e Docker Compose (para o broker)
- Python 3.10+
- Dependências Python: `pip install -r requirements.txt`

## Como executar

### 1. Subir o broker Mosquitto

```bash
docker compose up -d
docker compose logs -f mosquitto   # ver logs do broker
```

O broker fica disponível em `localhost:1883`.

### 2. Iniciar os subscribers (cada um em um terminal)

```bash
python subscribers/monitor_geral.py
python subscribers/alerta_temperatura.py
```

### 3. Iniciar os publishers (cada um em um terminal)

```bash
python publishers/sensor_temperatura.py
python publishers/sensor_umidade.py
```

### 4. Demonstrações extras

```bash
python qos/teste_qos.py          # compara QoS 0, 1 e 2
python qos/ultima_vontade.py     # demonstra Last Will Testament (LWT) e mensagem retida
```

### 5. Captura de tráfego

Ver `docs/captura_trafego.md` para o passo a passo com Wireshark
(filtro `mqtt` na interface loopback).

## Estrutura do repositório

| Pasta / arquivo            | Responsável | Conteúdo                                      |
|----------------------------|-------------|-----------------------------------------------|
| `docker-compose.yml`, `mosquitto/` | André   | Infraestrutura do broker                      |
| `publishers/`              | Gabriel     | Sensores simulados (publicadores)             |
| `subscribers/`             | Marcus      | Clientes assinantes (tópicos e wildcards)     |
| `qos/`                     | Pedro       | Demonstrações de QoS, retained e Last Will    |
| `docs/`                    | Alvaro      | Conceitos, captura de tráfego e limitações    |

## Fluxo de trabalho Git

Ver `GUIA_GIT.md`: cada integrante commita sua parte em uma branch própria e
abre um Pull Request; o André faz o merge na `main`.
