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

all_lines = []

for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()
        filtered_lines = [line for line in lines if not line.strip().startswith("#")]
        all_lines.extend(filtered_lines)
    except Exception as e:
        print(f"Failed to fetch from {url}: {e}")

with open("combined.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_lines))

print("combined.txt updated successfully.")
