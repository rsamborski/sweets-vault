import logging
from typing import Any

logger = logging.getLogger(__name__)

class RGBMatrixOptions:
    def __init__(self):
        self.rows = 16
        self.cols = 32
        self.chain_length = 1
        self.parallel = 1
        self.row_address_type = 0
        self.multiplexing = 0
        self.pwm_bits = 11
        self.brightness = 100
        self.pwm_lsb_nanoseconds = 130
        self.led_rgb_sequence = "RGB"
        self.pixel_mapper_config = ""
        self.panel_type = ""
        self.hardware_mapping = "regular"

class RGBMatrix:
    def __init__(self, options: RGBMatrixOptions = None):
        self.options = options or RGBMatrixOptions()
        self.width = self.options.cols * self.options.chain_length
        self.height = self.options.rows
        logger.info(f"Initialized Mock RGBMatrix: {self.width}x{self.height}")

    def Clear(self):
        logger.info("Mock RGBMatrix: Clear")

    def Fill(self, r, g, b):
        logger.info(f"Mock RGBMatrix: Fill({r}, {g}, {b})")

    def SetPixel(self, x, y, r, g, b):
        # logger.debug(f"Mock RGBMatrix: SetPixel({x}, {y}, {r}, {g}, {b})")
        pass

    def SetImage(self, image, x = 0, y = 0):
        logger.info(f"Mock RGBMatrix: SetImage({image}) at ({x}, {y})")

    def CreateFrameCanvas(self):
        return self

    def SwapOnVSync(self, canvas):
        return canvas

class Font:
    def LoadFont(self, path: str):
        logger.info(f"Mock Font: Loaded from {path}")

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class graphics:
    Font = Font
    Color = Color

    @staticmethod
    def DrawText(matrix, font, x, y, color, text):
        logger.info(f"Mock DrawText: '{text}' at ({x}, {y}) with color ({color.r},{color.g},{color.b})")
        return len(text) * 6  # Return dummy width

    @staticmethod
    def DrawLine(matrix, x0, y0, x1, y1, color):
        logger.info(f"Mock DrawLine: ({x0},{y0}) -> ({x1},{y1})")

    @staticmethod
    def DrawCircle(matrix, x, y, r, color):
        logger.info(f"Mock DrawCircle: Center({x},{y}) Radius({r})")
