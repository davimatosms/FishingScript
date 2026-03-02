"""
Bot de Pesca Automatizado para GTA RP
AVISO: Use por sua conta e risco. Pode violar termos de serviço.
"""
import pyautogui
import pydirectinput
import time
import keyboard
import cv2
import numpy as np
from vision import ScreenCapture, FishDetector
from config import Config

class FishingBot:
    def __init__(self):
        self.config = Config()
        self.screen_capture = ScreenCapture()
        self.fish_detector = FishDetector()
        self.running = False
        self.fish_caught = 0
        
        # Configurações de segurança
        pyautogui.FAILSAFE = True  # Move o mouse para o canto superior esquerdo para parar
        pyautogui.PAUSE = 0.1
        
        print("Bot de Pesca Inicializado!")
        print(f"Resolução do jogo: {self.config.GAME_WIDTH}x{self.config.GAME_HEIGHT} (janela)")
        print(f"Procurando janela: '{self.config.GAME_WINDOW_TITLE}'")
        
        # Verificar se encontra a janela do jogo
        from vision import find_game_window
        window = find_game_window(self.config.GAME_WINDOW_TITLE)
        if window:
            _, wx, wy, ww, wh = window
            print(f"[OK] Janela encontrada em ({wx}, {wy}) - {ww}x{wh}")
        else:
            print(f"[!] Janela '{self.config.GAME_WINDOW_TITLE}' NÃO encontrada!")
            print("[!] Certifique-se de que o jogo está aberto antes de iniciar.")
        
        print("\nPressione J para iniciar/pausar")
        print("Pressione ESC para parar completamente")
        
    def start(self):
        """Inicia o bot"""
        keyboard.add_hotkey('j', self.toggle_bot)
        keyboard.add_hotkey('esc', self.stop_bot)
        
        print("\n[INFO] Bot pronto! Aguardando comando...")
        print("[INFO] Posicione-se próximo ao local de pesca")
        
        keyboard.wait('esc')
        
    def toggle_bot(self):
        """Liga/desliga o bot"""
        self.running = not self.running
        if self.running:
            print("\n[✓] Bot ATIVADO")
            self.run_fishing_cycle()
        else:
            print("\n[X] Bot PAUSADO")
            
    def stop_bot(self):
        """Para o bot completamente"""
        self.running = False
        print(f"\n[INFO] Bot encerrado. Peixes capturados: {self.fish_caught}")
        
    def equip_fishing_rod(self):
        """Equipa a vara de pescar (tecla 1)"""
        print("[1/5] Equipando vara de pescar...")
        pydirectinput.press(self.config.FISHING_ROD_KEY)
        time.sleep(2)  # Aguardar animação
        
    def cast_line(self):
        """Joga a isca na água (tecla E)"""
        print("[2/5] Lançando isca...")
        pydirectinput.press(self.config.CAST_KEY)
        time.sleep(2)
        
    def wait_for_minigame(self):
        """Aguarda o minigame começar"""
        print("[3/5] Aguardando minigame...")
        timeout = time.time() + self.config.BITE_TIMEOUT
        
        while time.time() < timeout and self.running:
            # Detectar se o minigame começou (círculo azul apareceu)
            if self.fish_detector.detect_minigame_started():
                print("[!] MINIGAME INICIADO!")
                time.sleep(0.5)  # Pequeno delay para estabilizar
                return True
            
            time.sleep(0.2)
        
        print("[TIMEOUT] Minigame não iniciou, tentando novamente...")
        return False
        
    def play_minigame(self):
        """Executa o minigame de seguir o peixe"""
        print("[4/5] Jogando minigame...")
        start_time = time.time()
        movements  = 0
        no_detect  = 0

        while (time.time() - start_time) < self.config.MINIGAME_DURATION and self.running:
            # Captura a região do minigame
            screenshot = self.screen_capture.capture_region(
                self.config.MINIGAME_REGION
            )

            # Encontra a posição do peixe (blob escuro)
            target_pos = self.fish_detector.find_white_circle_position(screenshot)

            if target_pos:
                no_detect = 0
                # Ajustar para coordenadas absolutas da tela
                # (região é relativa à janela, + offset da janela na tela)
                offset_x, offset_y = self.screen_capture.get_game_offset()
                x, y = target_pos
                screen_x = offset_x + self.config.MINIGAME_REGION[0] + x
                screen_y = offset_y + self.config.MINIGAME_REGION[1] + y

                # Mover o mouse suavemente
                pyautogui.moveTo(screen_x, screen_y, duration=0.08)
                movements += 1

                # Log a cada 20 movimentos
                if movements % 20 == 1:
                    elapsed = time.time() - start_time
                    print(f"  [PEIXE] pos=({x},{y}) tela=({screen_x},{screen_y}) mov={movements} t={elapsed:.1f}s")
            else:
                no_detect += 1
                # Aviso a cada 2 segundos sem detecção (40 frames × 0.05s)
                if no_detect % 40 == 1:
                    elapsed = time.time() - start_time
                    print(f"  [!] Peixe NÃO detectado — verifique cores no config.py (t={elapsed:.1f}s)")

            time.sleep(0.05)  # 50ms entre checks

        print(f"[✓] Minigame completo! ({movements} movimentos, sem detecção: {no_detect}x)")
        
    def collect_fish(self):
        """Coleta o peixe após o minigame - aperta E múltiplas vezes para garantir"""
        print(f"[5/5] Aguardando {self.config.COLLECT_DELAY}s para coletar o peixe...")
        time.sleep(self.config.COLLECT_DELAY)
        
        print(f"[5/5] Coletando peixe (apertando E x{self.config.COLLECT_PRESSES})...")
        for i in range(self.config.COLLECT_PRESSES):
            pydirectinput.press(self.config.COLLECT_KEY)
            time.sleep(self.config.COLLECT_PRESS_INTERVAL)
        
        self.fish_caught += 1
        print(f"[✓✓✓] Peixe #{self.fish_caught} coletado!")
        
        # Cooldown pós-coleta antes de iniciar novo ciclo
        print(f"[...] Aguardando {self.config.CYCLE_DELAY}s antes do próximo ciclo...")
        time.sleep(self.config.CYCLE_DELAY)
        return True
    
    def run_fishing_cycle(self):
        """Executa um ciclo completo de pesca"""
        while self.running:
            try:
                # Passo 1: Equipar vara
                self.equip_fishing_rod()
                
                # Passo 2: Lançar isca
                self.cast_line()
                
                # Passo 3: Aguardar minigame iniciar
                if not self.wait_for_minigame():
                    continue
                
                # Passo 4: Jogar minigame
                self.play_minigame()
                
                # Passo 5: Coletar o peixe
                self.collect_fish()
                
                print("-" * 40)
                
            except Exception as e:
                print(f"[ERRO] {str(e)}")
                time.sleep(2)
                

if __name__ == "__main__":
    print("=" * 50)
    print("     BOT DE PESCA AUTOMATIZADO - GTA RP")
    print("=" * 50)
    print("\n⚠️  AVISO: Usar bots pode resultar em banimento!")
    print("Use por sua conta e risco.\n")
    
    bot = FishingBot()
    bot.start()
