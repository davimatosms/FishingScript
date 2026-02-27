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
    MINIGAME_REGION = (1207, 401, 284, 279)  # Calibrado manualmente
    
    # Região da notificação azul (canto superior direito)
    NOTIFICATION_REGION = (1100, 40, 250, 100)
    
    # ===== DETECÇÃO VISUAL =====
    # Cores para detectar (em HSV)
    
    # Notificação azul (ciano) no canto superior direito
    NOTIFICATION_COLOR_LOWER = [85, 100, 100]
    NOTIFICATION_COLOR_UPPER = [100, 255, 255]
    
    # BORDA CLARA do círculo dentro do peixe alvo
    # Detecta cinza claro azulado: HSV[105,46,112] vs peixe preto HSV[104,234,12]
    TARGET_CIRCLE_LOWER = [90, 0, 70]      # H=90-120 azulado amplo, S=0-120, V>70
    TARGET_CIRCLE_UPPER = [120, 120, 220]  # Faixa mais ampla para detecção estável
    
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
