import os
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from dotenv import load_dotenv

# Load env
load_dotenv()

WP_USER = os.getenv("WORDPRESS_USERNAME") or "davidturing"
WP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

def publish_blog():
    try:
        print("Connecting to WordPress...")
        client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    title = "推荐系统公平性研究现状与低活跃用户优化策略"
    
    # 构建博客内容
    content = """
    <h2>03. 国内外研究现状：推荐系统公平性</h2>
    
    <p>随着推荐系统在信息分发中的核心地位日益稳固，其算法的<strong>公平性（Fairness）</strong>问题也逐渐成为学术界和工业界关注的焦点。基于最新的研究综述（Li et al., 2023），我们对当前的国内外研究现状进行了梳理，特别是针对<strong>低活跃用户</strong>的公平性问题。</p>

    <h3>1. 研究框架与理论基础</h3>
    <p>推荐系统的公平性研究已经形成了一套相对完整的框架。Li等人（2023）对公平性的定义、优化方法及评测数据集进行了系统综述。研究指出，推荐场景具有交互性强、目标多样以及影响长期用户行为等特点，这使得公平性问题比传统分类或排序任务更为复杂。</p>

    <h3>2. 核心痛点：低活跃用户的不公平性</h3>
    <p>主流推荐算法在不同用户群体上的表现存在显著差异。Li等人（2021）从<strong>用户活跃度</strong>的角度进行了深入分析：</p>
    <ul>
        <li><strong>高活跃用户</strong>：虽然在数据总量中占比相对较小，但算法能够捕捉到足够的信息，从而提供高质量的推荐。</li>
        <li><strong>低活跃用户</strong>：作为系统中的<strong>多数群体</strong>，由于交互数据稀疏，长期处于推荐质量较差的“不利地位”。</li>
    </ul>
    <p>这种“贫者越贫”的现象是当前推荐系统亟待解决的重点问题。</p>

    <h3>3. 主流优化策略</h3>
    
    <h4>A. 重排序策略 (Re-ranking)</h4>
    <p>这是目前工业界应用最广泛的方法之一。其核心思想是在模型输出初步排序结果后，在最终展示给用户之前，通过引入公平性约束进行重新排序。</p>
    <p><strong>Geyik等人 (2019)</strong> 提出了公平感知排序框架，通过设定目标分布来控制不同群体的曝光比例，确保各类群体（如不同性别、种族或活跃度）获得合理的展示机会。</p>

    <h4>B. 多目标优化</h4>
    <p><strong>甘尧瑞等人</strong>提出了双边公平推荐模型，旨在兼顾“用户侧”体验与“项目侧”曝光公平性，通过排序一致性约束缓解了为了提升群体公平而导致的个体公平损失。</p>

    <h4>C. 隐私保护方案</h4>
    <p>针对敏感属性泄露问题，<strong>龚镇辉等人</strong>提出了敏感属性无关的大语言模型公平推荐框架，在无需显式获取用户敏感属性的情况下，有效缩小了群体间的推荐差距。</p>

    <h3>4. 算法实现示例：公平感知重排序 (Fairness Re-ranking)</h3>
    <p>针对提到的“重排序策略”，以下是一个简化的算法代码片段，展示了如何通过插值法（Interpolation）在保持推荐质量的同时提升公平性。</p>

    <pre><code class="language-python">
def fair_reranking(recommended_items, sensitive_groups, target_ratio=0.5, k=10):
    \"\"\"
    简化的公平性重排序算法示例
    
    Args:
        recommended_items: 原始推荐列表 (List of Item objects with score)
        sensitive_groups: 物品所属的敏感组别映射 (Dict: item_id -> group_id)
        target_ratio: 目标群体的期望占比 (例如: 保护群体至少占 50%)
        k: 最终推荐列表长度
    
    Returns:
        reranked_list: 重排序后的列表
    \"\"\"
    reranked_list = []
    
    # 将物品分为受保护组(Protected)和非受保护组(Non-Protected)
    protected_queue = [i for i in recommended_items if sensitive_groups[i.id] == 'protected']
    non_protected_queue = [i for i in recommended_items if sensitive_groups[i.id] == 'non_protected']
    
    # 按照原始分数排序
    protected_queue.sort(key=lambda x: x.score, reverse=True)
    non_protected_queue.sort(key=lambda x: x.score, reverse=True)
    
    protected_count = 0
    
    for i in range(k):
        # 计算当前受保护组的比例
        current_ratio = protected_count / (i + 1)
        
        # 如果比例不足，且还有受保护物品，优先插入受保护物品
        if current_ratio < target_ratio and protected_queue:
            item = protected_queue.pop(0)
            protected_count += 1
        # 否则，按照分数高低选择（通常选非受保护组中分高的，或者两组中分最高的）
        elif non_protected_queue:
             # 简单策略：如果不需要强制插入保护组，就看谁分数高
             if protected_queue and protected_queue[0].score > non_protected_queue[0].score:
                 item = protected_queue.pop(0)
                 protected_count += 1
             else:
                 item = non_protected_queue.pop(0)
        elif protected_queue:
             item = protected_queue.pop(0)
             protected_count += 1
        else:
            break # 没有物品了
            
        reranked_list.append(item)
        
    return reranked_list
    </code></pre>

    <h3>5. 总结</h3>
    <p>尽管现有研究在公平性建模上取得了进展，但仍面临<strong>对敏感属性依赖强</strong>和<strong>模型结构复杂</strong>的挑战。未来的研究趋势，特别是针对<strong>低活跃用户</strong>，更倾向于在排序阶段通过轻量级的<strong>公平重排序策略</strong>来实现质量调节，这在兼顾公平性与系统性能方面具有极高的现实意义。</p>
    """

    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = 'publish'
    post.terms_names = {
        'category': ['AI Research', 'Recommendation Systems'],
        'post_tag': ['Fairness', 'Algorithm', 'Re-ranking', 'Research']
    }

    try:
        print(f"Publishing blog: {title}...")
        post_id = client.call(posts.NewPost(post))
        print(f"SUCCESS: Blog published! Link: {WP_URL}/?p={post_id}")
    except Exception as e:
        print(f"Publish Failed: {e}")

if __name__ == "__main__":
    publish_blog()
