import requests

urls = {
    "Sub1.txt": "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "All_Configs_Sub_Epodonios.txt": "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "All_Configs_Sub_Hossein.txt": "https://raw.githubusercontent.com/hosseincarmany/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "All_Configs_Sub_Nyein.txt": "https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/main/All_Configs_Sub.txt",
    "V2RAY_RAW.txt": "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "all_configs_SoliSpirit.txt": "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "All_Configs_Sub_Sky.txt": "https://raw.githubusercontent.com/skywrt/v2ray-configs/main/All_Configs_Sub.txt",
    "all_sub_Matin.txt": "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt"
}

for filename, url in urls.items():
    r = requests.get(url)
    if r.ok:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"Saved {filename}")
    else:
        print(f"Failed to fetch {url}")
