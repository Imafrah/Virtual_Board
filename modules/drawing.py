import cv2
import numpy as np

class DrawingCanvas:
    def __init__(self, width, height, color=(0, 255, 0), brush_size=5):
        self.width = width
        self.height = height
        # Use 4 channels (BGRA) for proper transparency
        self.canvas = np.zeros((height, width, 4), dtype=np.uint8)
        self.color = color  # BGR format
        self.brush_size = brush_size
        self.prev_x = None
        self.prev_y = None
    
    def draw_line(self, x, y):
        """Draw line from previous position to current"""
        if self.prev_x is not None and self.prev_y is not None:
            # Draw with full opacity (alpha = 255)
            cv2.line(self.canvas, (self.prev_x, self.prev_y), 
                    (x, y), (*self.color, 255), self.brush_size)
        self.prev_x, self.prev_y = x, y
    
    def reset_position(self):
        """Reset drawing position (lift pen)"""
        self.prev_x, self.prev_y = None, None
    
    def clear(self):
        """Clear entire canvas"""
        self.canvas = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self.reset_position()
    
    def get_canvas(self):
        """Get current canvas (3-channel version for saving)"""
        # Convert BGRA to BGR for saving
        return self.canvas[:, :, :3].copy()
    
    def set_color(self, color):
        """Change drawing color (BGR format)"""
        self.color = color
    
    def set_brush_size(self, size):
        """Change brush size"""
        self.brush_size = max(1, size)
    
    def overlay_on_frame(self, frame):
        """
        Overlay ONLY the drawn lines on frame without darkening.
        This preserves the original camera quality.
        """
        # Check if canvas is empty (optimization)
        if np.max(self.canvas[:, :, 3]) == 0:
            return frame
        
        # Get alpha channel (where drawings exist)
        alpha = self.canvas[:, :, 3] / 255.0
        
        # Expand alpha to 3 channels for vectorized operation
        alpha_3ch = np.stack([alpha, alpha, alpha], axis=2)
        
        # Get BGR channels from canvas
        canvas_bgr = self.canvas[:, :, :3]
        
        # Blend: output = frame * (1 - alpha) + canvas * alpha
        # This only affects pixels where alpha > 0 (where you drew)
        blended = (frame * (1 - alpha_3ch) + canvas_bgr * alpha_3ch).astype(np.uint8)
        
        return blended