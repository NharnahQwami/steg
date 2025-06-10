from django.shortcuts import render
from .stego_utils import encode_message, decode_message
from PIL import Image
import os
from django.core.files.storage import default_storage
from django.http import FileResponse
import tempfile

def index(request):
    return render(request, 'stego/index.html')

def encode_view(request):
    if request.method == 'POST':
        image = request.FILES['image']
        message = request.POST['message']

        img_path = default_storage.save('temp_input.png', image)
        input_path = default_storage.path(img_path)
        output_path = input_path.replace('temp_input.png', 'output.png')

        encode_message(input_path, output_path, message)

        # Prepare file for download and cleanup
        response = None
        try:
            response = FileResponse(open(output_path, 'rb'), as_attachment=True, filename='output.png')
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        return response

def decode_view(request):
    if request.method == 'POST':
        image = request.FILES['image']
        img_path = default_storage.save('decode_input.png', image)
        input_path = default_storage.path(img_path)

        hidden_message = decode_message(input_path)

        return render(request, 'stego/result.html', {
            'hidden_message': hidden_message
        })
