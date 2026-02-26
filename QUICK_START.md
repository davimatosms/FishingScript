# ⚡ INÍCIO RÁPIDO - 5 MINUTOS

## 📋 Pré-requisitos
- ✅ Windows
- ✅ Python 3.8+ instalado
- ✅ GTA V com acesso ao servidor Prodigy RP
- ✅ Resolução 1920x1080 (recomendado)

## 🚀 Passo a Passo

### 1️⃣ Instalação (2 minutos)

**Abra o PowerShell como Administrador** e execute:

```powershell
cd C:\Users\vdesg\Desktop\FishingScript
pip install -r requirements.txt
```

**OU simplesmente clique duas vezes em:**
```
setup.bat
```

### 2️⃣ Primeira Calibração (2 minutos)

**Execute:**
```powershell
python calibrate.py
```

**Siga os passos:**

1. **Escolha opção 1** - Selecionar região do minigame
   - Inicie uma pesca no jogo
   - Quando o círculo azul aparecer, pressione ESPAÇO
   - Selecione a área circular com o mouse
   - Pressione ENTER
   - Copie o valor `MINIGAME_REGION` mostrado

2. **Edite config.py** e cole o valor:
   ```python
   MINIGAME_REGION = (x, y, largura, altura)  # Use os valores copiados
   ```

3. **Escolha opção 3** - Testar detecção
   - Inicie o minigame no jogo
   - Veja se o círculo branco é detectado (marcador verde)
   - Se não detectar, ajuste as cores no config.py

### 3️⃣ Usar o Bot (1 minuto)

1. **No jogo:**
   - Posicione seu personagem no local de pesca
   - Tenha a vara de pesca no inventário (slot 1)

2. **Execute o bot:**
   ```powershell
   python fishing_bot.py
   ```
   
   **OU clique duas vezes em:**
   ```
   start_bot.bat
   ```

3. **Pressione F6** para iniciar

4. **Observe:**
   ```
   [1/5] Equipando vara de pescar...
   [2/5] Lançando isca...
   [3/5] Aguardando minigame...
   [!] MINIGAME INICIADO!
   [4/5] Jogando minigame...
   [✓] Minigame completo! (142 movimentos)
   [5/5] Verificando resultado...
   [✓✓✓] SUCESSO! Coletando peixe...
   [SUCCESS] Peixe #1 capturado!
   ```

## 🎮 Controles Durante Execução

| Tecla | Ação |
|-------|------|
| **F6** | Iniciar/Pausar bot |
| **ESC** | Parar completamente |
| **Mouse no canto ↖** | Failsafe (emergência) |

## 🐛 Problemas Comuns

### "Bot não detecta o minigame"
✅ **Solução:** Recalibre a região (calibrate.py → opção 1)

### "Mouse não se move"
✅ **Solução:** Execute como Administrador

### "Não detecta o círculo branco"
✅ **Solução:** Ajuste as cores no config.py:
```python
WHITE_CIRCLE_LOWER = [0, 0, 150]
WHITE_CIRCLE_UPPER = [180, 80, 255]
```

### "Bot muito lento/rápido"
✅ **Solução:** Edite fishing_bot.py linha 106:
```python
pyautogui.moveTo(screen_x, screen_y, duration=0.05)  # Mais rápido
pyautogui.moveTo(screen_x, screen_y, duration=0.15)  # Mais lento
```

## 📊 Estrutura de Arquivos

```
FishingScript/
├── fishing_bot.py          ← Script principal
├── vision.py               ← Detecção visual
├── config.py              ← Configurações (EDITE AQUI!)
├── calibrate.py           ← Ferramenta de calibração
├── requirements.txt       ← Dependências
├── setup.bat             ← Instalação rápida
├── start_bot.bat         ← Iniciar bot
├── README.md            ← Manual completo
├── PRODIGY_RP_SETUP.md  ← Config do Prodigy
└── QUICK_START.md       ← Este arquivo
```

## ✅ Checklist Antes de Usar

- [ ] Python instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Região do minigame calibrada
- [ ] Personagem no local de pesca
- [ ] Vara no slot 1 do inventário
- [ ] Jogo em modo janela (recomendado)
- [ ] Executando como Administrador

## 🎯 Resultado Esperado

O bot deve:
1. ✅ Equipar vara automaticamente
2. ✅ Lançar isca
3. ✅ Detectar quando minigame inicia
4. ✅ Seguir o círculo branco com precisão
5. ✅ Coletar peixe automaticamente
6. ✅ Repetir o ciclo indefinidamente

**Taxa de sucesso esperada:** 70-90% (depende da calibração)

## 📞 Ainda com Problemas?

1. Leia o [README.md](README.md) completo
2. Leia o guia [PRODIGY_RP_SETUP.md](PRODIGY_RP_SETUP.md)
3. Use `calibrate.py` para ajustar as detecções
4. Verifique se está executando como Administrador

---

**Boa pesca! 🎣**

*Lembre-se: Use com moderação e por sua conta e risco!*
