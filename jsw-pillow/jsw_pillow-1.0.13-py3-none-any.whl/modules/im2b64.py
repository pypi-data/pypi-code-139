import io
import base64


def im2b64(im):
    buffer = io.BytesIO()
    im.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.read())
