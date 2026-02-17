import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

def upload_permanent_material(image_path, media_type='image'):
    appid = os.getenv('WECHAT_APPID')
    appsecret = os.getenv('WECHAT_APPSECRET')
    
    # 1. Get Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    with urllib.request.urlopen(token_url) as response:
        token = json.loads(response.read().decode('utf-8'))['access_token']
    
    # 2. Upload Material
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type={media_type}"
    
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    filename = os.path.basename(image_path)
    body = []
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="media"; filename="{filename}"'.encode())
    body.append(b'Content-Type: image/jpeg')
    body.append(b'')
    body.append(image_data)
    body.append(f'--{boundary}--'.encode())
    data = b'\r\n'.join(body)
    
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': len(data)
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    img = sys.argv[1] if len(sys.argv) > 1 else 'cover_final.jpg'
    res = upload_permanent_material(img)
    print(json.dumps(res, indent=2))
