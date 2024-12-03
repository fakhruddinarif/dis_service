from io import BytesIO
from typing import Final
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fastapi import UploadFile

text: Final[str] = "Find Me"
font_size: Final[int] = 300
font = ImageFont.truetype('Poppins-Medium.ttf', font_size)

def create_watermark(image: UploadFile):
    image = Image.open(BytesIO(image.file.read()), mode='r')
    # Create a new RGBA image for the watermark with the same size as the input image
    watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # Calculate the size of the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position for the text to be centered
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2

    # Draw the text on the watermark image
    soft_grey = (200, 200, 200, 128)
    draw.text((x, y), text, font=font, fill=soft_grey)

    # Combine the watermark with the original image
    watermark_image = Image.alpha_composite(image.convert('RGBA'), watermark)
    return np.array(watermark_image.convert('RGB'))