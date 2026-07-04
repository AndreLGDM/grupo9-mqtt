# Limitações do experimento

Responsável: Alvaro

1. **Ambiente local**: broker e todos os clientes rodam na mesma máquina
   (loopback). Não há latência, perda de pacotes nem instabilidade reais de
   uma rede de IoT em campo.

2. **Sensores simulados**: os valores são gerados com `random`, não vêm de
   hardware real (ESP32, DHT22 etc.). O comportamento elétrico/físico do
   sensor não é avaliado.

3. **Sem segurança real**: o broker aceita conexões anônimas
   (`allow_anonymous true`) e o tráfego vai em texto claro na porta 1883.
   Em produção seriam necessários autenticação (usuário/senha ou
   certificados), TLS na porta 8883 e ACLs por tópico.

4. **Poucos clientes**: testamos com 2 publishers e 2 subscribers. Não
   avaliamos escalabilidade do broker com milhares de conexões simultâneas.

5. **Broker único**: o Mosquitto é um ponto único de falha no experimento.
   Cenários reais podem exigir cluster/bridge de brokers.

6. **QoS observado sem perdas reais**: como a rede local não perde pacotes,
   a diferença prática entre QoS 0, 1 e 2 aparece apenas na quantidade de
   pacotes de confirmação, não em recuperação de mensagens perdidas.
