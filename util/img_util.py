import base64
import io
import time
from PIL import Image
from util import oss_util

def convert_img(data : bytes, size : int) -> bytes:
    img_bytes = io.BytesIO(data)
    img = Image.open(img_bytes)
    img.show()
    img = img.convert('RGB')
    img.thumbnail((size, size))
    with io.BytesIO() as output:
        img.save(output, 'JPEG', quality=80, optimize=True)
        data = output.getvalue()
    return data

def get_profile_filename(user_id : int) -> str:
    rand_code = hex(int(time.time() * 100)).strip('0x')
    file_name = f'{user_id}_{rand_code}.jpg'
    return file_name

def upload_profile(data : bytes, user_id : int) -> str:
    data = convert_img(data, 100)
    file_name = get_profile_filename(user_id)
    file_path = f'profile/{file_name}'
    oss_util.upload_file(file_path, data)
    return file_name

def upload_post_image(data : bytes, post_id : int, order_number : int):
    file_name = f'{post_id}_{order_number}.jpg'
    file_path = f'post_image/{file_name}'
    data = convert_img(data, 100)
    oss_util.upload_file(file_path, data)
    return file_name

def base_to_bytes(code : str) -> bytes:
    if code:
        start_index = code.find(',')
        if start_index != -1:
            code = code[start_index + 1:]
    data = base64.b64decode(code)
    return data

def get_profile_url(file_name : str) -> str:
    if file_name:
        return f'{oss_util.get_host()}/profile/{file_name}'
    else:
        return None

def get_post_image_url(file_name : str) -> str:
    return f'{oss_util.get_host()}/post_image/{file_name}'

if __name__ == '__main__':
    pass
    # with open("1.png", 'rb') as f:
    #     data = f.read()
    #     data = convert_img(data, 100)
    #     with open("2.jpg", 'wb') as f2:
    #         f2.write(data)