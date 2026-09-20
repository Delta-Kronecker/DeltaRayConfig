import urllib.request
import urllib.parse

urls = [
    "https://raw.githubusercontent.com/patterniha/Free-Configs/main/configs.tx",
    "https://github.com/Delta-Kronecker/DeltaRayConfig/raw/refs/heads/main/tested.tt",
]
out = "config.txt"

lines = []
for url in urls:
    try:
        with urllib.request.urlopen(url) as r:
            lines += r.read().decode("utf-8").splitlines()
    except Exception:
        pass

result = []
i = 1

for line in lines:
    line = line.strip()
    if not line.startswith(("vless://", "trojan://")):
        continue

    main, _, _ = line.partition("#")
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
    new += f"#{i}"

    result.append(new)
    i += 1

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
