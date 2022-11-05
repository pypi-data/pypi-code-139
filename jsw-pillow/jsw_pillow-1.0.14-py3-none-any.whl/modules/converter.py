import io
import base64


def im2base64(im):
    buffer = io.BytesIO()
    im.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.read())


class Converter:

    @classmethod
    def base64(cls, im, **kwargs):
        buffer = cls.buffer(im, **kwargs)
        return base64.b64encode(buffer.read())

    @classmethod
    def buffer(cls, im, **kwargs):
        buffer = io.BytesIO()
        im.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer

    @classmethod
    def file(cls, im, **kwargs):
        target = kwargs.get('target')
        im.save(target)
        return target
