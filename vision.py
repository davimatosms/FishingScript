"""
Módulo de Visão Computacional para detecção de elementos na tela
"""
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

class ScreenCapture:
    """Captura de tela otimizada"""
    
    def __init__(self):
        self.screen_size = pyautogui.size()
        
    def capture(self):
        """Captura a tela completa"""
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def capture_region(self, region):
        """
        Captura uma região específica da tela
        region: (x, y, width, height)
        """
        x, y, width, height = region
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


class FishDetector:
    """Detecta elementos relacionados à pesca na tela"""
    
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.last_notification_check = 0
        
    def detect_minigame_started(self):
        """
        Detecta se o minigame começou (círculo azul apareceu)
        """
        from config import Config
        config = Config()
        
        screenshot = self.screen_capture.capture_region(config.MINIGAME_REGION)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Detectar círculo azul do minigame
        lower = np.array(config.BLUE_CIRCLE_LOWER)
        upper = np.array(config.BLUE_CIRCLE_UPPER)
        mask = cv2.inRange(hsv, lower, upper)
        
        # Se houver pixels azuis suficientes, o minigame começou
        blue_pixels = np.sum(mask > 0)
        return blue_pixels > 5000  # Threshold ajustável
    
    def detect_notification(self, text_keywords=None):
        """
        Detecta notificação azul no canto superior direito
        text_keywords: lista de palavras para procurar (ex: ['Esperando', 'escapou'])
        """
        from config import Config
        config = Config()
        
        screenshot = self.screen_capture.capture_region(config.NOTIFICATION_REGION)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Detectar cor azul ciano da notificação
        lower = np.array(config.NOTIFICATION_COLOR_LOWER)
        upper = np.array(config.NOTIFICATION_COLOR_UPPER)
        mask = cv2.inRange(hsv, lower, upper)
        
        cyan_pixels = np.sum(mask > 0)
        return cyan_pixels > 500  # Se houver notificação azul
    
    def find_white_circle_position(self, screenshot):
        """
        Encontra a posição do círculo branco no minigame (alvo)
        Retorna (x, y) ou None
        """
        from config import Config
        config = Config()
        
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Detectar círculo branco
        lower = np.array(config.WHITE_CIRCLE_LOWER)
        upper = np.array(config.WHITE_CIRCLE_UPPER)
        mask = cv2.inRange(hsv, lower, upper)
        
        # Aplicar blur para reduzir ruído
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        # Encontrar círculos usando HoughCircles
        circles = cv2.HoughCircles(
            mask, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=50,
            param1=50, 
            param2=15,
            minRadius=10, 
            maxRadius=50
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            # Retornar o centro do primeiro círculo encontrado
            x, y, r = circles[0][0]
            return (int(x), int(y))
        
        # Fallback: usar contornos se não encontrar círculos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Filtrar contornos muito pequenos
            valid_contours = [c for c in contours if cv2.contourArea(c) > 100]
            
            if valid_contours:
                # Pegar o maior contorno
                largest = max(valid_contours, key=cv2.contourArea)
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)
        
        return None
    
    def detect_success(self):
        """
        Detecta se a pesca foi bem-sucedida
        Procura pelo texto 'FICAR COM O PEIXE' na parte inferior
        """
        screenshot = self.screen_capture.capture()
        
        # Região inferior da tela onde aparecem as opções
        height, width = screenshot.shape[:2]
        roi = screenshot[int(height*0.8):height, int(width*0.3):int(width*0.7)]
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Aumentar contraste
        gray = cv2.equalizeHist(gray)
        
        # Thresholding para destacar texto branco
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Verificar se há muito texto branco (indica mensagem)
        white_pixels = np.sum(thresh == 255)
        return white_pixels > 1000
    
    def detect_failure(self):
        """
        Detecta se o peixe escapou
        Procura por notificação azul no canto superior direito
        """
        return self.detect_notification()
    
    def calibrate_minigame_detection(self):
        """
        Função auxiliar para calibrar a detecção do minigame
        """
        print("Calibrando detecção do minigame...")
        print("Pressione ESPAÇO quando o minigame começar")
        
        import keyboard
        keyboard.wait('space')
        
        screenshot = self.screen_capture.capture()
        cv2.imwrite('minigame_started.png', screenshot)
        print("Screenshot salvo como 'minigame_started.png'")
        
    def calibrate_white_circle_tracking(self):
        """
        Função auxiliar para calibrar o rastreamento do círculo branco
        """
        print("Calibrando rastreamento do círculo branco...")
        print("Durante o minigame, pressione ESPAÇO")
        
        import keyboard
        from config import Config
        
        config = Config()
        keyboard.wait('space')
        
        screenshot = self.screen_capture.capture_region(config.MINIGAME_REGION)
        cv2.imwrite('white_circle.png', screenshot)
        print("Screenshot salvo como 'white_circle.png'")
        print("Analise para verificar a detecção do círculo branco")
        

class ColorDetector:
    """Utilitário para detectar cores específicas"""
    
    @staticmethod
    def find_color_range(image, color_bgr, tolerance=30):
        """
        Encontra a faixa HSV para uma cor BGR específica
        """
        # Converter BGR para HSV
        color_rgb = cv2.cvtColor(np.uint8([[color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        
        lower = np.array([max(0, color_rgb[0] - tolerance), 100, 100])
        upper = np.array([min(180, color_rgb[0] + tolerance), 255, 255])
        
        return lower, upper
    
    @staticmethod
    def detect_text_on_screen(screenshot, text):
        """
        Detecta texto na tela usando OCR (requer pytesseract)
        """
        try:
            import pytesseract
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            detected_text = pytesseract.image_to_string(gray)
            return text.lower() in detected_text.lower()
        except ImportError:
            print("pytesseract não instalado. Instale com: pip install pytesseract")
            return False
