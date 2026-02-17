from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies
import os
from dotenv import load_dotenv

load_dotenv()

WP_USER = "davidturing"
WP_PASSWORD = os.getenv("wordpress_app_password_for_dvspace5") or os.getenv("WORDPRESS_APP_PASSWORD")
WP_URL = os.getenv("WORDPRESS_URL", "https://dvspace5.wordpress.com")
XMLRPC_ENDPOINT = f"{WP_URL.rstrip('/')}/xmlrpc.php"

client = Client(XMLRPC_ENDPOINT, WP_USER, WP_PASSWORD)
terms = client.call(taxonomies.GetTerms('category'))
for t in terms:
    print(f"ID: {t.id} - Name: {t.name} - Slug: {t.slug}")
