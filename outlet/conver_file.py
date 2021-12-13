import base64, secrets, io
from PIL import Image
from django.core.files.base import ContentFile

def get_image_from_data_url(data_url, resize=True, base_width=600 ):
    _format, _dataurl       = data_url.split(';base64,')
    _filename, _extension   = secrets.token_hex(20), _format.split('/')[-1]
    file = ContentFile(base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
    if resize:
        image = Image.open(file)
        image_io = io.BytesIO()
        w_percent    = (base_width/float(image.size[0]))
        h_size       = int((float(image.size[1])*float(w_percent)))
        image        = image.resize((base_width,h_size), Image.ANTIALIAS)
        #image.save(image_io, format=_extension)
        file = ContentFile(image_io.getvalue(), name=f"{_filename}.{_extension}" )
    return file, ( _filename, _extension )


