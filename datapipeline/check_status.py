import collections.abc
import collections
collections.Iterable = collections.abc.Iterable

from wordpress_xmlrpc import Client

from wordpress_xmlrpc.methods.posts import GetPosts

WP_URL = "https://microblocks0.wordpress.com/xmlrpc.php"
WP_USER = "davidturing"
WP_PASS = "d4oy t4ae zq6l kwe4"

client = Client(WP_URL, WP_USER, WP_PASS)
posts = client.call(GetPosts({'number': 100, 'post_status': 'publish'}))

print(f"{'ID':<5} {'Title':<50} {'Has Chinese?':<12} {'Length'}")
print("-" * 80)

missing = []
for p in posts:
    has_chinese = "实验原理" in p.content
    print(f"{p.id:<5} {p.title[:48]:<50} {str(has_chinese):<12} {len(p.content)}")
    if not has_chinese:
        missing.append(p.title)

print("\nMissing Chinese:")
print(missing)
