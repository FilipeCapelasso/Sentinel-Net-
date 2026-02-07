# 🛡️ SentinelNet - Para vários Estados

O **SentinelNet** é um launcher de monitoramento de rede e unidades desenvolvido para garantir a alta disponibilidade de sistemas em regiões distribuídas. O foco do projeto é a **auto-recuperação (Self-Healing)** e a comunicação ágil com equipes de TI.

## Funcionalidades
* **Monitoramento em Tempo Real:** Interface intuitiva em modo Dark para acompanhamento de múltiplas unidades.
* **Protocolo de Auto-Recuperação:** O sistema tenta realizar reparos automáticos via software antes de escalar o problema.
* **Alertas Inteligentes via Telegram:** * ✅ Notificação de reparo bem-sucedido (sem necessidade de deslocamento).
  * Alerta de queda física com botões interativos para a equipe técnica.
* **Interface Moderna:** Construído com `CustomTkinter` para uma experiência de usuário (UX) premium.

## Tecnologias Utilizadas
* Python 3.14
* CustomTkinter (Interface Gráfica)
* Requests (Integração com API do Telegram)
* Threading (Processamento paralelo para monitoramento sem travamentos)

## Configuração do Bot (Telegram)

Para que o **SentinelNet** envie alertas para o seu celular, siga os passos abaixo:

1. **Criar o Bot:**
   - Procure o [@BotFather](https://t.me/botfather) no Telegram.
   - Digite `/newbot` e siga as instruções para dar um nome ao seu robô.
   - O BotFather enviará um **API TOKEN**. Guarde-o.

2. **Obter seu ID de Usuário:**
   - Procure o [@userinfobot](https://t.me/userinfobot) no Telegram.
   - Envie qualquer mensagem para ele e ele responderá com o seu `Id`.

3. **Configurar o Script:**
   - No arquivo substitua as variáveis abaixo pelos dados que você obteve:
   ```python
   self.token = "SEU_TOKEN_AQUI"
   self.chat_id = "SEU_ID_AQUI"
