#!/usr/bin/env python3

import sys
import time
import ST7735 as ST7735
import automationhat as ah

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

try:
    from fonts.ttf import RobotoBlackItalic as UserFont
except ImportError:
    print("""This example requires the Roboto font.
Install with: sudo pip3 install fonts font-roboto
""")
    sys.exit(1)

class DisplayService():
    
    def __init__(self):
        
        self.display = ST7735.ST7735(
            port=0,
            cs=ST7735.BG_SPI_CS_FRONT,
            dc=9,
            backlight=25,
            rotation=270,
            spi_speed_hz=4000000)
        
        self.onColor = (99, 225, 162)
        self.offColor = (235, 102, 121)
        self.bkgColor = (25, 16, 45)
        self.color = (255, 181, 86)
        self.font = ImageFont.truetype(UserFont, 12)

    def _draw_output_states(self, channels) -> None:
        
        self.display.begin()
        
        # Values to keep everything aligned nicely
        on_x, on_y = 115, 35
        off_x, off_y = 46, on_y
        dia = 10
        
        # Open our background image.
        image = Image.open("images/outputs-blank.jpg")
        draw = ImageDraw.Draw(image)
        offset = 0

        # Draw the on/off state of each channel.
        for channel in range(len(channels)):
            if channels[channel].is_on():
                draw.ellipse((on_x, on_y + offset, on_x + dia, on_y + dia + offset), self.onColor)
            else:
                draw.ellipse((off_x, off_y + offset, off_x + dia, off_y + dia + offset), self.offColor)
            offset += 14

        self.display.display(image)
        
        time.sleep(5)
    
    def draw_output_states(self) -> None:
        
        for channel in range(3):
            self._draw_output_states(ah.output())

    def draw_analog_values(self) -> None:
        
        # Values to keep everything aligned nicely.
        text_x, text_y = 110, 34
        bar_x, bar_y = 25, 37
        bar_height, bar_width = 8, 73
        offset = 0

        # Open our background image.
        image = Image.open("images/analog-inputs-blank.jpg")
        draw = ImageDraw.Draw(image)

        # Draw the text and bar for each channel in turn.
        for channel in range(3):
            reading = ah.analog[channel].read()
            draw.text((text_x, text_y + offset), f"{reading:.2f}", font=self.font, fill=self.color)

            # Scale bar dependent on channel reading.
            width = int(bar_width * (reading / 24.0))

            draw.rectangle((bar_x, bar_y + offset, bar_x + width, bar_y + bar_height + offset), self.color)

            offset += 14

        # Draw the image to the display.
        self.display.display(image)

        time.sleep(5)

if __name__ == "__main__":
    
    diss = DisplayService()
    
    '''
    TEST: draw output channel states
    '''
    diss.draw_output_states()
    
    '''
    TEST: draw analog channel values
    '''
    diss.draw_analog_values()
