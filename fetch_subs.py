import requests
import re
import fnmatch
import base64
import json
from urllib.parse import urlparse
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/nyeinkokoaung404/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/V2RAY_RAW.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/thirtysixpw/v2ray-reaper/main/normal/mix",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt"
]

blocked_domains = {
    "applegrafix.com", "*.applegrafix.com", "*.ads.net", "*.ssvpnapp.win", "*.yangon.club",
    "*.varzesh360.co", "*.slashdevslashnetslashtun.net", "*.samanehha.co", "*.gym0boy.com",
    "*.xpmc.cc", "*.plebai.net", "*.zula.ir", "*.ucdavis.edu", "*.wlftest.xyz", "*.parsvds.ir",
    "*.webredirect.org", "*.cataba.ir", "*.iraniantim.ir", "*.soskom.ir", "*.hosting-ip.com",
    "*.cloudflare.com", "*.speedtest.net", "*.rahavard365.co", "*.theatlantic.com",
    "*.threea.org", "*.discord.cc", "*.abvpn.ru", "*.xiaomi-api.xyz", "*.felafel.org",
    "*.vpnbook.com", "*.turkiye6.xyz", "*.namasha.co", "*.webramz.co", "*.gosdk.xyz",
    "*.stark-industries.solutions", "*.test3.net", "*.bolab.net", "*.mjt000.com",
    "xcvg65.999815.xyz", "*.facai2024.com", "*.meiziba5566.com", "*.heduian.link", "*fly.dev",
    "*.sh-cloudflare.sbs", "*.irvideo.cfd", "*.lrzdx.uk", "*.mcloudservice.site",
    "*.v2ray.motorcycles", "*.comnpmjs.com", "huffingtonpost.es", "iranserver.com", "*.ddns.net",
    "*.cloudupdate.ir", "series-a2-mec.samanehha.co", "cdn-prouk.plusmusical2.ir",
    "cdn.netraidly.ru", "greb.loralden.com"
}

explicitly_blocked_ips = {"1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4", "127.0.0.1", "0.0.0.0"}

ip_pattern = re.compile(r'((?:\d{1,3}\.){3}\d{1,3})')
ipv6_pattern = re.compile(r'([a-fA-F0-9:]+:+)+[a-fA-F0-9]+')

protocols = {'vless': [], 'vmess': [], 'ss': [], 'trojan': [], 'other': []}

seen_identity = set()  # 🔥 NEW: (UUID, domain) dedup key


def is_blocked_domain(domain):
    if not domain:
        return False
    domain = domain.lower()
    return any(fnmatch.fnmatch(domain, pattern) for pattern in blocked_domains)


def is_blocked_ip(ip):
    try:
        if ip in explicitly_blocked_ips:
            return True
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.version == 6 or ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved
    except:
        return True


def is_valid_port(port):
    try:
        return 1 <= int(port) <= 65535
    except:
        return False


def extract_v2ray_identity(config_line):
    """
    returns (uuid, host)
    """
    try:
        if config_line.startswith("vmess://"):
            b64 = config_line[len("vmess://"):].strip()
            padded = b64 + "=" * (-len(b64) % 4)
            decoded = base64.b64decode(padded).decode()
            obj = json.loads(decoded)
            return obj.get("id"), obj.get("add")

        elif config_line.startswith(("vless://", "trojan://", "ss://")):
            parsed = urlparse(config_line)
            uuid = parsed.username
            host = parsed.hostname
            return uuid, host

    except:
        return None, None

    return None, None


def fetch_url(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return url, r.text
    except:
        return url, None


with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    results = list(executor.map(fetch_url, urls))


all_lines = []

for url, text in sorted(results, key=lambda x: x[0]):
    if not text:
        continue

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # extract identity key
        uuid, host = extract_v2ray_identity(line)

        if not uuid or not host:
            continue

        if is_blocked_domain(host):
            continue

        # 🔥 CORE DEDUP RULE: UUID + domain
        identity_key = (uuid, host)
        if identity_key in seen_identity:
            continue

        seen_identity.add(identity_key)
        all_lines.append(line)

        # classify
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


# write outputs
for proto in protocols:
    protocols[proto] = list(dict.fromkeys(protocols[proto]))

for proto, lines in protocols.items():
    with open(f"{proto}.txt", "w") as f:
        f.write("\n".join(lines) + "\n")

combined = []
seen = set()

for proto in ['vless', 'vmess', 'ss', 'trojan', 'other']:
    for line in protocols[proto]:
        if line not in seen:
            seen.add(line)
            combined.append(line)

with open("combined.txt", "w") as f:
    f.write("\n".join(combined) + "\n")

print(f"Saved {len(combined)} unique configs (UUID+domain dedup)")
