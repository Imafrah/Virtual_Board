import cv2
import os
from datetime import datetime

class SketchManager:
    def __init__(self, save_dir="sketches", thumbnail_size=(100, 75)):
        self.save_dir = save_dir
        self.thumbnail_size = thumbnail_size
        self.sketches = []
        
        # Create directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        self.load_sketches()
    
    def save_sketch(self, canvas):
        """Save current sketch with thumbnail"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sketch_{timestamp}.png"
        filepath = os.path.join(self.save_dir, filename)
        
        # Save full-size sketch
        cv2.imwrite(filepath, canvas)
        
        # Create and store thumbnail
        thumbnail = cv2.resize(canvas, self.thumbnail_size)
        self.sketches.append({
            'filepath': filepath,
            'filename': filename,
            'thumbnail': thumbnail,
            'timestamp': timestamp
        })
        
        return filename
    
    def load_sketches(self):
        """Load existing sketches from directory"""
        if os.path.exists(self.save_dir):
            files = sorted([f for f in os.listdir(self.save_dir) if f.endswith('.png')])
            for filename in files:
                filepath = os.path.join(self.save_dir, filename)
                try:
                    img = cv2.imread(filepath)
                    if img is not None:
                        thumbnail = cv2.resize(img, self.thumbnail_size)
                        timestamp = filename.replace('sketch_', '').replace('.png', '')
                        self.sketches.append({
                            'filepath': filepath,
                            'filename': filename,
                            'thumbnail': thumbnail,
                            'timestamp': timestamp
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def draw_gallery(self, frame, max_display=5, x_offset=None, y_offset=None, orientation='vertical', spacing=10):
        """Draw sketch thumbnails on frame at optional (x_offset, y_offset).
        orientation: 'vertical' or 'horizontal'
        """
        if x_offset is None:
            x_offset = frame.shape[1] - 120
        if y_offset is None:
            y_offset = 50
        
        # Gallery header
        cv2.rectangle(frame, (x_offset-10, y_offset-30), 
                     (x_offset+110, y_offset-5), (50, 50, 50), -1)
        cv2.putText(frame, f"Saved ({len(self.sketches)})", (x_offset, y_offset - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display last N sketches
        recent_sketches = self.sketches[-max_display:]
        for i, sketch in enumerate(recent_sketches):
            if orientation == 'horizontal':
                x_pos = x_offset + i * (self.thumbnail_size[0] + spacing)
                y_pos = y_offset
                try:
                    frame[y_pos:y_pos+self.thumbnail_size[1],
                          x_pos:x_pos+self.thumbnail_size[0]] = sketch['thumbnail']
                    cv2.rectangle(frame, (x_pos, y_pos),
                                  (x_pos+self.thumbnail_size[0], y_pos+self.thumbnail_size[1]),
                                  (255, 255, 255), 2)
                except Exception as e:
                    print(f"Error displaying thumbnail: {e}")
            else:
                y_pos = y_offset + i * 85
                try:
                    frame[y_pos:y_pos+self.thumbnail_size[1], 
                          x_offset:x_offset+self.thumbnail_size[0]] = sketch['thumbnail']
                    cv2.rectangle(frame, (x_offset, y_pos), 
                                  (x_offset+self.thumbnail_size[0], y_pos+self.thumbnail_size[1]), 
                                  (255, 255, 255), 2)
                except Exception as e:
                    print(f"Error displaying thumbnail: {e}")
        
        return frame
    
    def get_sketch_count(self):
        """Return number of saved sketches"""
        return len(self.sketches)
    
    def clear_all(self):
        """Delete all sketches"""
        for sketch in self.sketches:
            try:
                if os.path.exists(sketch['filepath']):
                    os.remove(sketch['filepath'])
            except Exception as e:
                print(f"Error deleting {sketch['filename']}: {e}")
        
        self.sketches = []