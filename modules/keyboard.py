import cv2
import time

class VirtualKeyboard:
    def __init__(self, key_w=80, key_h=80, key_margin=14, hover_threshold=1.5):
        self.keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<-'],
            ['SPACE', 'CLEAR', 'SEND']
        ]
        self.key_w = key_w
        self.key_h = key_h
        self.key_margin = key_margin
        self.start_y = 140  # Y position of first row
        self.typed_text = ""
        self.hover_time = {}
        self.hover_threshold = hover_threshold
        self.last_activated_key = None

    def draw(self, frame, panel_rect=None):
        # Panel background under keys (semi-transparent)
        # panel_rect: (x, y, w, h) area to use for keyboard; defaults to full width
        if panel_rect is None:
            panel_x = self.key_margin
            panel_w = frame.shape[1] - 2 * self.key_margin
            area_w = frame.shape[1]
        else:
            px, py, pw, ph = panel_rect
            panel_x = px
            panel_w = pw
            area_w = pw
        panel_y = self.start_y - 50
        panel_h = 4 * (self.key_h + self.key_margin) + 70
        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x, panel_y), 
                      (panel_x+panel_w, panel_y+panel_h), (32,32,64), -1, cv2.LINE_AA)
        frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

        # Key buttons (dynamically spaced)
        for i, row in enumerate(self.keys):
            row_length = len(row)
            row_total_width = sum([self.key_w * (3 if k == 'SPACE' else 2 if k in ['CLEAR', 'SEND'] else 1) + self.key_margin for k in row]) - self.key_margin
            # center within available area (panel_x .. panel_x+panel_w)
            row_x = panel_x + (panel_w - row_total_width) // 2
            y = self.start_y + i * (self.key_h + self.key_margin)

            for key in row:
                key_width = self.key_w * 3 if key == 'SPACE' else self.key_w * 2 if key in ['CLEAR', 'SEND'] else self.key_w
                x = row_x
                # Custom style/color per key type
                active_color = (160, 80, 255) if key in ['CLEAR', 'SEND', '<-', 'SPACE'] else (100,200,240)
                border_color = (255,255,255)
                shadow_color = (30,30,30)
                text_color = (0,0,0) if key in ['CLEAR', 'SEND', '<-', 'SPACE'] else (255,255,255)
                font_scale = 0.75 if len(key) > 1 else 1.15

                # Shadow
                cv2.rectangle(frame, (x+4, y+4), (x+key_width+4, y+self.key_h+4), shadow_color, -1, cv2.LINE_AA)
                # Main
                cv2.rectangle(frame, (x, y), (x+key_width, y+self.key_h), active_color, -1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+key_width, y+self.key_h), border_color, 3, cv2.LINE_AA)
                # Text
                text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                text_x = x + (key_width - text_size[0]) // 2
                text_y = y + (self.key_h + text_size[1]) // 2
                cv2.putText(frame, key, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, 2, cv2.LINE_AA)
                row_x += key_width + self.key_margin

        # Text display area
        text_bg_y = self.start_y - 80
        text_bg_x = panel_x
        text_bg_w = panel_w
        overlay = frame.copy()
        cv2.rectangle(overlay, (text_bg_x, text_bg_y),
                      (text_bg_x+text_bg_w, text_bg_y+48), (52,170,240), -1, cv2.LINE_AA)
        frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
        cv2.putText(frame, self.typed_text, (text_bg_x+28, text_bg_y+37),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3, cv2.LINE_AA)
        return frame

    def get_hovered_key(self, x, y, frame_w=None, panel_rect=None):
        for i, row in enumerate(self.keys):
            row_length = len(row)
            row_total_width = sum([self.key_w * (3 if k == 'SPACE' else 2 if k in ['CLEAR', 'SEND'] else 1) + self.key_margin for k in row]) - self.key_margin
            # Determine available width
            if panel_rect is None:
                avail_w = frame_w if frame_w is not None else 1280
                start_x = (avail_w - row_total_width) // 2
            else:
                px, py, pw, ph = panel_rect
                start_x = px + (pw - row_total_width) // 2
            key_y = self.start_y + i * (self.key_h + self.key_margin)
            for key in row:
                key_width = self.key_w * 3 if key == 'SPACE' else self.key_w * 2 if key in ['CLEAR', 'SEND'] else self.key_w
                key_x = start_x
                if key_x < x < key_x + key_width and key_y < y < key_y + self.key_h:
                    return key, (key_x, key_y, key_width, self.key_h)
                start_x += key_width + self.key_margin
        return None, None

    def handle_hover(self, x, y, frame, panel_rect=None):
        key, bounds = self.get_hovered_key(x, y, frame_w=frame.shape[1], panel_rect=panel_rect)
        if key:
            if key not in self.hover_time:
                self.hover_time[key] = time.time()
            elapsed = time.time() - self.hover_time[key]
            # Key progress bar
            if bounds:
                kx, ky, kw, kh = bounds
                progress = min(elapsed / self.hover_threshold, 1.0)
                progress_w = int(kw * progress)
                cv2.rectangle(frame, (kx, ky + kh - 10),
                              (kx + progress_w, ky + kh), (0, 255, 0), -1)
            # Key activation
            if elapsed >= self.hover_threshold and self.last_activated_key != key:
                action = self.activate_key(key)
                self.hover_time = {}
                self.last_activated_key = key
                return frame, action
        else:
            self.hover_time = {}
            self.last_activated_key = None
        return frame, None

    def activate_key(self, key):
        if key == '<-':
            self.typed_text = self.typed_text[:-1]
        elif key == 'SPACE':
            self.typed_text += ' '
        elif key == 'CLEAR':
            self.typed_text = ''
        elif key == 'SEND':
            return 'SEND'
        else:
            self.typed_text += key
        return None

    def get_text(self):
        return self.typed_text

    def clear_text(self):
        self.typed_text = ''
