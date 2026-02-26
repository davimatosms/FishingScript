# 🎣 Configuração Específica para Prodigy RP

## ✅ Configurações Já Aplicadas

Baseado nas screenshots fornecidas, o bot já está pré-configurado para o servidor Prodigy RP:

### Teclas Configuradas:
- **Tecla 1**: Equipar vara de pescar
- **Tecla E**: Lançar isca e coletar peixe

### Detecções Implementadas:
1. **Notificação azul** no canto superior direito ("Esperando um peixe...")
2. **Círculo azul** do minigame na tela
3. **Círculo branco** central que deve ser seguido
4. **Mensagem de sucesso** ("FICAR COM O PEIXE")
5. **Mensagem de falha** ("O peixe escapou!")

## 🔧 Ajustes Finos Necessários

### 1. Calibrar Região do Minigame

A região do minigame está configurada como:
```python
MINIGAME_REGION = (750, 250, 350, 350)
```

**Para verificar se está correto:**

```powershell
python calibrate.py
# Escolha opção 1: Selecionar região do minigame
# Capture a tela durante o minigame e selecione a área circular
```

### 2. Testar Detecção do Círculo Branco

```powershell
python calibrate.py
# Escolha opção 3: Testar detecção em tempo real
# Durante o minigame, veja se o círculo branco está sendo detectado
```

**Se não estiver detectando:**
- Ajuste `WHITE_CIRCLE_LOWER` e `WHITE_CIRCLE_UPPER` no config.py
- Use a opção 2 do calibrate.py para clicar no círculo branco

### 3. Ajustar Tempo do Minigame

O tempo padrão é 15 segundos. Se o minigame do Prodigy for diferente:

```python
# Em config.py
MINIGAME_DURATION = 20  # Ajuste conforme necessário
```

## 🎮 Fluxo Completo da Pesca no Prodigy RP

1. ✅ **Personagem no local** de pesca
2. ✅ **Aperta "1"** → Vara equipada
3. ✅ **Aperta "E"** → Lança isca
4. ✅ **Notificação azul** aparece ("Esperando...")
5. ✅ **Círculo azul** aparece na tela → Minigame iniciado
6. ✅ **Seguir círculo branco** com o mouse por ~15 segundos
7. ✅ **Dois resultados possíveis:**
   - ✅ Sucesso: Aparece "FICAR COM O PEIXE" → Aperta "E"
   - ❌ Falha: Aparece "O peixe escapou!" → Recomeça

## 🖥️ Requisitos de Resolução

As configurações atuais assumem resolução **1920x1080**.

**Se sua resolução for diferente:**

Ajuste as regiões no config.py:
```python
# Exemplo para 2560x1440
MINIGAME_REGION = (1000, 333, 467, 467)  # Escala proporcional
NOTIFICATION_REGION = (1467, 53, 333, 133)
```

## 🚀 Teste Rápido

1. **Instalar dependências:**
```powershell
pip install -r requirements.txt
```

2. **Posicionar personagem** no local de pesca

3. **Executar bot:**
```powershell
python fishing_bot.py
```

4. **Pressionar F6** para iniciar

5. **Observar o console:**
   - "[1/5] Equipando vara..."
   - "[2/5] Lançando isca..."
   - "[3/5] Aguardando minigame..."
   - "[!] MINIGAME INICIADO!"
   - "[4/5] Jogando minigame..."
   - "[5/5] Verificando resultado..."
   - "[SUCCESS] Peixe #1 capturado!"

## ⚠️ Troubleshooting

### Bot não detecta o minigame
**Solução:** Recalibre a região do minigame:
```powershell
python calibrate.py → Opção 1
```

### Mouse não segue o círculo branco
**Solução:** Ajuste as cores HSV:
```python
# Em config.py, tente valores mais permissivos:
WHITE_CIRCLE_LOWER = [0, 0, 150]  # Mais tolerante
WHITE_CIRCLE_UPPER = [180, 80, 255]
```

### Bot não detecta sucesso/falha
**Solução:** A detecção de texto pode falhar. O bot assume sucesso por padrão como fallback.

### Mouse muito lento/rápido
**Solução:** Ajuste a velocidade:
```python
# Em fishing_bot.py, linha do pyautogui.moveTo:
pyautogui.moveTo(screen_x, screen_y, duration=0.05)  # Mais rápido
pyautogui.moveTo(screen_x, screen_y, duration=0.15)  # Mais lento
```

## 📊 Cores Detectadas (HSV)

### Notificação Azul (Canto Superior Direito)
```python
Hue: 85-100 (Ciano)
Saturation: 100-255
Value: 100-255
```

### Círculo Branco (Alvo do Minigame)
```python
Hue: 0-180 (Qualquer matiz)
Saturation: 0-50 (Pouca saturação = branco)
Value: 180-255 (Brilhante)
```

### Círculo Azul (Fundo do Minigame)
```python
Hue: 90-110 (Azul)
Saturation: 80-255
Value: 80-200
```

## 💡 Dicas de Performance

1. **Execute como Administrador** para o bot funcionar corretamente
2. **Jogue em modo Janela** para melhor captura
3. **Desative overlays** (Discord, etc) que podem interferir
4. **Use configurações gráficas médias** para melhor detecção
5. **Evite usar à noite** (iluminação do jogo afeta detecção)

## 🔒 Segurança

- O bot tem **FAILSAFE ativado**: Mova o mouse para o canto superior esquerdo para parar imediatamente
- Use **F6** para pausar/retomar
- Use **ESC** para encerrar completamente
- Recomenda-se **não deixar rodando 24/7** para evitar detecção

## 📈 Melhorias Futuras Possíveis

- [ ] Adicionar delays aleatórios para parecer mais humano
- [ ] Sistema de anti-AFK (movimentos ocasionais)
- [ ] Contador de tempo de pesca
- [ ] Estatísticas de sucesso/falha
- [ ] Notificações sonoras ao capturar
- [ ] Parar automaticamente após X peixes

---

**Pronto para pescar! 🎣**

Se tiver problemas, use o `calibrate.py` para ajustar as configurações.
