import cv2
import mediapipe as mp
import numpy as np
import random

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.8)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-7, -2)
        self.life = 1.0 
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.04

particles = []

def draw_mandala(size, angle):
    pad = 100
    canvas_size = size + pad
    img = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
    center = (canvas_size // 2, canvas_size // 2)
    
    orange = (20, 150, 255) 
    cyan = (255, 255, 100)
    
    # 1. Outer Fractal Rings
    cv2.circle(img, center, size // 2, orange, 3)
    cv2.circle(img, center, (size // 2) - 20, orange, 1)
    
    # 2. Main Star Logic
    pts = []
    for i in range(12):
        r = (size // 2.1) if i % 2 == 0 else (size // 3.5)
        rad = np.deg2rad(i * 30 + angle)
        pts.append([center[0] + r * np.cos(rad), center[1] + r * np.sin(rad)])
    cv2.polylines(img, [np.array(pts, np.int32)], True, cyan, 2)
    
    # 3. Inner Rotating Glyphs
    for i in range(4):
        rad = np.deg2rad(i * 90 - angle * 2)
        p1 = (int(center[0] + (size//5) * np.cos(rad)), int(center[1] + (size//5) * np.sin(rad)))
        cv2.drawMarker(img, p1, orange, cv2.MARKER_DIAMOND, size//10, 2)

    # 4. Heavy Bloom Effect
    glow = cv2.GaussianBlur(img, (31, 31), 0)
    img = cv2.addWeighted(img, 1.0, glow, 3.0, 0)
    return img

def main():
    cap = cv2.VideoCapture(0)
    
    # --- FULL SCREEN SETUP ---
    window_name = "Sorcerer Supreme - Full Screen"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    angle = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        # Resize frame to fit full screen resolution if needed
        # frame = cv2.resize(frame, (1920, 1080)) 
        
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        
        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                cx = int(hand_lms.landmark[9].x * w)
                cy = int(hand_lms.landmark[9].y * h)
                
                t, p = hand_lms.landmark[4], hand_lms.landmark[20]
                dist = np.sqrt((t.x - p.x)**2 + (t.y - p.y)**2)
                s_size = int(dist * 1400) # Increased scale for full screen
                
                if s_size > 100:
                    shield = draw_mandala(s_size, angle)
                    sh, sw = shield.shape[:2]
                    
                    y1, y2 = max(0, cy - sh//2), min(h, cy + sh//2)
                    x1, x2 = max(0, cx - sw//2), min(w, cx + sw//2)
                    
                    shield_crop = shield[0:(y2-y1), 0:(x2-x1)]
                    roi = frame[y1:y2, x1:x2]
                    
                    if roi.shape == shield_crop.shape:
                        frame[y1:y2, x1:x2] = cv2.add(roi, shield_crop)
                    
                    # Particles
                    for _ in range(2):
                        particles.append(Particle(cx, cy, (0, 140, 255)))

        # Update and Draw Particles
        for p in particles[:]:
            p.update()
            if p.life > 0:
                color = tuple([int(c * p.life) for c in p.color])
                cv2.circle(frame, (int(p.x), int(p.y)), random.randint(1, 3), color, -1)
            else:
                particles.remove(p)

        # HUD Overlay (Corner Brackets)
        length = 50
        cv2.line(frame, (20, 20), (20, 20+length), (0, 255, 255), 2)
        cv2.line(frame, (20, 20), (20+length, 20), (0, 255, 255), 2)
        cv2.line(frame, (w-20, h-20), (w-20, h-20-length), (0, 255, 255), 2)
        cv2.line(frame, (w-20, h-20), (w-20-length, h-20), (0, 255, 255), 2)

        angle += 15
        cv2.imshow(window_name, frame)
        
        # Press 'ESC' or 'q' to exit full screen
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()