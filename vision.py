"""
Módulo de Visão Computacional para detecção de elementos na tela
Suporte a modo janela: detecta a janela do jogo e usa coordenadas relativas
"""
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import win32gui
import win32con


def find_game_window(title_keyword="FiveM"):
    """
    Encontra a janela do jogo pelo título.
    Retorna (hwnd, x, y, width, height) ou None.
    """
    result = []
    
    def enum_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if title_keyword.lower() in window_title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                x, y, x2, y2 = rect
                # Ajustar para a área cliente (sem bordas/titlebar)
                try:
                    client_rect = win32gui.GetClientRect(hwnd)
                    import win32api
                    import ctypes
                    
                    # Converter coordenadas do cliente para coordenadas de tela
                    class POINT(ctypes.Structure):
                        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
                    
                    pt = POINT(0, 0)
                    ctypes.windll.user32.ClientToScreen(hwnd, ctypes.byref(pt))
                    
                    client_w = client_rect[2] - client_rect[0]
                    client_h = client_rect[3] - client_rect[1]
                    
                    result.append((hwnd, pt.x, pt.y, client_w, client_h))
                except:
                    # Fallback: usar rect completo
                    w = x2 - x
                    h = y2 - y
                    result.append((hwnd, x, y, w, h))
    
    win32gui.EnumWindows(enum_callback, None)
    
    if result:
        # Retornar a maior janela encontrada (provavelmente a principal)
        result.sort(key=lambda r: r[3] * r[4], reverse=True)
        return result[0]
    return None


class ScreenCapture:
    """Captura de tela otimizada com suporte a modo janela"""
    
    def __init__(self):
        self.screen_size = pyautogui.size()
        self._game_window = None  # Cache da posição da janela
        self._last_window_check = 0
        
    def _get_game_window(self):
        """Obtém a posição da janela do jogo (com cache de 1 segundo)"""
        import time
        now = time.time()
        if self._game_window is None or (now - self._last_window_check) > 1.0:
            from config import Config
            config = Config()
            self._game_window = find_game_window(config.GAME_WINDOW_TITLE)
            self._last_window_check = now
        return self._game_window
    
    def get_game_offset(self):
        """Retorna (offset_x, offset_y) da janela do jogo na tela"""
        window = self._get_game_window()
        if window:
            _, x, y, w, h = window
            return (x, y)
        # Fallback: sem offset (tela cheia)
        return (0, 0)
        
    def capture(self):
        """Captura a tela completa"""
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def capture_game_window(self):
        """Captura apenas a janela do jogo"""
        window = self._get_game_window()
        if window:
            _, x, y, w, h = window
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # Fallback: captura tela inteira
        return self.capture()
    
    def capture_region(self, region):
        """
        Captura uma região específica RELATIVA À JANELA DO JOGO
        region: (x, y, width, height) - coordenadas relativas ao jogo
        """
        rx, ry, width, height = region
        
        # Obter offset da janela do jogo
        offset_x, offset_y = self.get_game_offset()
        
        # Converter para coordenadas absolutas da tela
        abs_x = offset_x + rx
        abs_y = offset_y + ry
        
        screenshot = ImageGrab.grab(bbox=(abs_x, abs_y, abs_x + width, abs_y + height))
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


class FishDetector:
    """Detecta elementos relacionados à pesca na tela"""
    
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.last_notification_check = 0
        self._last_fish_pos   = None  # última posição conhecida do peixe
        self._frames_lost     = 0     # frames consecutivos sem detecção
        
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
    
    def _detect_blob(self, hsv, lower, upper, min_area):
        """Tenta detectar o maior blob dentro de um range HSV. Retorna (cx,cy) ou None."""
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        # Morfologia 7x7: fecha buracos maiores no blob do peixe
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < min_area:
            return None

        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None

        return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    def find_white_circle_position(self, screenshot):
        """
        Encontra a posição do PEIXE (blob escuro) dentro do minigame.
        Estratégia:
          1. Tenta com range estrito (calibrado)
          2. Se falhar, tenta com range relaxado
          3. Se ambos falharem, reutiliza a última posição conhecida
             por até FISH_LOST_FRAMES frames (evita tremida do mouse)
        Retorna (x, y) ou None.
        """
        from config import Config
        config = Config()

        hsv      = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        min_area = getattr(config, 'FISH_MIN_AREA', 30)

        # Passo 1 — range estrito
        pos = self._detect_blob(hsv,
                                config.TARGET_CIRCLE_LOWER,
                                config.TARGET_CIRCLE_UPPER,
                                min_area)

        # Passo 2 — range relaxado (fallback de cor)
        if pos is None and hasattr(config, 'TARGET_CIRCLE_LOWER2'):
            pos = self._detect_blob(hsv,
                                    config.TARGET_CIRCLE_LOWER2,
                                    config.TARGET_CIRCLE_UPPER2,
                                    min_area)

        if pos is not None:
            # Detecção OK — atualizar estado
            self._last_fish_pos = pos
            self._frames_lost   = 0
            return pos

        # Passo 3 — usar última posição conhecida por até FISH_LOST_FRAMES frames
        max_lost = getattr(config, 'FISH_LOST_FRAMES', 8)
        if self._last_fish_pos is not None and self._frames_lost < max_lost:
            self._frames_lost += 1
            return self._last_fish_pos

        # Peixe realmente perdido
        self._last_fish_pos = None
        self._frames_lost   = 0
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
        Função auxiliar para calibrar o rastreamento da borda branca
        """
        print("Calibrando rastreamento da borda branca do círculo...")
        print("Durante o minigame, pressione ESPAÇO")
        
        import keyboard
        from config import Config
        
        config = Config()
        keyboard.wait('space')
        
        screenshot = self.screen_capture.capture_region(config.MINIGAME_REGION)
        cv2.imwrite('white_border.png', screenshot)
        print("Screenshot salvo como 'white_border.png'")
        print("Analise para verificar a detecção da borda branca")
        

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
