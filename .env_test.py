import os
print(f"GOOGLE_API_KEY: {'set' if os.environ.get('GOOGLE_API_KEY') else 'not set'}")
print(f"WP_USER: {'set' if os.environ.get('WP_USER') else 'not set'}")
