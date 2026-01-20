import sys
import os

# Suppress DWPose logs from external dependencies
class DWPoseLogFilter:
    """Filter to suppress DWPose timing and diagnostic logs"""
    def __init__(self, stream):
        self.stream = stream
        self.buffer = ""
        self.suppression_keywords = ["DWPose:", "Bbox", "Pose", "torchscript"]
        
    def write(self, text):
        if not text:
            return 0
            
        # Add to buffer
        self.buffer += text
        
        # Process complete lines
        lines_to_write = []
        while '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            # Skip lines that contain suppression keywords OR are empty/whitespace-only
            if not any(keyword in line for keyword in self.suppression_keywords) and line.strip():
                lines_to_write.append(line + '\n')
        
        # Write accumulated non-filtered lines
        if lines_to_write:
            self.stream.write(''.join(lines_to_write))
        
        return len(text)
    
    def flush(self):
        self.stream.flush()
    
    def __getattr__(self, name):
        return getattr(self.stream, name)

# Apply the filter
sys.stdout = DWPoseLogFilter(sys.stdout)
sys.stderr = DWPoseLogFilter(sys.stderr)

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]