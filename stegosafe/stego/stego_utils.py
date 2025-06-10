from PIL import Image

def encode_message(input_image_path, output_image_path, message):
    image = Image.open(input_image_path)
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'  # EOF marker

    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    data = image.getdata()
    new_data = []

    data_iter = iter(data)
    for i in range(0, len(binary_message), 3):
        pixels = [list(next(data_iter)) for _ in range(3)]
        for j in range(3):
            if i + j < len(binary_message):
                pixels[j][0] = pixels[j][0] & ~1 | int(binary_message[i + j])
        new_data.extend([tuple(p) for p in pixels])

    new_data.extend(list(data)[len(new_data):])
    encoded_img = Image.new(image.mode, image.size)
    encoded_img.putdata(new_data)
    encoded_img.save(output_image_path)

def decode_message(image_path):
    image = Image.open(image_path)
    binary_data = ''
    for pixel in image.getdata():
        binary_data += str(pixel[0] & 1)
    # Split into 8-bit chunks
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for byte in all_bytes:
        if byte == '11111110':  # EOF marker
            break
        message += chr(int(byte, 2))
    return message
