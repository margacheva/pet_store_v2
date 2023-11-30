from PIL import Image
from io import BytesIO


def resize_and_convert_to_jpg(image_data):
    image = Image.open(BytesIO(image_data))
    image = image.convert('RGB')
    image_resized = image.resize((280, 280))
    output_buffer = BytesIO()
    image_resized.save(output_buffer, format="JPEG")
    jpg_data = output_buffer.getvalue()

    return jpg_data
