# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from PIL import Image

logger = logging.getLogger(__name__)

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
    logger.info("RGBMatrix imported successfully.")
except ImportError:
    from app.mock_rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
    logger.warning("RGBMatrix not imported. Using mock implementation.")

# Preload the images - for some reason this fails if done in __init__
padlock_size = 12
padlock_closed = Image.open("img/padlock-closed.png")
padlock_closed.thumbnail((padlock_size, padlock_size), Image.LANCZOS)
padlock_open = Image.open("img/padlock-open.png")
padlock_open.thumbnail((padlock_size, padlock_size), Image.LANCZOS)

class LedMatrixController:
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.rows = 16
        self.options.cols = 32
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'regular'  
        
        # Configure for best performance/compatibility if needed
        # self.options.gpio_slowdown = 4

        self.matrix = RGBMatrix(options=self.options)
        self.font = graphics.Font()
        # We assume a font file exists or we use default if available. 
        # For simplicity in this snippet, we'll try to load a common one or skip if failing.
        # Ideally, font file should be bundled.
        try:
            self.font.LoadFont("fonts/5x7.bdf") # Example font
        except Exception:
            logger.warning("Failed to load font.")
            pass

        self.color_text = graphics.Color(255, 255, 255) # White
        self.canvas = self.matrix.CreateFrameCanvas()
        


        # State tracking for sections
        self.sections = {
            0: {"char": "", "locked": False},
            1: {"char": "", "locked": False}
        }
        
    def clear(self):
        self.sections = {
            0: {"char": "", "locked": False},
            1: {"char": "", "locked": False}
        }
        self.canvas.Clear()
        self.matrix.SwapOnVSync(self.canvas)
        logger.info("Matrix cleared")

    def update_section(self, section_id: int, char: str, locked: bool):
        if section_id not in [0, 1]:
            raise ValueError(f"Invalid section_id {section_id}")
        
        self.sections[section_id] = {"char": char, "locked": locked}
        self._draw()

    def _draw(self):
        self.canvas.Clear()
        
        # Each section is 16x16
        # Section 0: x=0 to 15
        # Section 1: x=16 to 31
        
        for section_id, data in self.sections.items():
            if not data["char"]:
                continue
                
            offset_x = section_id * 16
            
            # --- Draw Character ---
            # Attempt to center or place in upper-left as requested.
            # "upper-left corner of the section"
            # Font positioning usually specifies bottom-left baseline or top-left depending on lib.
            # RGBMatrix graphics.DrawText(canvas, font, x, y, color, text)
            # y is usually baseline. 4x6 font -> baseline around 6?
            # Let's approximate.
            
            # Draw Char in White
            graphics.DrawText(self.canvas, self.font, offset_x, 6, self.color_text, data["char"])
            
            # --- Draw Status Icon ---
            # "locked status ... display a closed lock icon in red"
            # "unlocked ... green unlocked icon"
            # "must not cover the section id"                     
            image = padlock_closed if data["locked"] else padlock_open
            self.matrix.SetImage(image.convert('RGB'), offset_x + 4, 2)
                        
        self.canvas = self.matrix.SwapOnVSync(self.canvas)
