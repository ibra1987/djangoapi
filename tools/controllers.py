from django.http import JsonResponse
from rembg import remove
from PIL import Image
import imghdr
import time
import calendar
import io
import base64
from .form import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json


# controllers


@csrf_exempt
def remove_background(request):
    if (request.method != "POST"):
        return JsonResponse({
            "error": "Unauthorized method"
        },
            status=400)

    images = request.FILES.getlist('userImages')
    if (images is None or len(images) == 0):
        return JsonResponse({
            "error": "no files uploaded"
        },
            status=400)

    data = []
    for image in images:
        filename = image.name
        img = Image.open(image)
        img = remove(img)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        encoded_image = base64.b64encode(byte_im).decode("ascii")
        data.append({
            "base64": encoded_image,
            "filename": filename,
            "type": image.content_type
        })
        img.close()

    return JsonResponse({

        "success": "ok",
        "data": data
    },
        status=200)


# compess image


@csrf_exempt
def compress_image(request):
    if (request.method == "POST"):
        quality = request.POST.get('quality') if request.POST.get(
            'quality') is not None else 80
        images = request.FILES.getlist('userImages')
        data = []
        if (len(images) > 0):

            for image in images:
                filename = image.name
                image_type = image.content_type
                image_format = "JPEG" if filename.split(
                    '.')[1] == "jpg" or "jpeg" else filename.split('.')[1].upper()
                # print(image_format)
                #
                # if img.mode in ("RGBA", "P"):
                #     img.convert("RGB")
                img = Image.open(image)
                output_buffer = io.BytesIO()
                img.save(output_buffer, format=image_format,
                         quality=int(quality))
                compressed_data = output_buffer.getvalue()
                encoded_image = base64.b64encode(
                    compressed_data).decode("ascii")

                data.append({
                    "base64": encoded_image,
                    "filename": filename,
                    "image_type": image_type
                })
                img.close()
            return JsonResponse({
                "success": "ok",
                "data": data
            },
                status=200)

        else:
            return JsonResponse({
                "error": "No file uploaded"
            }, status=400)

    else:
        return JsonResponse({
            "error": "Unauthorized method"
        }, status=500)


@csrf_exempt
def convert_image(request):
    if (request.method != "POST"):
        return JsonResponse({
            "error": "Unauthorized method"
        }, status=500)

    target_format = request.POST.get('target_format')
    print(target_format)
    data = []
    if (target_format is None):
        return JsonResponse({
            "error": "Please select a target format"
        }, status=400)

    images = request.FILES.getlist('userImages')

    if (images is None or len(images) == 0):
        return JsonResponse({
            "error": "No images selected"
        }, status=400)

    for image in images:
        filename = image.name
        filename = filename.split('.')[0]
        new_filename = (f'{filename}.{target_format.lower()}')
        img = Image.open(image)

        output_buffer = io.BytesIO()
        img.save(output_buffer, format=target_format)

        image_data = output_buffer.getvalue()
        encoded_image = base64.b64encode(
            image_data).decode("ascii")
        img.close()
        data.append({
            "base64": encoded_image,
            "filename": new_filename,
        })

    return JsonResponse({
        "data": data,
        "success": "ok"
    })
