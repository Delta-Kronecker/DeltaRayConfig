import urllib.request
import urllib.parse

url = "https://raw.githubusercontent.com/patterniha/Free-Configs/main/configs.txt"
out = "config.txt"

with urllib.request.urlopen(url) as r:
    content = r.read().decode("utf-8")

result = []

for line in content.splitlines():
    line = line.strip()
    if not line.startswith(("vless://", "trojan://")):
        continue

    main, _, tag = line.partition("#")
    proto, _, rest = main.partition("://")
    user, _, hp = rest.partition("@")
    _, _, query = hp.partition("?")

    if query:
        params = urllib.parse.parse_qsl(query, keep_blank_values=True)
        params = [(k, v) for k, v in params if k not in ("cs", "fm")]
        query = urllib.parse.urlencode(params)

    new = f"{proto}://{user}@127.0.0.1:40443"
    if query:
        new += f"?{query}"
    if tag:
        new += f"#{tag}"

    result.append(new)

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
