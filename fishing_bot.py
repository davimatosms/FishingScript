"""
Bot de Pesca Automatizado para GTA RP
AVISO: Use por sua conta e risco. Pode violar termos de serviço.
"""
import pyautogui
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
        print("Pressione F6 para iniciar/pausar")
        print("Pressione ESC para parar completamente")
        
    def start(self):
        """Inicia o bot"""
        keyboard.add_hotkey('f6', self.toggle_bot)
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
        keyboard.press_and_release(self.config.FISHING_ROD_KEY)
        time.sleep(2)  # Aguardar animação
        
    def cast_line(self):
        """Joga a isca na água (tecla E)"""
        print("[2/5] Lançando isca...")
        keyboard.press_and_release(self.config.CAST_KEY)
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
        """Executa o minigame de seguir o círculo branco"""
        print("[4/5] Jogando minigame...")
        start_time = time.time()
        movements = 0
        
        while (time.time() - start_time) < self.config.MINIGAME_DURATION and self.running:
            # Captura a região do minigame
            screenshot = self.screen_capture.capture_region(
                self.config.MINIGAME_REGION
            )
            
            # Encontra a posição do círculo branco
            target_pos = self.fish_detector.find_white_circle_position(screenshot)
            
            if target_pos:
                # Ajustar para coordenadas absolutas da tela
                x, y = target_pos
                screen_x = self.config.MINIGAME_REGION[0] + x
                screen_y = self.config.MINIGAME_REGION[1] + y
                
                # Mover o mouse suavemente
                pyautogui.moveTo(screen_x, screen_y, duration=0.08)
                movements += 1
            
            time.sleep(0.05)  # 50ms entre checks
        
        print(f"[✓] Minigame completo! ({movements} movimentos)")
        time.sleep(1.5)
        
    def check_result(self):
        """Verifica se a pesca foi bem-sucedida ou se o peixe escapou"""
        print("[5/5] Verificando resultado...")
        time.sleep(1)  # Aguardar mensagem aparecer
        
        # Verificar sucesso
        if self.fish_detector.detect_success():
            print("[✓✓✓] SUCESSO! Coletando peixe...")
            keyboard.press_and_release(self.config.COLLECT_KEY)
            time.sleep(2)
            self.fish_caught += 1
            return True
        
        # Verificar falha
        if self.fish_detector.detect_failure():
            print("[X] Peixe escapou!")
            return False
        
        # Se não detectou nada, assumir sucesso por segurança
        print("[?] Resultado incerto, assumindo sucesso...")
        keyboard.press_and_release(self.config.COLLECT_KEY)
        time.sleep(2)
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
                
                # Passo 5: Verificar resultado
                if self.check_result():
                    print(f"\n[SUCCESS] Peixe #{self.fish_caught} capturado!")
                else:
                    print(f"\n[FAIL] Tentativa falhou, reiniciando...")
                
                print("-" * 40)
                
                # Pequeno delay entre ciclos
                time.sleep(self.config.CYCLE_DELAY)
                
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
