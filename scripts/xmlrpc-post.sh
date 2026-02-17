#!/bin/bash
# XML-RPC Poster for WordPress
# Usage: ./xmlrpc-post.sh <title> <content_file> <categories>
# Env: WP_XMLRPC_URL, WP_USER, WP_PASS

if [ -z "$WP_XMLRPC_URL" ] || [ -z "$WP_USER" ] || [ -z "$WP_PASS" ]; then
  echo "Error: WP_XMLRPC_URL, WP_USER, and WP_PASS environment variables must be set."
  exit 1
fi

TITLE="$1"
CONTENT_FILE="$2"
CATEGORIES="$3"

if [ ! -f "$CONTENT_FILE" ]; then
  echo "Error: Content file $CONTENT_FILE not found."
  exit 1
fi

CONTENT=$(cat "$CONTENT_FILE")

# Construct XML payload
XML_PAYLOAD="<?xml version=\"1.0\"?>
<methodCall>
  <methodName>wp.newPost</methodName>
  <params>
    <param><value><int>1</int></value></param>
    <param><value><string>$WP_USER</string></value></param>
    <param><value><string>$WP_PASS</string></value></param>
    <param>
      <value>
        <struct>
          <member><name>post_title</name><value><string>$TITLE</string></value></member>
          <member><name>post_content</name><value><string><![CDATA[$CONTENT]]></string></value></member>
          <member><name>post_status</name><value><string>publish</string></value></member>
          <member><name>terms_names</name><value><struct><member><name>category</name><value><array><data><value><string>$CATEGORIES</string></value></data></array></value></member></struct></value></member>
        </struct>
      </value>
    </param>
  </params>
</methodCall>"

# Send request
curl -s -X POST -d "$XML_PAYLOAD" "$WP_XMLRPC_URL"

