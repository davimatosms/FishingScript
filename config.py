"""
Arquivo de Configuração
AJUSTE ESTES VALORES PARA O SEU SERVIDOR
"""

class Config:
    # ===== JANELA DO JOGO =====
    # Título da janela do jogo (usado para encontrar automaticamente)
    # Para FiveM/Prodigy RP, geralmente contém "FiveM" ou "GTA"
    GAME_WINDOW_TITLE = "FiveM"
    
    # Resolução do jogo em modo janela
    GAME_WIDTH = 1904
    GAME_HEIGHT = 1041
    
    # ===== TECLAS DO JOGO =====
    # Tecla para equipar a vara de pescar
    FISHING_ROD_KEY = '1'  # Prodigy RP
    
    # Tecla para lançar a isca
    CAST_KEY = 'e'
    
    # Tecla para pegar o peixe após sucesso
    COLLECT_KEY = 'e'
    
    # ===== TIMINGS =====
    # Tempo máximo para esperar um peixe morder (segundos)
    BITE_TIMEOUT = 30
    
    # Duração do minigame (segundos) - aumentado para suportar 3 peixes
    MINIGAME_DURATION = 25
    
    # Cooldown após minigame acabar, antes de coletar o peixe (segundos)
    COLLECT_DELAY = 3
    
    # Quantas vezes apertar E para garantir coleta do peixe
    COLLECT_PRESSES = 3
    
    # Intervalo entre cada pressionamento de E na coleta (segundos)
    COLLECT_PRESS_INTERVAL = 0.5
    
    # Delay após coletar o peixe, antes de iniciar novo ciclo (segundos)
    CYCLE_DELAY = 2
    
    # ===== REGIÕES DA TELA (RELATIVAS À JANELA DO JOGO) =====
    # Formato: (x, y, largura, altura) - coordenadas RELATIVAS à janela do jogo
    # Baseado em resolução 1904x1041
    
    # Região do minigame circular (centro-direita da tela)
    # Expandida para cobrir cor clicada em (1480,656) com folga
    MINIGAME_REGION = (1140, 360, 380, 320)
    
    # Região da notificação azul (canto superior direito)
    NOTIFICATION_REGION = (1091, 39, 248, 96)
    
    # ===== DETECÇÃO VISUAL =====
    # Cores para detectar (em HSV)
    
    # Notificação azul (ciano) no canto superior direito
    NOTIFICATION_COLOR_LOWER = [85, 100, 100]
    NOTIFICATION_COLOR_UPPER = [100, 255, 255]
    
    # COR DO PEIXE ALVO - calibrado via debug_vision
    # Azul-preto saturado: corpo escuro do peixe no minigame
    # H=91-121 (azul-esverdeado), S=154-234 (muito saturado), V=0-65 (escuro/preto)
    TARGET_CIRCLE_LOWER = [91, 154, 0]
    TARGET_CIRCLE_UPPER = [121, 234, 65]
    
    # Círculo azul do minigame (fundo)
    BLUE_CIRCLE_LOWER = [90, 80, 80]
    BLUE_CIRCLE_UPPER = [110, 255, 200]
    
    # Threshold mínimo de pixels para considerar detecção válida
    DETECTION_THRESHOLD = 5  # Bem baixo para detectar bordas finas (reduzido de 10)
    
    # ===== SENSIBILIDADE =====
    # Velocidade do mouse ao seguir o peixe
    MOUSE_SPEED = 0.1  # Segundos (menor = mais rápido)
    
    # Threshold para detecção de pixel (ajuste se tiver falsos positivos)
    DETECTION_THRESHOLD = 1000
