import urllib.request
import urllib.parse

urls = [
    "https://raw.githubusercontent.com/patterniha/Free-Configs/main/configs.tt",
    "https://github.com/Delta-Kronecker/V2ray-Config/raw/refs/heads/main/config/patt/all.txt", 
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

    if not query:
        continue

    params = urllib.parse.parse_qsl(query, keep_blank_values=True)
    d = dict(params)
    if d.get("security") != "tls":
        continue

    new_params = []
    for k, v in params:
        if k == "fp":
            new_params.append((k, "chrome"))
        else:
            new_params.append((k, v))

    if "fp" not in d:
        new_params.append(("fp", "chrome"))

    new_query = urllib.parse.urlencode(new_params)

    new = f"{proto}://{user}@127.0.0.1:40443?{new_query}"
    new += f"#{i}"

    result.append(new)
    i += 1

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(result))
