import struct
from PIL import Image
from collections import Counter
import io

def block_reduce(img: Image.Image, block_size: int = 3) -> Image.Image:
    w, h = img.size
    pixels = img.load()
    new_img = Image.new("RGB", (w, h))
    new_pixels = new_img.load()

    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = []
            for dy in range(block_size):
                for dx in range(block_size):
                    if x + dx < w and y + dy < h:
                        block.append(pixels[x + dx, y + dy])
            dominant = Counter(block).most_common(1)[0][0]
            for dy in range(block_size):
                for dx in range(block_size):
                    if x + dx < w and y + dy < h:
                        new_pixels[x + dx, y + dy] = dominant
    return new_img

def save_cpgf(image: Image.Image, file_like: io.BytesIO):
    if image.mode != "RGB":
        image = image.convert("RGB")
    w, h = image.size
    pixels = image.tobytes()
    file_like.write(b"CPGF\x01")
    file_like.write(struct.pack("<I", w))
    file_like.write(struct.pack("<I", h))
    file_like.write(struct.pack("<I", 0))
    file_like.write(pixels)

def load_cpgf(file_like: io.BytesIO) -> Image.Image:
    file_like.seek(0)
    magic = file_like.read(5)
    if magic != b"CPGF\x01":
        raise ValueError("Not a valid CPGF file")
    w = struct.unpack("<I", file_like.read(4))[0]
    h = struct.unpack("<I", file_like.read(4))[0]
    _ = file_like.read(4)  # Reserved
    pixels = file_like.read(w * h * 3)
    if len(pixels) != w * h * 3:
        raise ValueError("File truncated or corrupt")
    return Image.frombytes("RGB", (w, h), pixels)
