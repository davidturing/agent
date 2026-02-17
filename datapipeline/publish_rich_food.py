import os
import xmlrpc.client
import sys

# Configuration
url = "https://dvcamera6.wordpress.com/xmlrpc.php"
username = "davidturing"
password = "5hyx wocr tyom lwef"
image_url = "http://dvcamera6.files.wordpress.com/2026/02/f5d41b29-cbb0-4ab2-ac52-a56aa535d87e.jpg"

def create_rich_post():
    server = xmlrpc.client.ServerProxy(url)
    
    title = "食在深圳：陈鹏鹏金牌卤鹅探店，舌尖上的潮汕仪式感"
    
    # 精彩描述 - 采用更精美的 HTML 排版
    body = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
        <p style="font-size: 18px; color: #d93025; font-weight: bold; border-left: 4px solid #d93025; padding-left: 15px; margin-bottom: 25px;">
            在深圳，如果想寻觅一口最正宗的潮汕味道，陈鹏鹏总是绕不开的名字。
        </p>

        <div style="text-align: center; margin: 30px 0;">
            <img src="{image_url}" alt="陈鹏鹏潮汕菜盛宴" style="max-width: 100%; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.15);" />
            <p style="font-size: 13px; color: #888; margin-top: 10px;">📸 镜头记录下的潮汕美食盛宴</p>
        </div>

        <h2 style="font-size: 22px; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 40px;">🦢 镇店之宝：金牌卤鹅</h2>
        <p style="margin-bottom: 15px;">
            桌上最吸引眼球的莫过于那盘<strong>金牌卤鹅拼盘</strong>。选用正宗狮头鹅，经过秘制卤水经年累月的浸润，鹅肉紧致不柴，鹅皮肥而不腻。搭配那一抹爽口的酸梅汁和软糯的卤蛋、猪血，层次感在舌尖瞬间爆发。
        </p>

        <h2 style="font-size: 22px; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 40px;">🍲 暖心暖胃：砂锅海鲜粥</h2>
        <p style="margin-bottom: 15px;">
            那一锅乳白浓郁的<strong>砂锅粥</strong>，是潮汕人对食材新鲜度的最高致敬。粥底绵软，米粒分明却又入口即化，每一口都吸饱了海产的鲜甜。在微凉的夜晚，这一口温热最是抚慰人心。
        </p>

        <h2 style="font-size: 22px; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 40px;">🥢 卤味江湖：隆江猪脚与鱼饭</h2>
        <p style="margin-bottom: 15px;">
            别忘了那一盘红亮诱人的<strong>隆江猪脚</strong>，皮糯肉香，满满的胶原蛋白感。搭配潮汕特色的<strong>鱼饭</strong>（煎鱼），将咸鲜味发挥到了极致，这不仅是一顿饭，更是一场跨越地域的味觉旅行。
        </p>

        <div style="background-color: #fffbe6; padding: 20px; border-radius: 8px; border: 1px solid #ffe58f; margin-top: 40px;">
            <p style="margin: 0; color: #856404; font-weight: bold;">💡 小贴士：</p>
            <p style="margin-top: 5px; color: #856404;">陈鹏鹏的鹅肝也是一绝，入口即化的口感非常惊艳。建议饭点早点去，卤鹅最肥美的部位往往去得最快！</p>
        </div>

        <p style="text-align: right; color: #999; margin-top: 40px; font-style: italic;">—— 记录于 2026年2月5日 深圳</p>
    </div>
    """
    
    post = {
        'title': title,
        'description': body,
        'post_status': 'publish',
        'mt_keywords': ['美食', '深圳', '潮汕菜', '陈鹏鹏', '探店']
    }
    
    try:
        print("Creating rich post...")
        post_id = server.metaWeblog.newPost(0, username, password, post, True)
        return post_id
    except Exception as e:
        print(f"Error creating post: {e}")
        return None

if __name__ == "__main__":
    pid = create_rich_post()
    if pid:
        print(f"Post created successfully! ID: {pid}")
    else:
        print("Failed to create post.")
