from io import BytesIO
from PIL import Image
import eel
import PIL
from keras.saving.save import load_model
import os
from keras_preprocessing.image.utils import img_to_array, load_img
import numpy as np
import base64

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

eel.init('web')

model = load_model('upscaler.tf')

@eel.expose
def upscale_image(b64img,name):
    """Predict the result based on input image and restore the image as RGB."""

    img = Image.open(BytesIO(base64.b64decode(b64img)))
    w = img.size[0] * 3
    h = img.size[1] * 3

    img.resize((w,h),PIL.Image.BICUBIC,)

    ycbcr = img.convert("YCbCr")
    y, cb, cr = ycbcr.split()
    y = img_to_array(y)
    y = y.astype("float32") / 255.0

    input = np.expand_dims(y, axis=0)
    out = model.predict(input)

    out_img_y = out[0]
    out_img_y *= 255.0

    # Restore the image in RGB color space.
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = out_img_y.reshape((np.shape(out_img_y)[0], np.shape(out_img_y)[1]))
    out_img_y = PIL.Image.fromarray(np.uint8(out_img_y), mode="L")
    out_img_cb = cb.resize(out_img_y.size, PIL.Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, PIL.Image.BICUBIC)
    out_img = PIL.Image.merge("YCbCr", (out_img_y, out_img_cb, out_img_cr)).convert(
        "RGB"
    )
    # out_img = out_img.filter(ImageFilter.DETAIL);
    # out_img = out_img.filter(ImageFilter.SHARPEN);
    out_img.save("./web/out/"+name+".jpg")
    return True


eel.start('index.html',size=(1280, 720))