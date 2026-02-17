import os
import sys
import subprocess

def run():
    title = "佳能 RF 全家桶实战：从扫街到打鸟的参数进阶"
    content_file = "blog_content.html"
    category = "Photography Education"
    
    # Check if variables are available
    url = os.environ.get("WP_XMLRPC_URL", "https://dvcamera6.wordpress.com/xmlrpc.php")
    user = os.environ.get("WP_USER")
    passwd = os.environ.get("WP_PASS")
    
    if not user or not passwd:
        print("Error: WP_USER or WP_PASS not set in environment.")
        return False
        
    cmd = ["bash", "scripts/xmlrpc-post.sh", title, content_file, category]
    env = os.environ.copy()
    env["WP_XMLRPC_URL"] = url
    
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    return result.returncode == 0

run()
