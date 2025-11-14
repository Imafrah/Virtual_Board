import cv2
import sys
from modules import HandTracker, VirtualKeyboard, DrawingCanvas, AIAssistant, SketchManager
import config


class AirBoard:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        
        # Enhanced camera settings for consistent quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, 30)  # Set consistent frame rate
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer lag
        
        # Try to set these if your camera supports them
        try:
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        except:
            pass

        if not self.cap.isOpened():
            print("Error: Could not open camera")
            sys.exit(1)

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read from camera")
            sys.exit(1)

        self.frame_h, self.frame_w = frame.shape[:2]

        # Initialize modules
        self.hand_tracker = HandTracker(
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
            max_num_hands=config.MAX_NUM_HANDS
        )

        self.drawing_canvas = DrawingCanvas(
            self.frame_w,
            self.frame_h,
            color=(0, 165, 255),  # Orange-ish pen color
            brush_size=config.DEFAULT_BRUSH_SIZE
        )

        self.keyboard = VirtualKeyboard(
            key_w=config.KEY_WIDTH,
            key_h=config.KEY_HEIGHT,
            key_margin=config.KEY_MARGIN,
            hover_threshold=config.HOVER_THRESHOLD
        )

        self.sketch_manager = SketchManager(
            save_dir=config.SKETCH_DIR,
            thumbnail_size=config.THUMBNAIL_SIZE
        )

        # AI Assistant
        self.ai_response = ""
        self.ai = AIAssistant(
            api_key=config.GEMINI_API_KEY,
            model=config.AI_MODEL
        )

        self.mode = "DRAW"
        self.show_help = True

    # Helper: word wrap for AI text
    def format_ai_text(self, text, max_chars, max_lines=20):
        if not text:
            return []
        lines = []
        for para in text.split('\n'):
            para = para.strip()
            if not para:
                continue
            words = para.split()
            current = ""
            for word in words:
                if len(current + " " + word) <= max_chars:
                    current = (current + " " + word).strip()
                else:
                    lines.append(current)
                    current = word
                if len(lines) >= max_lines:
                    return lines
            if current:
                lines.append(current)
                if len(lines) >= max_lines:
                    return lines
        return lines

    # === AI Response Overlay (DRAW Mode) ===
    def display_ai_response(self, frame):
        if not self.ai_response:
            return frame

        # Styling constants
        margin = 40
        header_h = 40
        padding = 25
        line_height = 30
        font_size = 0.6
        font_thickness = 1
        
        # Calculate dimensions
        top_margin = margin + (270 if self.show_help else 50)
        max_width = int(self.frame_w * 0.4)  # Limit width for better readability
        
        # Format text with word wrapping
        lines = []
        for line in self.ai_response.split('\n'):
            if line.strip() == '':
                lines.append('')
                continue
                
            words = line.split()
            current_line = ''
            
            for word in words:
                # Check if we should start a new line
                if not current_line:
                    test_line = word
                else:
                    test_line = f"{current_line} {word}"
                
                # Get text width
                (w, _), _ = cv2.getTextSize(test_line, 
                                          cv2.FONT_HERSHEY_SIMPLEX, 
                                          font_size, 
                                          font_thickness)
                
                if w <= max_width - 2 * padding:
                    current_line = test_line
                else:
                    if current_line:  # Only add if not empty
                        lines.append(current_line)
                    # Start new line with current word
                    current_line = word if len(word) * 10 <= max_width else word[:max_width//10] + '...'
            
            # Add the last line if not empty
            if current_line.strip():
                lines.append(current_line)
        
        # Calculate total height needed
        content_h = len(lines) * line_height + padding * 2
        box_h = header_h + content_h + padding
        
        # Draw semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, 
                     (margin, top_margin), 
                     (margin + max_width, top_margin + box_h), 
                     (20, 20, 40), -1)
        frame = cv2.addWeighted(overlay, 0.8, frame, 0.2, 0)
        
        # Draw header with gradient
        for i in range(header_h):
            alpha = i / header_h
            color = (
                int(30 * (1 - alpha) + 10 * alpha),
                int(80 * (1 - alpha) + 40 * alpha),
                int(150 * (1 - alpha) + 100 * alpha)
            )
            cv2.line(frame, 
                    (margin, top_margin + i), 
                    (margin + max_width, top_margin + i), 
                    color, 1)
        
        # Draw header text with shadow
        cv2.putText(frame, "AI Response", 
                   (margin + 15, top_margin + int(header_h * 0.7)), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Draw content with better formatting
        y = top_margin + header_h + padding
        for line in lines[:15]:  # Limit to 15 lines max
            if not line.strip():
                y += line_height // 2  # Smaller gap for empty lines
                continue
                
            # Draw text with shadow for better readability
            cv2.putText(frame, line, 
                       (margin + padding + 1, y + 1), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 0, 0), 
                       font_thickness + 1, cv2.LINE_AA)
            cv2.putText(frame, line, 
                       (margin + padding, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 
                       font_thickness, cv2.LINE_AA)
            y += line_height
            
        return frame

    # === AI Side Panel (KEYBOARD Mode) ===
    def display_ai_side_panel(self, frame, panel_x, panel_y, panel_w, panel_h):
        # Calculate panel dimensions and position
        panel_h = int(self.frame_h * 0.8)
        panel_y = 10
        
        # Calculate content area dimensions with padding
        padding = 15
        content_x = panel_x + padding
        content_width = panel_w - 2 * padding
        
        # Draw semi-transparent background for the panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (panel_x, panel_y),
                     (panel_x + panel_w, panel_y + panel_h),
                     (32, 32, 64), -1)
        frame = cv2.addWeighted(overlay, 0.15, frame, 0.85, 0)

        # Draw header with gradient
        header_h = 40
        for i in range(header_h):
            alpha = i / header_h
            color = (
                int(52 * (1 - alpha) + 70 * alpha),
                int(170 * (1 - alpha) + 190 * alpha),
                int(240 * (1 - alpha) + 255 * alpha)
            )
            cv2.line(frame, (panel_x, panel_y + i),
                   (panel_x + panel_w, panel_y + i), color, 1)

        # Draw header text with shadow
        cv2.putText(frame, "AI Response",
                   (panel_x + 18, panel_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # If no response, show waiting message
        if not self.ai_response:
            cv2.putText(frame, "(Waiting for your question...)",
                       (content_x, panel_y + 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 220), 1)
            return frame

        # Calculate text metrics
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        line_spacing = 5
        
        # Get text size for a single line to calculate line height
        (_, text_height), _ = cv2.getTextSize("A", font, font_scale, font_thickness)
        line_height = text_height + line_spacing
        
        # Calculate available height for content
        content_start_y = panel_y + header_h + padding
        available_height = panel_h - header_h - 2 * padding
        max_lines = available_height // line_height
        
        # Format text with word wrapping and limit to visible lines
        lines = self.format_ai_text(self.ai_response, 45, max_lines)  # Reduced further to ensure fit
        
        # Draw each line with proper word wrapping and boundary checking
        y = content_start_y
        for i, line in enumerate(lines):
            if y + line_height > panel_y + panel_h - padding:
                break
                
            # Split line if it's too wide
            while line:
                # Find the longest prefix that fits
                for j in range(len(line), 0, -1):
                    (w, _), _ = cv2.getTextSize(line[:j], font, font_scale, font_thickness)
                    if w <= content_width or j == 1:
                        # Draw the text with shadow for better readability
                        cv2.putText(frame, line[:j], (content_x + 1, y + 1),
                                  font, font_scale, (0, 0, 0), font_thickness + 1, cv2.LINE_AA)
                        cv2.putText(frame, line[:j], (content_x, y),
                                  font, font_scale, (230, 230, 250), font_thickness, cv2.LINE_AA)
                        y += line_height
                        line = line[j:].lstrip()
                        break
                
                # If we've reached the bottom, stop drawing
                if y + line_height > panel_y + panel_h - padding:
                    break
        return frame

    # === UI & Help Panel ===
    def draw_ui(self, frame):
        mode_color = (0, 255, 0) if self.mode == "DRAW" else (255, 165, 0)
        cv2.rectangle(frame, (10, 10), (200, 50), (0, 0, 0), -1)
        cv2.putText(frame, f"Mode: {self.mode}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_color, 2)

        if self.ai.is_busy():
            cv2.putText(frame, "AI Processing...", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        if self.show_help:
            overlay = frame.copy()
            panel_w, panel_h = 320, 140
            panel_x = self.frame_w - panel_w - 10
            panel_y = self.frame_h - panel_h - 10
            cv2.rectangle(overlay, (panel_x, panel_y),
                          (panel_x + panel_w, panel_y + panel_h), (0, 0, 0), -1)
            frame = cv2.addWeighted(overlay, 0.15, frame, 0.85, 0)

            help_texts = [
                "'M' - Switch Mode",
                "'S' - Save Sketch",
                "'C' - Clear Canvas",
                "'R' - Reset AI",
                "'H' - Toggle Help",
                "'Q' - Quit"
            ]
            y = panel_y + 25
            for t in help_texts:
                cv2.putText(frame, t, (panel_x + 10, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y += 22
        return frame

    # === Main Loop ===
    def run(self):
        print("AirBoard Started!")
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            
            # Flip frame immediately for consistent processing
            frame = cv2.flip(frame, 1)
            
            # Process hand tracking
            frame = self.hand_tracker.find_hands(frame, draw=False)
            hands = self.hand_tracker.get_all_landmarks()
            fingertip_points = []

            if hands:
                for hand in hands:
                    x, y = self.hand_tracker.get_index_finger_tip(hand, frame.shape)
                    fingertip_points.append((x, y))
                    if self.mode == "DRAW":
                        if self.hand_tracker.is_index_only_up(hand):
                            self.drawing_canvas.draw_line(x, y)
                        else:
                            self.drawing_canvas.reset_position()
                    elif self.mode == "KEYBOARD":
                        kb_panel_x = 20
                        kb_panel_w = int(self.frame_w * 0.64)
                        kb_panel_y = self.keyboard.start_y - 50
                        kb_panel_h = 4 * (self.keyboard.key_h + self.keyboard.key_margin) + 70
                        frame, action = self.keyboard.handle_hover(x, y, frame,
                            panel_rect=(kb_panel_x, kb_panel_y, kb_panel_w, kb_panel_h))
                        if action == "SEND":
                            text = self.keyboard.get_text().strip()
                            if text:
                                self.ai.query(text, lambda r: setattr(self, "ai_response", r))
                                self.keyboard.clear_text()
            else:
                self.drawing_canvas.reset_position()

            # Mode-specific rendering
            if self.mode == "DRAW":
                # Overlay the drawing canvas on the camera frame
                frame = self.drawing_canvas.overlay_on_frame(frame)
            else:
                self.keyboard.key_w = 60
                self.keyboard.key_h = 60
                self.keyboard.key_margin = 10
                kb_panel_x = 20
                kb_panel_w = int(self.frame_w * 0.64)
                kb_panel_y = self.keyboard.start_y - 50
                kb_panel_h = 4 * (self.keyboard.key_h + self.keyboard.key_margin) + 70
                frame = self.keyboard.draw(frame, panel_rect=(kb_panel_x, kb_panel_y, kb_panel_w, kb_panel_h))
                ai_panel_w = self.frame_w - (kb_panel_x + kb_panel_w) - 30
                ai_panel_x = kb_panel_x + kb_panel_w + 10
                ai_panel_y = self.keyboard.start_y - 50
                ai_panel_h = kb_panel_h
                frame = self.display_ai_side_panel(frame, ai_panel_x, ai_panel_y, ai_panel_w, ai_panel_h)

            # Draw hand landmarks and fingertips
            frame = self.hand_tracker.find_hands(frame, draw=True)
            for (fx, fy) in fingertip_points:
                cv2.circle(frame, (fx, fy), 12, (255, 0, 255), -1)
                cv2.circle(frame, (fx, fy), 15, (255, 255, 255), 2)

            # Draw UI elements based on mode
            if self.mode == "DRAW":
                # Show sketch gallery at the bottom
                thumb_w, thumb_h = self.sketch_manager.thumbnail_size
                spacing = 12
                max_disp = max(1, (self.frame_w - 20) // (thumb_w + spacing))
                gal_x = 10
                gal_y = self.frame_h - thumb_h - 12
                frame = self.sketch_manager.draw_gallery(
                    frame,
                    max_display=int(max_disp),
                    x_offset=gal_x,
                    y_offset=gal_y,
                    orientation='horizontal',
                    spacing=spacing
                )
            
            frame = self.draw_ui(frame)

            cv2.imshow("AirBoard - Touchless Whiteboard", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                self.mode = "KEYBOARD" if self.mode == "DRAW" else "DRAW"
            elif key == ord('c'):
                self.drawing_canvas.clear()
                self.keyboard.clear_text()
            elif key == ord('s') and self.mode == "DRAW":
                self.sketch_manager.save_sketch(self.drawing_canvas.get_canvas())
            elif key == ord('r'):
                self.ai_response = ""
            elif key == ord('h'):
                self.show_help = not self.show_help

        self.cap.release()
        cv2.destroyAllWindows()


def main():
    try:
        AirBoard().run()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()