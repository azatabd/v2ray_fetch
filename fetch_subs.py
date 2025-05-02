import requests
import re

# URLs to fetch configuration files from
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

# Set to collect unique lines
all_lines = set()
ip_addresses = set()

# Regex pattern to match IP addresses
ip_pattern = re.compile(r'((?:\d{1,3}\.){3}\d{1,3})')

for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.strip().splitlines()

        # Process each line
        for line in lines:
            if line.strip() and not line.strip().startswith("#"):
                all_lines.add(line.strip())

                # Search for IPs in the line
                match = ip_pattern.findall(line)
                for ip in match:
                    ip_addresses.add(ip)

    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Categorize lines into protocols
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

# Save all protocol files
with open("combined.txt", "w") as f:
    for group in ['vless', 'vmess', 'ss', 'trojan', 'other']:
        f.write("\n".join(protocols[group]) + "\n")

for proto, lines in protocols.items():
    with open(f"{proto}.txt", "w") as f:
        f.write("\n".join(lines) + "\n")

# Save IP addresses to ip_addresses.txt
with open("ip_addresses.txt", "w") as f:
    f.write("\n".join(sorted(ip_addresses)) + "\n")

print(f"Extracted {len(ip_addresses)} unique IP addresses.")
