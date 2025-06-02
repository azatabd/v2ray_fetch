import requests
import re
import fnmatch
import base64
import json
from urllib.parse import urlparse
import ipaddress

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

# Wildcard patterns for blocked domains
blocked_domains = [
    "applegrafix.com",
    "*.applegrafix.com",
    "*.ads.net",
]

# Regex to match IPv4 addresses
ip_pattern = re.compile(r'((?:\d{1,3}\.){3}\d{1,3})')

# Set to store unique config lines and IPs
all_lines = set()
ip_addresses = set()

# Categorized configs
protocols = {
    'vless': [],
    'vmess': [],
    'ss': [],
    'trojan': [],
    'other': []
}

def is_blocked_domain(domain):
    if not domain:
        return False
    domain = domain.lower()
    for pattern in blocked_domains:
        if fnmatch.fnmatch(domain, pattern):
            return True
    return False

def is_blocked_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.version == 6:
            return True
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return True
    except ValueError:
        return True  # Malformed IPs are treated as blocked
    return False

def extract_host(config_line):
    try:
        if config_line.startswith("vmess://"):
            b64 = config_line[len("vmess://"):].strip()
            padded = b64 + "=" * (-len(b64) % 4)
            decoded = base64.b64decode(padded).decode()
            obj = json.loads(decoded)
            return obj.get("add")
        elif config_line.startswith(("vless://", "trojan://", "ss://")):
            parsed = urlparse(config_line)
            return parsed.hostname
    except Exception as e:
        print(f"Error extracting domain: {e}")
    return None

def contains_ipv6(text):
    ipv6_pattern = re.compile(r'([a-fA-F0-9:]+:+)+[a-fA-F0-9]+')
    return bool(ipv6_pattern.search(text))

# Process all URLs
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.strip().splitlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if contains_ipv6(line):
                continue  # Skip configs with IPv6

            host = extract_host(line)
            if host:
                if contains_ipv6(host):
                    continue
                if is_blocked_domain(host):
                    continue
                try:
                    ip = ipaddress.ip_address(host)
                    if is_blocked_ip(str(ip)):
                        continue
                except ValueError:
                    pass  # Host is not an IP, it's a domain

            # Add to unique lines
            all_lines.add(line)

            # Extract valid IPs
            for ip in ip_pattern.findall(line):
                if not is_blocked_ip(ip):
                    ip_addresses.add(ip)

    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Categorize by protocol
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

# Save all configs
with open("combined.txt", "w") as f:
    for group in ['vless', 'vmess', 'ss', 'trojan', 'other']:
        f.write("\n".join(protocols[group]) + "\n")

# Save per-protocol files
for proto, lines in protocols.items():
    with open(f"{proto}.txt", "w") as f:
        f.write("\n".join(lines) + "\n")

# Save public IPv4s
with open("ip_addresses.txt", "w") as f:
    f.write("\n".join(sorted(ip_addresses)) + "\n")

print(f"Extracted {len(ip_addresses)} unique IPv4 addresses.")
