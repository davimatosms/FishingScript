"""
Ferramenta de debug visual - mostra EXATAMENTE o que o bot está enxergando
Use para calibrar cores e regiões corretamente
"""
import cv2
import numpy as np
import time
import sys
from vision import ScreenCapture, find_game_window
from config import Config

# ── Estado global para o clique de cor ──────────────────────────────────────
g_clicked_pos = None
g_sampled_hsv = None
g_screenshot  = None

def mouse_callback(event, x, y, flags, param):
    global g_clicked_pos, g_sampled_hsv
    if event == cv2.EVENT_LBUTTONDOWN and g_screenshot is not None:
        h, w = g_screenshot.shape[:2]
        if 0 <= x < w and 0 <= y < h:
            g_clicked_pos = (x, y)
            hsv_img = cv2.cvtColor(g_screenshot, cv2.COLOR_BGR2HSV)
            g_sampled_hsv = hsv_img[y, x]
            bgr = g_screenshot[y, x]
            print(f"\n[CLIQUE] Pixel ({x},{y})")
            print(f"  BGR = {bgr}")
            print(f"  HSV = {g_sampled_hsv}  →  H={g_sampled_hsv[0]}, S={g_sampled_hsv[1]}, V={g_sampled_hsv[2]}")
            tol = 15
            lower = [max(0,   int(g_sampled_hsv[0]) - tol), max(0,   int(g_sampled_hsv[1]) - 40), max(0,   int(g_sampled_hsv[2]) - 40)]
            upper = [min(179, int(g_sampled_hsv[0]) + tol), min(255, int(g_sampled_hsv[1]) + 40), min(255, int(g_sampled_hsv[2]) + 40)]
            print(f"\n  Cole no config.py:")
            print(f"  TARGET_CIRCLE_LOWER = {lower}")
            print(f"  TARGET_CIRCLE_UPPER = {upper}")


def build_mask(screenshot, lower, upper):
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return mask


def find_target(mask, config):
    """Encontra o peixe pelo maior blob na máscara (mesmo algoritmo do vision.py)"""
    # Morfologia: fecha buracos no blob
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, 0, ""

    largest = max(contours, key=cv2.contourArea)
    area    = cv2.contourArea(largest)

    if area < 30:
        return None, 0, f"blob muito pequeno ({area:.0f}px)"

    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None, 0, ""

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    _, radius = cv2.minEnclosingCircle(largest)
    return (cx, cy), int(radius), f"Blob {area:.0f}px²"


