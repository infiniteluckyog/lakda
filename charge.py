from flask import Flask, request, Response
import requests
import urllib.parse

app = Flask(__name__)

VOIDAPI_KEY = "VDX-SHA2X-NZ0RS-O7HAM"

@app.route('/stripechk')
def stripechk():
    card = request.args.get("card", "")
    proxy_param = request.args.get("proxy")
    card = urllib.parse.unquote(card)
    if proxy_param:
        url = f"https://api.voidapi.xyz/v2/stripe_charge?key={VOIDAPI_KEY}&card={card}&proxy={proxy_param}"
    else:
        url = f"https://api.voidapi.xyz/v2/stripe_charge?key={VOIDAPI_KEY}&card={card}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        # Always return HTTP 200, even if VoidAPI returns 400!
        return Response(r.text, status=200, content_type="application/json")
    except Exception as e:
        return Response(
            '{"success": false, "error": "Relay server error: %s"}' % str(e),
            status=200,
            content_type="application/json"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
