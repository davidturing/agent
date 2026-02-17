import os
import json
import urllib.request
import urllib.error

WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"

def get_access_token():
    appid = os.getenv('WECHAT_APPID')
    appsecret = os.getenv('WECHAT_APPSECRET')
    url = f"{WECHAT_API_BASE}/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        return data.get('access_token')

def list_images(token):
    url = f"{WECHAT_API_BASE}/material/batchget_material?access_token={token}"
    data = json.dumps({
        "type": "image",
        "offset": 0,
        "count": 10
    }).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            if 'item' in res:
                return res['item']
            else:
                print("Error:", res)
                return []
    except urllib.error.HTTPError as e:
        print(e.read())
        return []

if __name__ == "__main__":
    token = get_access_token()
    if token:
        items = list_images(token)
        if items:
            print(f"Found {len(items)} images.")
            for item in items:
                print(f"Media ID: {item['media_id']}")
                # print(f"URL: {item['url']}")
        else:
            print("No images found.")