def mode_live():
    """Modo 1: Preview ao vivo do que o bot está enxergando"""
    global g_screenshot

    config   = Config()
    capture  = ScreenCapture()

    print("\n[MODO AO VIVO] Vizualizando região do minigame em tempo real")
    print("  Clique em qualquer pixel para amostrar a cor")
    print("  Pressione ESC para voltar ao menu\n")

    cv2.namedWindow("Original (Região Minigame)", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Máscara HSV (TARGET)",       cv2.WINDOW_NORMAL)
    cv2.namedWindow("Detecção Final",             cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Original (Região Minigame)", mouse_callback)

    while True:
        screenshot = capture.capture_region(config.MINIGAME_REGION)
        g_screenshot = screenshot.copy()

        lower = config.TARGET_CIRCLE_LOWER
        upper = config.TARGET_CIRCLE_UPPER
        mask  = build_mask(screenshot, lower, upper)

        # Monta overlay de detecção
        display = screenshot.copy()
        pos, radius, method = find_target(mask, config)
        if pos:
            cv2.circle(display, pos, max(radius, 10), (0, 255, 0), 2)
            cv2.circle(display, pos, 3, (0, 255, 0), -1)
            cv2.putText(display, f"{method} ({pos[0]},{pos[1]})",
                        (pos[0] + 12, pos[1] - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
        else:
            cv2.putText(display, "NADA DETECTADO", (5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

        # Mostrar ponto clicado
        if g_clicked_pos:
            cv2.circle(display, g_clicked_pos, 5, (255, 0, 255), -1)
            cv2.circle(display, g_clicked_pos, 15, (255, 0, 255), 1)

        # Máscara colorida: pixels detectados em verde sobre cinza
        mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Pixel count
        n_px = int(np.sum(mask > 0))
        cv2.putText(mask_color, f"Pixels: {n_px}", (5, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)

        cv2.imshow("Original (Região Minigame)", display)
        cv2.imshow("Máscara HSV (TARGET)",       mask_color)
        cv2.imshow("Detecção Final",             display)

        k = cv2.waitKey(50) & 0xFF
        if k == 27:   # ESC
            break

    cv2.destroyAllWindows()


def mode_full_region():
    """Modo 2: Captura a janela completa do jogo para verificar MINIGAME_REGION"""
    global g_screenshot

    config  = Config()
    capture = ScreenCapture()

    print("\n[MODO JANELA COMPLETA] Mostrando onde está o MINIGAME_REGION")
    print("  Clique em qualquer ponto para obter coordenadas relativas à janela")
    print("  Pressione ESC para voltar ao menu\n")

    def full_mouse_cb(event, x, y, flags, param):
        global g_clicked_pos, g_sampled_hsv
        if event == cv2.EVENT_LBUTTONDOWN and g_screenshot is not None:
            g_clicked_pos = (x, y)
            hsv_img = cv2.cvtColor(g_screenshot, cv2.COLOR_BGR2HSV)
            g_sampled_hsv = hsv_img[y, x]
            bgr = g_screenshot[y, x]
            print(f"\n[CLIQUE] Posição relativa à janela: ({x}, {y})")
            print(f"  BGR = {bgr}")
            print(f"  HSV = {g_sampled_hsv}")

    cv2.namedWindow("Janela do Jogo Completa", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Janela do Jogo Completa", 1280, 720)
    cv2.setMouseCallback("Janela do Jogo Completa", full_mouse_cb)

    while True:
        screenshot = capture.capture_game_window()
        g_screenshot = screenshot.copy()
        display = screenshot.copy()

        # Desenhar MINIGAME_REGION em verde
        rx, ry, rw, rh = config.MINIGAME_REGION
        cv2.rectangle(display, (rx, ry), (rx + rw, ry + rh), (0, 255, 0), 2)
        cv2.putText(display, "MINIGAME_REGION", (rx, ry - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Desenhar NOTIFICATION_REGION em amarelo
        nx, ny, nw, nh = config.NOTIFICATION_REGION
        cv2.rectangle(display, (nx, ny), (nx + nw, ny + nh), (0, 255, 255), 2)
        cv2.putText(display, "NOTIF_REGION", (nx, ny - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        if g_clicked_pos:
            cv2.circle(display, g_clicked_pos, 5, (255, 0, 255), -1)
            cv2.putText(display, f"({g_clicked_pos[0]},{g_clicked_pos[1]})",
                        (g_clicked_pos[0] + 8, g_clicked_pos[1] - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        cv2.imshow("Janela do Jogo Completa", display)

        k = cv2.waitKey(100) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


def mode_screenshot_and_analyze():
    """Modo 3: Tira screenshot e abre para análise (conta-régressiva)"""
    global g_screenshot

    config  = Config()
    capture = ScreenCapture()

    print("\n[MODO SCREENSHOT] Capturará a região do minigame em 5 segundos")
    print("  Abra o jogo e deixe o minigame visível!\n")

    for i in range(5, 0, -1):
        print(f"  Capturando em {i}...", end='\r', flush=True)
        time.sleep(1)

    screenshot = capture.capture_region(config.MINIGAME_REGION)
    g_screenshot = screenshot.copy()

    # Salva arquivos de análise
    cv2.imwrite("debug_raw.png", screenshot)

    lower = config.TARGET_CIRCLE_LOWER
    upper = config.TARGET_CIRCLE_UPPER
    mask  = build_mask(screenshot, lower, upper)
    cv2.imwrite("debug_mask.png", mask)

    display = screenshot.copy()
    pos, radius, method = find_target(mask, config)
    if pos:
        cv2.circle(display, pos, max(radius, 10), (0, 255, 0), 2)
        cv2.circle(display, pos, 3, (0, 255, 0), -1)
        print(f"\n[OK] Detectado via {method} em {pos}")
    else:
        print("\n[X] Nada detectado com as cores atuais do config.py")

    cv2.imwrite("debug_detection.png", display)
    print("  Arquivos salvos: debug_raw.png | debug_mask.png | debug_detection.png")

    print("\n  Clique no peixe para amostrar a cor. ESC para sair.")
    cv2.namedWindow("Screenshot - Clique no Peixe", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Screenshot - Clique no Peixe", mouse_callback)

    while True:
        disp2 = g_screenshot.copy()
        if g_clicked_pos:
            cv2.circle(disp2, g_clicked_pos, 5,  (255, 0, 255), -1)
            cv2.circle(disp2, g_clicked_pos, 15, (255, 0, 255), 1)
        cv2.imshow("Screenshot - Clique no Peixe", disp2)
        k = cv2.waitKey(50) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


def mode_color_tune():
    """Modo 4: Ajuste interativo de Lower/Upper HSV com trackbars"""
    config  = Config()
    capture = ScreenCapture()

    print("\n[MODO AJUSTE DE COR] Use os sliders para tunar os valores HSV em tempo real")
    print("  Quando estiver bom, anote os valores e atualize o config.py")
    print("  Pressione ESC para sair\n")

    win = "Ajuste HSV - Lower/Upper"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win, 900, 600)

    # Criar trackbars com valores atuais do config
    lo = config.TARGET_CIRCLE_LOWER
    hi = config.TARGET_CIRCLE_UPPER

    cv2.createTrackbar("Lo H", win, lo[0], 179, lambda x: None)
    cv2.createTrackbar("Lo S", win, lo[1], 255, lambda x: None)
    cv2.createTrackbar("Lo V", win, lo[2], 255, lambda x: None)
    cv2.createTrackbar("Hi H", win, hi[0], 179, lambda x: None)
    cv2.createTrackbar("Hi S", win, hi[1], 255, lambda x: None)
    cv2.createTrackbar("Hi V", win, hi[2], 255, lambda x: None)

    while True:
        screenshot = capture.capture_region(config.MINIGAME_REGION)

        lo_h = cv2.getTrackbarPos("Lo H", win)
        lo_s = cv2.getTrackbarPos("Lo S", win)
        lo_v = cv2.getTrackbarPos("Lo V", win)
        hi_h = cv2.getTrackbarPos("Hi H", win)
        hi_s = cv2.getTrackbarPos("Hi S", win)
        hi_v = cv2.getTrackbarPos("Hi V", win)

        lower = [lo_h, lo_s, lo_v]
        upper = [hi_h, hi_s, hi_v]

        mask  = build_mask(screenshot, lower, upper)
        n_px  = int(np.sum(mask > 0))

        display = screenshot.copy()
        pos, radius, method = find_target(mask, config)
        if pos:
            cv2.circle(display, pos, max(radius, 10), (0, 255, 0), 2)
            cv2.circle(display, pos, 3, (0, 255, 0), -1)

        # Combinar lado a lado
        mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        label = f"Lower={lower}  Upper={upper}  px={n_px}"
        combined = np.hstack([display, mask_color])
        cv2.putText(combined, label, (5, combined.shape[0] - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 1)

        cv2.imshow(win, combined)

        k = cv2.waitKey(50) & 0xFF
        if k == 27:
            print(f"\n[RESULTADO FINAL]")
            print(f"  TARGET_CIRCLE_LOWER = {lower}")
            print(f"  TARGET_CIRCLE_UPPER = {upper}")
            print(f"  Cole esses valores no config.py!")
            break

    cv2.destroyAllWindows()


def main():
    print("=" * 55)
    print("   DEBUG VISUAL - BOT DE PESCA")
    print("=" * 55)

    config = Config()
    window = find_game_window(config.GAME_WINDOW_TITLE)
    if window:
        _, wx, wy, ww, wh = window
        print(f"[OK] Janela '{config.GAME_WINDOW_TITLE}' em ({wx},{wy}) {ww}x{wh}")
    else:
        print(f"[!] Janela '{config.GAME_WINDOW_TITLE}' não encontrada!")

    while True:
        print("\n" + "-" * 55)
        print("1. Preview ao vivo (região do minigame + clique na cor)")
        print("2. Ver janela completa (verificar posição das regiões)")
        print("3. Screenshot + análise (salva debug_*.png)")
        print("4. Ajuste interativo de cor HSV (sliders)")
        print("5. Sair")
        print("-" * 55)

        choice = input("Opção: ").strip()

        if choice == "1":
            mode_live()
        elif choice == "2":
            mode_full_region()
        elif choice == "3":
            mode_screenshot_and_analyze()
        elif choice == "4":
            mode_color_tune()
        elif choice == "5":
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
