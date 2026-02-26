# 🎣 Bot de Pesca Automatizado - GTA RP (Prodigy)

Bot inteligente que automatiza todo o processo de pesca no servidor **Prodigy RP** usando visão computacional e automação de teclado/mouse.

## ⚠️ AVISO IMPORTANTE

**USO POR SUA CONTA E RISCO!** 

Automatizar ações em jogos online pode violar os Termos de Serviço do servidor e resultar em **BANIMENTO PERMANENTE**. Este projeto é apenas para fins educacionais sobre automação e visão computacional.

## ✅ PRÉ-CONFIGURADO PARA PRODIGY RP

Este bot já vem configurado especificamente para o servidor **Prodigy RP** com base nas mecânicas de pesca observadas:

- ✅ Tecla **1** para equipar vara
- ✅ Tecla **E** para lançar/coletar
- ✅ Detecção de notificação azul
- ✅ Rastreamento do círculo branco no minigame
- ✅ Detecção automática de sucesso/falha

📖 **[Ver configurações específicas do Prodigy RP →](PRODIGY_RP_SETUP.md)**

## 🚀 Funcionalidades

- ✅ **Captura e análise de tela em tempo real**
- ✅ **Detecção automática de eventos de pesca**
- ✅ **Automação do minigame (seguir o peixe)**
- ✅ **Sistema de calibração fácil**
- ✅ **Controles de início/pausa (F6) e parada (ESC)**
- ✅ **Contador de peixes capturados**
- ✅ **Failsafe integrado (move mouse para canto superior esquerdo para parar)**

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Windows (Linux/Mac requer adaptações)
- Resolução de tela: 1920x1080 (outras resoluções precisam ajustar config.py)

## 🔧 Instalação

