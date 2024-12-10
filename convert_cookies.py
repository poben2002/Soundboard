import json

def json_to_netscape(json_path, netscape_path):
    with open(json_path, 'r') as json_file:
        cookies = json.load(json_file)

    with open(netscape_path, 'w') as netscape_file:
        netscape_file.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            netscape_file.write(f"{cookie.get('domain', '')}\t"
                                f"{'TRUE' if cookie.get('hostOnly') is False else 'FALSE'}\t"
                                f"{cookie.get('path', '/')}\t"
                                f"{'TRUE' if cookie.get('secure') else 'FALSE'}\t"
                                f"{cookie.get('expirationDate', '0')}\t"
                                f"{cookie.get('name', '')}\t"
                                f"{cookie.get('value', '')}\n")

json_to_netscape('cookies.json', 'cookies_netscape.txt')
