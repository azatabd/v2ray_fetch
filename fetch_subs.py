import requests

urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/hosseincarmany/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/skywrt/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt"
]

# Sets to store unique lines by protocol
vless_lines = set()
vmess_lines = set()
ss_lines = set()
trojan_lines = set()
other_lines = set()

# Fetch and categorize
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        for line in lines:
            clean = line.strip()
            if not clean or clean.startswith("#"):
                continue
            if clean.startswith("vless://"):
                vless_lines.add(clean)
            elif clean.startswith("vmess://"):
                vmess_lines.add(clean)
            elif clean.startswith("ss://"):
                ss_lines.add(clean)
            elif clean.startswith("trojan://"):
                trojan_lines.add(clean)
            else:
                other_lines.add(clean)
    except Exception as e:
        print(f"Error fetching from {url}: {e}")

# Write separate files
def write_file(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(lines)))
    print(f"{filename} written ({len(lines)} lines).")

write_file("vless.txt", vless_lines)
write_file("vmess.txt", vmess_lines)
write_file("ss.txt", ss_lines)
write_file("trojan.txt", trojan_lines)
write_file("other.txt", other_lines)

# Create combined.txt in desired order
combined_lines = (
    sorted(vless_lines) +
    sorted(vmess_lines) +
    sorted(ss_lines) +
    sorted(trojan_lines) +
    sorted(other_lines)
)

write_file("combined.txt", combined_lines)
