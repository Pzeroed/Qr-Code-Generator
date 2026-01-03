import qrcode
from PIL import Image
import os

ERROR_CORR_MAP = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H
}

def generate_qr_image(
    data,
    box_size=10,
    fg_color="#000000",
    bg_color="#ffffff",
    error_correction="H",
    logo_path=None
):
    if not data:
        return Image.new("RGB", (box_size * 29, box_size * 29), bg_color)

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORR_MAP.get(error_correction),
        box_size=box_size,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=fg_color,
        back_color=bg_color
    ).convert("RGB")

    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)
            size = img.size[0] // 4
            logo = logo.resize((size, size))
            pos = ((img.size[0] - size) // 2, (img.size[1] - size) // 2)
            img.paste(logo, pos, logo if logo.mode == "RGBA" else None)
        except:
            pass

    return img
