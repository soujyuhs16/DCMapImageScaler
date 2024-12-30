class PreviewState:
    """Manages the state of the preview functionality"""
    def __init__(self):
        self._is_previewing = False
        
    @property
    def is_previewing(self):
        return self._is_previewing
        
    def start_preview(self):
        self._is_previewing = True
        
    def end_preview(self):
        self._is_previewing = False