# 🛡️ SentinelNet - Para vários Estados

O **SentinelNet** é um launcher de monitoramento de rede e unidades desenvolvido para garantir a alta disponibilidade de sistemas em regiões distribuídas. O foco do projeto é a **auto-recuperação (Self-Healing)** e a comunicação ágil com equipes de TI.

## Funcionalidades
* **Monitoramento em Tempo Real:** Interface intuitiva em modo Dark para acompanhamento de múltiplas unidades.
* **Protocolo de Auto-Recuperação:** O sistema tenta realizar reparos automáticos via software antes de escalar o problema.
* **Alertas Inteligentes via Telegram:** * ✅ Notificação de reparo bem-sucedido (sem necessidade de deslocamento).
  * Alerta de queda física com botões interativos para a equipe técnica.
* **Interface Moderna:** Construído com `CustomTkinter` para uma experiência de usuário (UX) premium.

## Tecnologias Utilizadas
* Python 3.x
* CustomTkinter (Interface Gráfica)
* Requests (Integração com API do Telegram)
* Threading (Processamento paralelo para monitoramento sem travamentos)
