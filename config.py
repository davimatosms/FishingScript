"""
Arquivo de Configuração
AJUSTE ESTES VALORES PARA O SEU SERVIDOR
"""

class Config:
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
    
    # Duração do minigame (segundos)
    MINIGAME_DURATION = 15
    
    # Delay entre ciclos de pesca (segundos)
    CYCLE_DELAY = 2
    
    # ===== REGIÕES DA TELA =====
    # Região do minigame circular (centro-direita da tela)
    # Formato: (x, y, largura, altura) para 1920x1080
    MINIGAME_REGION = (750, 250, 350, 350)  # Ajuste conforme necessário
    
    # Região da notificação azul (canto superior direito)
    NOTIFICATION_REGION = (1100, 40, 250, 100)
    
    # ===== DETECÇÃO VISUAL =====
    # Cores para detectar (em HSV)
    
    # Cor da notificação azul (ciano)
    NOTIFICATION_COLOR_LOWER = [85, 100, 100]
    NOTIFICATION_COLOR_UPPER = [100, 255, 255]
    
    # Cor do círculo branco no minigame (alvo onde o mouse deve ficar)
    WHITE_CIRCLE_LOWER = [0, 0, 180]
    WHITE_CIRCLE_UPPER = [180, 50, 255]
    
    # Cor do círculo azul do minigame
    BLUE_CIRCLE_LOWER = [90, 80, 80]
    BLUE_CIRCLE_UPPER = [110, 255, 200]
    
    # ===== SENSIBILIDADE =====
    # Velocidade do mouse ao seguir o peixe
    MOUSE_SPEED = 0.1  # Segundos (menor = mais rápido)
    
    # Threshold para detecção de pixel (ajuste se tiver falsos positivos)
    DETECTION_THRESHOLD = 1000
