import os
import json
import urllib.request
import urllib.error
import time

def call_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY is not set.")
        return
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={api_key}"
    
    prompt = """
撰写一篇关于佳能 RF 镜头的摄影教育博文。
标题：佳能 RF 全家桶实战：从扫街到打鸟的参数进阶
结构：
1. 人像篇: Canon R5 + RF 50mm f/1.2 L USM. 重点: 大光圈, Eye-AF.
   图片: <img src='https://image.pollinations.ai/prompt/photorealistic%20cinematic%20portrait%20of%20an%20Asian%20woman%20in%20a%20cozy%20bookstore%2C%20warm%20ambient%20light%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2050mm%20f/1.2%20L%20USM%2C%20f/1.2%2C%201/125s%2C%20ISO%20400%2C%20creamy%20bokeh%2C%20extremely%20high%20detail%20skin%20and%20eyes' alt='portrait'>
2. 街拍篇: Canon R5 + RF 24-70mm f/2.8 L USM. 重点: 捕捉动态, 蓝调时刻.
   图片: <img src='https://image.pollinations.ai/prompt/photorealistic%20street%20photography%20of%20a%20busy%20Shanghai%20intersection%20at%20blue%20hour%2C%20motion%20blur%20of%20cars%2C%20sharp%20pedestrian%20crossing%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2024-70mm%20f/2.8%20L%20USM%2C%20f/4%2C%201/30s%2C%20ISO%20800%2C%20vibrant%20city%20colors' alt='street'>
3. 生态篇: Canon R5 + RF 70-200mm f/2.8 L IS USM. 重点: 快快门, 动物检测.
   图片: <img src='https://image.pollinations.ai/prompt/photorealistic%20action%20shot%20of%20a%20kingfisher%20bird%20diving%20into%20water%2C%20splashing%20water%20droplets%20in%20air%2C%20shot%20on%20Canon%20EOS%20R5%2C%20RF%2070-200mm%20f/2.8%20L%20IS%20USM%20at%20200mm%2C%20f/2.8%2C%201/3200s%2C%20ISO%201600%2C%20sharp%20focus%20on%20bird%27s%20eye' alt='wildlife'>
使用 HTML 格式，包含 <h2> 和 <ul>。
"""

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    while True:
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(result['candidates'][0]['content']['parts'][0]['text'])
                return
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(120)
            else:
                print(f"Error {e.code}")
                return

call_gemini()
