from django.http import HttpResponse, HttpRequest, FileResponse
from django.views.generic import CreateView

from moviepy import editor
from PIL import Image, ImageDraw, ImageFont
from wsgiref.util import FileWrapper

import logging

from .models import UserRequest

log = logging.getLogger(__name__)


class RequestCreateView(CreateView):

    model = UserRequest
    fields = "input_text",

    def form_valid(self, form):
        self.object = form.save(False)
        text = self.object.input_text
        log.debug("A valid form has been entered. Text: %s", text)
        user_ip = ip_specifier(self.request)
        self.object.user_ip = user_ip
        self.object.save()

        images = []
        width = 100
        height = 100
        font = ImageFont.truetype("fonts/ArialRegular.ttf", 40)
        text_size = int(font.getlength(text))
        log.debug("Text size: %s", text_size)
        start_position = -1 * text_size

        for i_length in range(start_position, text_size + 1, 10):
            im = Image.new('RGB', (width, height), color='#00BFFF')
            draw_text = ImageDraw.Draw(im)
            first_position = -1 * i_length
            draw_text.text(
                (first_position, 30),
                text,
                fill='#1C0606',
                font=font,
            )
            images.append(im)

        duration = int(3550 / len(images))
        log.debug("Duration: %s", duration)
        images[0].save(
            'content/ticker.gif',
            save_all=True,
            append_images=images[1:],
            optimize=False,
            duration=duration,
            loop=0
        )

        clip = editor.VideoFileClip('content/ticker.gif')
        clip.write_videofile('content/ticker.mp4')
        clip.close()

        filename = "ticker.mp4"
        file = FileWrapper(open("content/ticker.mp4", "rb"))
        response = HttpResponse(file, content_type='video/mp4')
        response["Content-Disposition"] = f"attachment; filename={filename}"
        log.info("Sending a mp4 file")

        return response


def ip_specifier(request: HttpRequest):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    return ipaddress
