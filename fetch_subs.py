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

all_lines = set()
ip_addresses = set()
protocols = {'vless': [], 'vmess': [], 'ss': [], 'trojan': [], 'other': []}


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
    except ValueError:
        return True


def is_valid_port(port):
    """Return True if port is an integer in [1, 65535]."""
    try:
        p = int(port)
        return 1 <= p <= 65535
    except (TypeError, ValueError):
        return False


def extract_host_and_port(config_line):
    """Return (host, port) tuple or (None, None) on failure."""
    try:
        if config_line.startswith("vmess://"):
            b64 = config_line[len("vmess://"):].strip()
            padded = b64 + "=" * (-len(b64) % 4)
            decoded = base64.b64decode(padded).decode()
            obj = json.loads(decoded)
            return obj.get("add"), obj.get("port")

        elif config_line.startswith(("vless://", "trojan://", "ss://")):
            parsed = urlparse(config_line)
            return parsed.hostname, parsed.port

    except Exception as e:
        print(f"Error extracting host/port: {e}")

    return None, None


def contains_ipv6(text):
    return bool(ipv6_pattern.search(text))


def fetch_url(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return url, response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return url, None


# Fetch all URLs concurrently
with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    results = [future.result() for future in as_completed(futures)]

# Process results
for url, text in results:
    if text is None:
        continue

    for line in text.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or contains_ipv6(line):
            continue

        # Extract raw IPv4s regardless of domain/port status
        for ip in ip_pattern.findall(line):
            if not is_blocked_ip(ip):
                ip_addresses.add(ip)

        host, port = extract_host_and_port(line)

        # Skip lines with invalid or missing ports
        if not is_valid_port(port):
            continue

        if host:
            if contains_ipv6(host) or is_blocked_domain(host):
                continue
            try:
                ip = ipaddress.ip_address(host)
                if is_blocked_ip(str(ip)):
                    continue
            except ValueError:
                pass

        all_lines.add(line)

# Categorize lines
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

# Save to output files
for proto, lines in protocols.items():
    with open(f"{proto}.txt", "w") as f:
        f.write("\n".join(lines) + "\n")

with open("combined.txt", "w") as f:
    for proto in ['vless', 'vmess', 'ss', 'trojan', 'other']:
        f.write("\n".join(protocols[proto]) + "\n")

with open("ip_addresses.txt", "w") as f:
    f.write("\n".join(sorted(ip_addresses)) + "\n")

print(f"✅ Extracted {len(ip_addresses)} unique IPv4 addresses.")
print(f"✅ Saved {sum(len(v) for v in protocols.values())} configs total.")
