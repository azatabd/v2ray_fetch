# 🔗 V2Ray Configuration Files (Auto-Fetched)

This repository contains automatically fetched and processed V2Ray configuration subscriptions. The configurations are sorted by protocol types and are updated every 6 hours.

## 🚀 Auto-Updated Configuration Files

### 📥 Raw GitHub Links

- [VLESS Configs (raw)](https://raw.githubusercontent.com/azatabd/v2ray_fetch/main/vless.txt)
- [VMess Configs (raw)](https://raw.githubusercontent.com/azatabd/v2ray_fetch/main/vmess.txt)
- [Shadowsocks (SS) (raw)](https://raw.githubusercontent.com/azatabd/v2ray_fetch/main/ss.txt)
- [Trojan (raw)](https://raw.githubusercontent.com/azatabd/v2ray_fetch/main/trojan.txt)
- [Other Protocols (raw)](https://raw.githubusercontent.com/azatabd/v2ray_fetch/main/other.txt)
- [Combined (All in One) (raw)](https://raw.githubusercontent.com/azatabd/v2ray_fetch/main/combined.txt)

---

### 🌐 CDN Links via jsDelivr (Faster for Global Users)

- [VLESS Configs (CDN)](https://cdn.jsdelivr.net/gh/azatabd/v2ray_fetch@main/vless.txt)
- [VMess Configs (CDN)](https://cdn.jsdelivr.net/gh/azatabd/v2ray_fetch@main/vmess.txt)
- [Shadowsocks (SS) (CDN)](https://cdn.jsdelivr.net/gh/azatabd/v2ray_fetch@main/ss.txt)
- [Trojan (CDN)](https://cdn.jsdelivr.net/gh/azatabd/v2ray_fetch@main/trojan.txt)
- [Other Protocols (CDN)](https://cdn.jsdelivr.net/gh/azatabd/v2ray_fetch@main/other.txt)
- [Combined (All in One) (CDN)](https://cdn.jsdelivr.net/gh/azatabd/v2ray_fetch@main/combined.txt)

---
## Contents

- **combined.txt**: A combined list of all configuration subscriptions.
- **vless.txt**: Contains all VLESS protocol configurations.
- **vmess.txt**: Contains all VMESS protocol configurations.
- **ss.txt**: Contains all Shadowsocks (SS) protocol configurations.
- **trojan.txt**: Contains all Trojan protocol configurations.
- **other.txt**: Contains configurations for other protocols not categorized above.
- **ip_addresses.txt**: A list of all unique IP addresses extracted from the configurations.

## Configuration Files

The configuration files are fetched from the following public sources:

- [Barry Far V2Ray Configs](https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt)
- [Epodonios V2Ray Configs](https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt)
- [Hossein Carmany V2Ray Configs](https://raw.githubusercontent.com/hosseincarmany/v2ray-configs/main/All_Configs_Sub.txt)
- [Nyeinkokoaung404 V2Ray Configs](https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/main/All_Configs_Sub.txt)
- [Roosterkid Open Proxy List](https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt)
- [SoliSpirit V2Ray Configs](https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt)
- [Skywrt V2Ray Configs](https://raw.githubusercontent.com/skywrt/v2ray-configs/main/All_Configs_Sub.txt)
- [Matin Ghanbari V2Ray Configs](https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt)

The configurations are fetched, processed, and saved in different files based on their protocol type:
- **vless**: V2Ray VLESS protocol
- **vmess**: V2Ray VMESS protocol
- **ss**: Shadowsocks protocol
- **trojan**: Trojan protocol
- **other**: Any protocols that don't fall into the categories above

## IP Addresses Extraction

All unique IP addresses from the configuration files are extracted and saved in the `ip_addresses.txt` file.

### Example entry in `ip_addresses.txt`:

8.8.8.8

192.168.1.1

203.0.113.45

...

These IP addresses are collected from the configuration links to provide an additional resource for users to analyze the IPs available in the V2Ray configurations.

## Automatic Updates

This repository is automatically updated every 6 hours to fetch the latest configurations. The updates are triggered via a GitHub Action that pulls the latest configurations, processes them, and commits the updated files back to the repository.

## How to Use

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/v2ray_fetch.git
    cd v2ray_fetch
    ```

2. **Download the configuration files**:
    - All files are available in the repository and are automatically updated every 6 hours.
    - You can manually trigger an update by going to the **Actions** tab on GitHub and selecting "Run workflow."

3. **Access the files**:
    - After the files are fetched and updated, you can access the following files:
      - `combined.txt` (all configurations)
      - `vless.txt` (VLESS configurations)
      - `vmess.txt` (VMESS configurations)
      - `ss.txt` (Shadowsocks configurations)
      - `trojan.txt` (Trojan configurations)
      - `other.txt` (Other protocols)
      - `ip_addresses.txt` (List of IP addresses)

4. **Use the IP addresses**:
    - You can extract the IP addresses for further analysis or use them to configure your V2Ray client.

## Contributing

Feel free to fork this repository, contribute improvements, or suggest new configuration sources. Pull requests are welcome!

## License

This repository is licensed under the MIT License.

> 🛠️ This project is updated every 6 hours using GitHub Actions.  
> 🔁 Duplicates and comment lines are removed automatically.
