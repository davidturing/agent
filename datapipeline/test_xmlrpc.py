import requests

user = "davidturing"
password = "d4oy t4ae zq6l kwe4"
url = "https://microblocks0.wordpress.com/xmlrpc.php"

title = "Connection Test XMLRPC"
content = "Testing XML-RPC connection."
categories = ["Uncategorized"]

xml_payload = f"""<?xml version="1.0"?>
<methodCall>
  <methodName>wp.newPost</methodName>
  <params>
    <param><value><int>1</int></value></param>
    <param><value><string>{user}</string></value></param>
    <param><value><string>{password}</string></value></param>
    <param>
      <value>
        <struct>
          <member><name>post_title</name><value><string>{title}</string></value></member>
          <member><name>post_content</name><value><string><![CDATA[{content}]]></string></value></member>
          <member><name>post_status</name><value><string>publish</string></value></member>
        </struct>
      </value>
    </param>
  </params>
</methodCall>"""

print(f"Testing XML-RPC to {url}...")
try:
    response = requests.post(url, data=xml_payload, headers={'Content-Type': 'text/xml'})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if "<int>" in response.text and "faultCode" not in response.text:
         print("SUCCESS: Post created via XML-RPC.")
    else:
         print("FAILED via XML-RPC.")
except Exception as e:
    print(f"ERROR: {e}")
