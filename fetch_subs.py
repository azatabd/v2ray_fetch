import requests

urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/hosseincarmany/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/skywrt/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt"
]

all_lines = set()

for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.strip().splitlines()
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                all_lines.add(line.strip())
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Categorize lines
protocols = {
    'vless': [],
    'vmess': [],
    'ss': [],
    'trojan': [],
    'other': []
}

for line in sorted(all_lines):
    if line.startswith("vless://"):
        protocols['vless'].append(line)
    elif line.startswith("vmess://"):
        protocols['vmess'].append(line)
    elif line.startswith("ss://"):
        protocols['ss'].append(line)
    elif line.startswith("trojan://"):
        protocols['trojan'].append(line)
    else:
        protocols['other'].append(line)

# Save all files
with open("combined.txt", "w") as f:
    for group in ['vless', 'vmess', 'ss', 'trojan', 'other']:
        f.write("\n".join(protocols[group]) + "\n")

for proto, lines in protocols.items():
    with open(f"{proto}.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
