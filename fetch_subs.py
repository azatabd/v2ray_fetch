import requests

urls = {
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/hosseincarmany/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/skywrt/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt"
}

combined_data = ""

for url in urls:
    try:
        r = requests.get(url, timeout=10)
        if r.ok:
            content = r.text.strip()
            combined_data += content + "\n"
            print(f"Fetched: {url}")
        else:
            print(f"Failed to fetch: {url}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

with open("combined.txt", "w", encoding="utf-8") as f:
    f.write(combined_data.strip())

print("Saved combined.txt")