### 1. Instalar Python
Baixe e instale Python de [python.org](https://www.python.org/downloads/)

### 2. Instalar dependências

```powershell
cd C:\Users\vdesg\Desktop\FishingScript
pip install -r requirements.txt
```

### 3. Executar com permissões de administrador

**IMPORTANTE:** Execute o prompt de comando como Administrador para que o bot possa controlar teclado e mouse.

## ⚙️ Configuração

### Passo 1: Calibrar o bot

Execute o script de calibração:

```powershell
python calibrate.py
```

#### Opções de calibração:

**1. Selecionar região do minigame**
- Capture a tela durante o minigame de pesca
- Selecione a área onde o peixe aparece
- Cole os valores no `config.py` em `MINIGAME_REGION`

**2. Detectar cor do peixe/indicador**
- Capture a tela quando o peixe aparecer
- Clique no peixe/alvo
- Cole os valores HSV no `config.py`

**3. Testar detecção em tempo real**
- Veja se o bot está detectando corretamente
- Ajuste as cores se necessário

**4. Ver coordenadas do mouse**
- Útil para identificar posições específicas

### Passo 2: Configurar teclas

Edite `config.py` e ajuste:

```python
# Tecla para equipar vara de pescar
FISHING_ROD_KEY = 'e'  # Mude conforme seu servidor

# Tecla para lançar isca
CAST_KEY = 'e'

# Tecla para fisgar o peixe
HOOK_KEY = 'e'
```

### Passo 3: Ajustar timings

```python
# Tempo para esperar peixe morder (segundos)
BITE_TIMEOUT = 30

# Duração do minigame (segundos)
MINIGAME_DURATION = 15

# Delay entre ciclos
CYCLE_DELAY = 2
```

## 🎮 Como Usar

### 1. Iniciar o bot

```powershell
python fishing_bot.py
```

### 2. No jogo

1. Posicione seu personagem próximo ao local de pesca
2. Pressione **F6** para iniciar o bot
3. O bot automaticamente:
   - Equipará a vara de pescar
   - Lançará a isca
   - Esperará e detectará quando o peixe morder
   - Jogará o minigame seguindo o peixe
   - Repetirá o ciclo

### 3. Controles

- **F6**: Iniciar/Pausar bot
- **ESC**: Parar completamente
- **Mover mouse para canto superior esquerdo**: Failsafe (para emergências)

## 📁 Estrutura do Projeto

```
FishingScript/
│
├── fishing_bot.py       # Script principal
├── vision.py            # Módulo de visão computacional
├── config.py            # Configurações (EDITE AQUI!)
├── calibrate.py         # Ferramenta de calibração
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

## 🔍 Como Funciona

### 1. **Captura de Tela**
O bot captura frames da tela em tempo real usando `pyautogui` e `PIL`.

### 2. **Visão Computacional**
Usa `OpenCV` para:
- Detectar cores específicas (indicador de mordida, peixe no minigame)
- Encontrar contornos e posições de objetos
- Rastrear movimento do peixe

### 3. **Automação**
- `pyautogui`: Controla o mouse
- `keyboard`: Simula pressionar teclas

### 4. **Ciclo de Pesca**
```
Equipar Vara → Lançar Isca → Esperar Mordida → Minigame → Repetir
```

## 🎨 Calibração Avançada

### Entendendo HSV

HSV (Hue, Saturation, Value) é melhor que RGB para detectar cores:

- **Hue (Matiz)**: 0-180 (cor)
- **Saturation (Saturação)**: 0-255 (intensidade da cor)
- **Value (Valor)**: 0-255 (brilho)

### Detectar cores específicas

Use `calibrate.py` opção 2 para clicar em elementos e obter seus valores HSV.

**Exemplo de cores comuns:**
- Vermelho: `[0, 100, 100]` a `[10, 255, 255]`
- Branco: `[0, 0, 200]` a `[180, 30, 255]`
- Amarelo: `[20, 100, 100]` a `[30, 255, 255]`

### Ajustar detecção de mordida

Edite `vision.py` na função `detect_bite()`:

```python
# Método 1: Detecção por cor
lower_color = np.array([H-20, 100, 100])
upper_color = np.array([H+20, 255, 255])

# Método 2: Detecção por texto (requer pytesseract)
# Instale: pip install pytesseract
if ColorDetector.detect_text_on_screen(screenshot, "MORDED"):
    return True
```

## 🐛 Solução de Problemas

### Bot não detecta o peixe
- Recalibre a região do minigame
- Ajuste os valores de cor HSV
- Verifique se a resolução está correta

### Bot não pressiona teclas
- Execute como Administrador
- Verifique se as teclas em `config.py` estão corretas

### MouseSpeed muito lento/rápido
Ajuste em `config.py`:
```python
MOUSE_SPEED = 0.05  # Mais rápido
MOUSE_SPEED = 0.2   # Mais lento
```

### Falsos positivos na detecção
Aumente o threshold:
```python
DETECTION_THRESHOLD = 2000  # Mais rigoroso
```

## 📊 Melhorias Futuras

- [ ] Interface gráfica (GUI)
- [ ] Suporte para múltiplos servidores
- [ ] Detecção de texto com OCR
- [ ] Machine Learning para melhor precisão
- [ ] Notificações quando capturar peixe raro
- [ ] Sistema de anti-detecção (delays aleatórios)

## 🤝 Contribuindo

Este é um projeto educacional. Fique à vontade para:
- Reportar bugs
- Sugerir melhorias
- Adaptar para outros servidores

## 📝 Licença

Projeto para fins educacionais apenas. Use por sua conta e risco.

## 💡 Dicas Extras

### Segurança
1. **Sempre teste em modo janela** antes de usar fullscreen
2. **Use delays aleatórios** para parecer mais humano
3. **Não deixe rodando 24/7** - moderação é importante

### Desempenho
1. Reduza a área de captura para melhor FPS
2. Use resolução menor se possível
3. Feche programas desnecessários

### Debug
Para ver o que o bot está detectando, adicione:

```python
# Em vision.py, função find_fish_position
cv2.imshow('Debug', mask)
cv2.waitKey(1)
```

## 📞 Suporte

Problemas comuns já estão documentados acima. Para questões específicas do servidor Prodigy RP, você precisará ajustar os valores baseado nos elementos visuais únicos desse servidor.

---

**Bora automatizar essa pesca! 🎣🚀**

Mas lembre-se: *Com grandes poderes vêm grandes responsabilidades* (e possíveis bans 😅)
