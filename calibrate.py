"""
Script de Calibração
Use este script para configurar as regiões e cores corretas
"""
import cv2
import numpy as np
import pyautogui
import keyboard
import time
from vision import ScreenCapture

class Calibrator:
    def __init__(self):
        self.capture = ScreenCapture()
        self.selecting = False
        self.start_point = None
        self.end_point = None
        self.current_screenshot = None
        
    def select_region(self):
        """Interface interativa para selecionar região da tela"""
        print("\n=== CALIBRAÇÃO DE REGIÃO ===")
        print("Vá para o jogo e inicie o minigame de pesca!")
        print("A tela será capturada automaticamente em 5 segundos...")
        print("")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"Capturando em {i}...", end='\r', flush=True)
            time.sleep(1)
        
        print("\n✓ Capturando tela!")
        
        # Captura screenshot
        screenshot = self.capture.capture()
        self.current_screenshot = screenshot.copy()
        
        # Salvar screenshot para referência
        cv2.imwrite('screenshot_calibration.png', screenshot)
        
        print("✓ Tela capturada!")
        print("✓ Screenshot salva como 'screenshot_calibration.png'")
        print("\nAbrindo janela de seleção...")
        print("Se a janela não aparecer, ALT+TAB para encontrá-la!")
        print("\nNa janela que abrir:")
        print("1. Clique e arraste para selecionar a região circular do minigame")
        print("2. Pressione ENTER para confirmar")
        print("3. Pressione ESC para cancelar")
        
        time.sleep(1)  # Pequeno delay para dar tempo de ler
        
        # Cria janela com flags para ficar na frente
        cv2.namedWindow('Selecione a Região', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Selecione a Região', 1280, 720)
        cv2.setMouseCallback('Selecione a Região', self.mouse_callback)
        
        while True:
            display = self.current_screenshot.copy()
            
            if self.start_point and self.end_point:
                cv2.rectangle(display, self.start_point, self.end_point, (0, 255, 0), 2)
                
            cv2.imshow('Selecione a Região', display)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 13:  # Enter
                break
            elif key == 27:  # ESC
                cv2.destroyAllWindows()
                return None
                
        cv2.destroyAllWindows()
        
        if self.start_point and self.end_point:
            x1, y1 = self.start_point
            x2, y2 = self.end_point
            
            x = min(x1, x2)
            y = min(y1, y2)
            w = abs(x2 - x1)
            h = abs(y2 - y1)
            
            region = (x, y, w, h)
            print(f"\n✓ Região selecionada: {region}")
            print(f"Cole isso no config.py:")
            print(f"MINIGAME_REGION = {region}")
            
            return region
            
        return None
        
    def mouse_callback(self, event, x, y, flags, param):
        """Callback para seleção de região com mouse"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (x, y)
            self.selecting = True
            
        elif event == cv2.EVENT_MOUSEMOVE and self.selecting:
            self.end_point = (x, y)
            
        elif event == cv2.EVENT_LBUTTONUP:
            self.end_point = (x, y)
            self.selecting = False
            
    def detect_color_at_click(self):
        """Detecta a cor HSV de onde você clica"""
        print("\n=== CALIBRAÇÃO DE COR ===")
        print("Vá para o jogo com o elemento visível na tela!")
        print("A tela será capturada automaticamente em 5 segundos...")
        print("")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"Capturando em {i}...", end='\r', flush=True)
            time.sleep(1)
        
        print("\n✓ Capturando tela!")
        print("Clique no elemento que quer detectar (peixe, círculo branco, etc)")
        
        screenshot = self.capture.capture()
        hsv_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        def click_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                # Pegar cor BGR e HSV
                bgr = screenshot[y, x]
                hsv = hsv_screenshot[y, x]
                
                print(f"\n✓ Cor detectada em ({x}, {y}):")
                print(f"BGR: {bgr}")
                print(f"HSV: {hsv}")
                
                # Calcular range com tolerância
                tolerance = 20
                lower = np.array([max(0, hsv[0] - tolerance), 100, 100])
                upper = np.array([min(180, hsv[0] + tolerance), 255, 255])
                
                print(f"\nUse estes valores no config.py:")
                print(f"COLOR_LOWER = {lower.tolist()}")
                print(f"COLOR_UPPER = {upper.tolist()}")
                
        cv2.namedWindow('Clique na Cor')
        cv2.setMouseCallback('Clique na Cor', click_callback)
        
        while True:
            cv2.imshow('Clique na Cor', screenshot)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                break
                
        cv2.destroyAllWindows()
        
    def test_detection(self):
        """Testa a detecção em tempo real"""
        print("\n=== TESTE DE DETECÇÃO ===")
        print("Mostrando detecção em tempo real")
        print("Pressione ESC para sair")
        
        from config import Config
        from vision import FishDetector
        
        config = Config()
        detector = FishDetector()
        
        while True:
            screenshot = self.capture.capture_region(config.MINIGAME_REGION)
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Detectar borda branca do círculo (único diferencial do peixe alvo)
            lower = np.array(config.TARGET_CIRCLE_LOWER)
            upper = np.array(config.TARGET_CIRCLE_UPPER)
            
            mask = cv2.inRange(hsv, lower, upper)
            result = cv2.bitwise_and(screenshot, screenshot, mask=mask)
            
            # Encontrar posição do centro do círculo (borda branca)
            pos = detector.find_white_circle_position(screenshot)
            
            # Desenhar marcador se encontrou
            display = screenshot.copy()
            if pos:
                cv2.circle(display, pos, 10, (0, 255, 0), 2)
                cv2.putText(display, f"CIRCULO X:{pos[0]} Y:{pos[1]}", (pos[0]+15, pos[1]), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    
            cv2.imshow('Original', display)
            cv2.imshow('Mascara', mask)
            cv2.imshow('Resultado', result)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
                
        cv2.destroyAllWindows()
        
    def get_screen_coordinates(self):
        """Mostra as coordenadas do mouse em tempo real"""
        print("\n=== COORDENADAS DO MOUSE (MÉTODO MANUAL) ===")
        print("\nVá para o jogo e posicione o mouse nos cantos do círculo do minigame:")
        print("1. Canto SUPERIOR ESQUERDO do círculo")
        print("2. Canto INFERIOR DIREITO do círculo")
        print("\nAnote as coordenadas X e Y de cada posição")
        print("\nPressione CTRL+C para sair quando terminar\n")
        print("-" * 50)
        
        try:
            while True:
                x, y = pyautogui.position()
                print(f"\rPosição: X={x:4d} Y={y:4d}    ", end='', flush=True)
                
                if keyboard.is_pressed('esc'):
                    break
                    
        except KeyboardInterrupt:
            pass
            
        print("\n\n" + "="*50)
        print("COMO CALCULAR A REGIÃO:")
        print("="*50)
        print("\nSuponha que você anotou:")
        print("  Canto superior esquerdo: X=800, Y=300")
        print("  Canto inferior direito:  X=1100, Y=600")
        print("\nCalcule:")
        print("  x = 800 (canto esquerdo)")
        print("  y = 300 (canto superior)")
        print("  largura = 1100 - 800 = 300")
        print("  altura = 600 - 300 = 300")
        print("\nNo config.py, use:")
        print("  MINIGAME_REGION = (800, 300, 300, 300)")
        print("="*50 + "\n")


def main():
    calibrator = Calibrator()
    
    while True:
        print("\n" + "="*50)
        print("FERRAMENTA DE CALIBRAÇÃO - BOT DE PESCA")
        print("="*50)
        print("\n1. Selecionar região do minigame (automático)")
        print("2. Detectar cor (peixe/indicador)")
        print("3. Testar detecção em tempo real")
        print("4. Ver coordenadas do mouse (método manual - RECOMENDADO se opção 1 falhar)")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == '1':
            calibrator.select_region()
        elif choice == '2':
            calibrator.detect_color_at_click()
        elif choice == '3':
            calibrator.test_detection()
        elif choice == '4':
            calibrator.get_screen_coordinates()
        elif choice == '5':
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
