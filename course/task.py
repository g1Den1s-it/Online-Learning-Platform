import asyncio
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from django.core.files.base import ContentFile

from online_learning_platform import settings
from online_learning_platform.celery import app
from .models import UserCertificate


@app.task()
def create_certificate(recipient_name: str,
                       course_name: str,
                       date: datetime,
                       certificate_blank: str,
                       user_certificate_id: int) -> None:
    certificate_blank_path = os.path.join(settings.MEDIA_ROOT, certificate_blank)
    image = Image.open(certificate_blank_path)
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        title_font = ImageFont.truetype("Roboto-Regular.ttf", 80)
        name_font = ImageFont.truetype("Roboto-Regular.ttf", 50)
        body_font = ImageFont.truetype("Roboto-Regular.ttf", 50)
    except IOError:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # certificate text
    title = "Certificate of Achievement"
    course_description = "This certificate is awarded to"
    completion_text = "for successfully completing the course on"
    completion_date = f"{date.year}-{date.month}-{date.day}"

    # get width by elements
    width, height = image.size
    title_width = draw.textlength(title, font=title_font)
    name_width = draw.textlength(recipient_name, font=name_font)
    course_width = draw.textlength(course_description, font=body_font)
    course_name_width = draw.textlength(course_name, font=body_font)
    date_width = draw.textlength(completion_text, font=body_font)
    completion_date_width = draw.textlength(completion_date, font=body_font)

    # x position set up
    title_x = (width - title_width) / 2
    name_x = (width - name_width) / 2
    course_x = (width - course_width) / 2
    course_name_x = (width - course_name_width) / 2
    date_x = (width - date_width) / 2
    completion_date_x = (width - completion_date_width) / 2

    # Draw text on the certificate
    draw.text((title_x, 350), title, fill="black", font=title_font)  # Title at the top
    draw.text((name_x, 550), recipient_name, fill="blue", font=name_font)  # Recipient's name
    draw.text((course_x, 650), course_description, fill="black", font=body_font)  # Course description
    draw.text((course_name_x, 750), course_name, fill="blue", font=body_font)  # Course name
    draw.text((date_x, 850), completion_text, fill="black", font=body_font)  # Completion text
    draw.text((completion_date_x, 950), completion_date, fill="black", font=body_font)  # Date

    image.convert('L')

    io_image = BytesIO()

    image.save(io_image, format="PNG")

    user_certificate = UserCertificate.objects.get(pk=user_certificate_id)

    user_certificate.certificate.save(
        f"{recipient_name}_certificate".replace(" ", "_") + ".png",
        ContentFile(io_image.getvalue()),
        save=False
    )

    user_certificate.save()
