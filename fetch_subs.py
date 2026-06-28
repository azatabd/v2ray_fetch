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
    "cdn.netraidly.ru", "greb.loralden.com", "9sbisocj5c11.dxdx5.com", "a.pabloping.cloud",
    "abdzgg.teemazad.com", "acv-79.privetpack.site", "adf.ly", "afrcloud22.mmv.kr",
    "ahmad-ir.3patify.com", "alait.marzban-locations.com", "all.mdvpnsec.cfd",
    "all.tellmethetrue.shop", "all.v-2rayngvpn.cfd", "amir.ancvp.ancvpp.shop",
    "amo.amirnew.fun", "as.pink-perfect.ru", "atts5vkx96ec.dxdx5.com", "av.nexconnx.com",
    "avalpardakht.com", "axs.amirxshot.ir", "b.pabloping.cloud", "backend.xwhiteness.site",
    "belnn.appleseraj.ir", "benz.pmpads.com", "berovps.masoodbiranvand-230.workers.dev",
    "billowing-sunset-e340.qaraatayi.workers.dev", "bm.boulvarmoein.shop", "bm.xq-vpn.com",
    "byebye.safeconfig.ir", "bypass.ch-gt-01.com", "bypass.fr-gt-01.com", "bypass.uk-gthost-01.com",
    "c3.lunaparkmaku.ir", "c9v1mt2xe451.contigolibre.com", "camp.nahidapp.com", "cart.ankerios.ir",
    "cd4ul9u4hlil.fly.p7d.ir", "cdg-1.fromblancwithlove.com", "cdn.9889888.xyz", "cdn.cdnjst.org",
    "cdn.melodyshopone2.ir", "cdn.tzpro.xyz", "cdn7-09.vk-cdnvideo.com", "cdn7-39.vk-cdnvideo.com",
    "cdn9-33.vk-cdnvideo.com", "cdnjs.com", "cf.008500.xyz", "cf.090227.xyz", "cf.gafe-marz.ir", "cf.naixii.top",
    "cf.narton.ir", "cf1.466688.xyz", "cf10.466688.xyz", "cf2.466688.xyz", "cf3.466688.xyz", "cf4.466688.xyz",
    "cf5.466688.xyz", "cf6.466688.xyz", "cf7.466688.xyz", "cf8.466688.xyz", "cf9.466688.xyz",
    "cf-wkrs-pages-vless-aoy.pages.dev", "ch.viralforge.ru", "change.org", "chefox.kkkl.ir", "cherry-nll-01.live",
    "cl.digifile.pw", "clfconnect.pishipishi.pro", "cloudflare-dns.com", "cm.db-link.in", "creativecommons.org",
    "da.mfa.gov.ua", "da.mobileemdad.top", "damp-sound-f99c.golamirreza19954312.workers.dev", "dash.getasa.ir",
    "dd.openaccessnode.com", "de.kaia.pw", "de.ko.prod.n7.homes", "de.pink-perfect.ru", "de.vpnbase.net",
    "de-1.coinbridge.nl", "de1.gamelistak.com", "de-15.ipsum.sbs", "de2.socifiles.com", "de-3.coinbridge.nl",
    "de-dp-01.com", "deu196.unboundaccess.org", "dey.lnmarketplace.net", "digitalocean.com", "dns8.nufilter.store",
    "dnss.iraniranshopdashnoard.ir", "dqf21.sdssd1.sadqwdw1.carvan1.mimkiscx.ir", "du1.gamelistak.com", "edge.aiteamplus.ir",
    "ee.janusgate.org", "eng14.netliberated.org", "ercf-ma.rainzone.site", "ert-4.v-sub.site", "euro.cloud-play.ir",
    "eventx.faraservice.space", "everyday-vpn.telegram-channel", "ez-421a72.mohamadfarajian09144538950.workers.dev",
    "ez-e989d9.ezaccess104f94a.workers.dev", "f.mobilemarketahora.top", "f1.springpaatogh8.store", "f2.springpaatogh8.store",
    "fast1.mrsf.ir", "fastly1.yasharmobile.com", "fearless-change.oneeat.co", "fi.faygo.bot", "fi.janusgate.org", "fire.jykvpn.com",
    "fit.jojack.ru", "five.nothingnewtodo.online", "fl.gamelistak.com", "fl.v2online3.site", "fn2-unlimited.q09.ir", "ford.pmpads.com",
    "fr.connfull.org", "fr.pink-perfect.ru", "france.cloudpath.live", "free.miladiran1.shop", "freeiran-opiran-2.shaygan.site",
    "freesocks.work", "freetg.strettenvpn.com", "freev2ray.v2ray4.xyz", "fr-tx.sbrf-cdn342.ru", "fx3033.game2lizard.com",
    "ge.it-programer.ir", "germanubhf.dadashinet10.ir", "germanyjkjklj.dadashinet10.ir", "germany-vip.soft26.ir",
    "germnode.dostupnet.ru", "gifi.dns-crypto-yandex.com", "gift.nazincup.ir", "gkgjfjeifidjejfj.fars-daxter.ir",
    "global.cloud-play.ir", "godaddy.com", "goto.antimelinet.click", "grif.dns-crypto-yandex.com", "h3.capigodserv.ir",
    "handsome-device.oneeat.co", "hcaptcha.com", "hes.purplrose.ir", "hfhh.hshsh7261.workers.dev", "hinet2.gzcloud.shop",
    "hybrid.arvancloud.online", "i.badboys.gq", "i25.myfreessl.top", "id.artunnel57.host", "ip", "ip.shakhle.ir",
    "ip.yasharteam.com", "ip2.neoservers.ir", "ipadvpn.dpdns.org", "ipbaz.ping-box.com", "ips.it.mobileemdad.top",
    "ips.list.nonpath.ir", "ipw.gfdv54cvghhgfhgj-njhgj64.info", "ipw.ygdfw.com", "ir.fxgoldensignals.com", "itarmy.com.ua",
    "join-masterserver.lehefe6790.workers.dev", "k6.capigodserv.ir", "kaliconnect-starpanel-vip6.up.railway.app",
    "kam.kamo-bish.ir", "karandish.mahkocholo.com", "kz.accesspoints.cloakify.app", "l4.l-itx.info", "late-wood-c116.vahshi2000.workers.dev",
    "liad.maf-tahas.ir", "ll0ll.vip", "lobgfvdas.dadashinet10.ir", "local.cloud-play.ir", "lv.faygo.bot",
    "m33a.vip784.com", "m7a.vip784.com", "magazine.sentry-warrunner.xyz", "mail.erwinhoda.shop", "main.danlodino.ir",
    "mci.cloud-play.ir", "mci.ircf.space", "mci.tahermollaei.pw", "medium.com", "melo-mtn.outline-vpn.cloud",
    "mmdu-production.up.railway.app", "morphinn.gheychi.me", "mtn.anahid.beauty", "mv2.amydoodles.com", "myip.check.nonpath.ir",
    "my-pp.arminpixel2.workers.dev", "namedkenzo-senzo.hf.space", "nameless-moon-7c4d.shafmrhjlos23.workers.dev",
    "narrow-passenger.oneeat.co", "netraidly.ru", "neymar.ariyant.ir", "nimbaha.yousefbn.com.turkcloud.ir", "nl-1.coinbridge.nl",
    "nl2.gamelistak.com", "nl3.gamelistak.com", "nodc.bazarkha.sbs", "nova-mango-vault-2e63.wolf-fbi-red.workers.dev",
    "npmjs.com", "nuclear.us.kg", "o6.lunaboutiqu.ir", "octopusss5.info", "om.mastermarly.ir", "online.4zkaban.xyz",
    "onnevpn.dibaux.ir", "osre3.jykvpn.com", "out.newlinemobile.xyz", "ov2.liiliil.ir", "ov-canada1.09vpn.com",
    "ov-france1.09vpn.com", "ov-france2.09vpn.com", "ov-germany1.09vpn.com", "ovhwuxian.pai50288.uk", "ov-italy1.09vpn.com",
    "p4.capigodserv.ir", "panel.dibaux.ir", "pc.amirxshot.ir", "pl.boxypn.com", "pl.healthy-connected.com", "pl.nitroo-tech.ru",
    "pl.viralforge.ru", "poli.appleseraj.ir", "poom.hardvezoo.ir", "pqh27v4.waipdirect.shop", "pqh30v8.waipdirect.shop",
    "profile.netraidly.ru", "psc-1.zdshop.ir", "psf-1.zdshop.ir", "public18v7.fastipsport.com", "python-graysongon.wasmer.app",
    "railway-production-b185.up.railway.app", "red.nahidapp.com", "rez5.royalro.shop", "rezerv.yunus.guru", "rezerv20.yunus.guru",
    "rezerv3.yunus.guru", "rezerv4.yunus.guru", "rezerv5.yunus.guru", "rezerv6.yunus.guru", "riga-1.easyodin.ir", "riga1.ns.asriranfun.ir",
    "root.configforvpn.fun", "rose5.lhpuniversity.online", "rshirt.lordmakuboutiqu.site", "ru.faygo.bot", "ru01.goodmaximum.com",
    "rvg-production-1ab7.up.railway.app", "rvg-production-6b96.up.railway.app", "rvg-production-7fb9.up.railway.app",
    "rvg-production-b337.up.railway.app", "rvg-production-cdb5.up.railway.app", "s10.digitalcity9.sbs", "s2.skullvpn.xyz",
    "s356.nba203.sbs", "s5.fastspeeds.ir", "sabz8.sabztarash.ir", "sam.amirgod.top", "sca10.myfymain.com", "sca11.myfymain.com",
    "sca11.speedmeter.shop", "sca12.myfymain.com", "sca13.myfymain.com", "sca14.myfymain.com", "sca15.myfymain.com", "sca16.myfymain.com",
    "sca17.myfymain.com", "sca18.myfymain.com", "sca20.myfymain.com", "sca21.myfymain.com", "sca22.myfymain.com", "sca23.myfymain.com",
    "sca25.speedmeter.shop", "sca26.myfymain.com", "sca29.myfymain.com", "sca29.speedmeter.shop", "sca30.mysilipdir.com", "sca31.myfymain.com",
    "sca33.myfymain.com", "sca33.speedmeter.shop", "sca34.mysilipdir.com", "sca35.myfymain.com", "sca35.speedmeter.shop", "sca37.myfymain.com",
    "sca8.myfymain.com", "sca9.myfymain.com", "sc-thenetherlands1.09vpn.com", "sc-thenetherlands2.09vpn.com", "se.faygo.bot",
    "securitytrails.com", "server3.pegibol940.workers.dev", "set.api-tel.xyz", "shhproxy.varzesh3-cnd.site", "silver.api-tel.xyz",
    "sk.abadanvpn.host", "sky2.hupcloud.com", "snapp.ir", "sosooos.turbo2v.top", "sourceforge.net", "spd-mynames.global.ssl.fastly.net",
    "speedtest.net", "sr13.dmitri.sbs", "ss.ll0ll.vip", "ssl.hostirann.xyz", "static.lotussec.com", "sub.shadowsokstes.workers.dev",
    "subgift-production-aeb1.up.railway.app", "support.fastcmd.top", "sv2.azparadox.ir", "sv3.tsteam99.top", "svg-2.onrender.com",
    "svn.yasharmobile.com", "sw.pink-perfect.ru", "sw-2.coinbridge.nl", "swed.oplatasite.ru", "sweet-combination.seotoolsforyou.co.uk",
    "sweet-night-d458.panelgfw3.workers.dev", "switzerland.boot-lee.ru", "sy2.syragame.com", "tabrizm138.lll.l0l.lll.workers.dev",
    "tamam-1.conf-tun.site", "tg.riotvpn.eu", "tgju.org", "tmesubgift.onrender.com", "tmesubgift.up.railway.app", "t-panel.wasmer.app",
    "tr.dtgitar.com", "tr.janusgate.org", "turk.izumii.ir", "tw3.miyazono-kaori.com", "uk-gthost-01.com", "undef.network", "us.janusgate.org",
    "usa.viralforge.ru", "usa-join.outline-vpn.fun", "usamd.ptuu.gq", "v.abolfazlsafeti.top", "v1.vpn1016.ru", "v2tr.imesaagetext.ir",
    "v2tr.topacp.store", "varzesh3.com", "velsanto.online", "vip-76.f-sub.cfd", "vip-80.f-sub.cfd", "vip-81.f-sub.cfd", "vpn.oplatasite.ru",
    "vpnv1.aspidnet.xyz", "vtodkcdisnc.fars-daxter.ir", "wandering-mode-754c.pashashams99.workers.dev", "web.biatochannelv271g.shop",
    "web-production-3e200.up.railway.app", "wstg.datasynctrue.online", "ww.sansorchi.net", "www.baipiao.eu.org", "www.cnae.top", "www.gcore.com",
    "www.hcaptcha.com", "www.paypal.com", "www.tgju.org", "x.fl.vpnpplvpn.top", "xcdn.accuracycloud.ir", "xn-ip1.dbssl.ir", "yandex.plan-vpn.ru",
    "youxuan.cf.090227.xyz", "zeus-panel-2vxg7a.kingworkerpeekconfig.workers.dev", "zeus-panel-2x50i7.zeus-z3vu4r.workers.dev",
    "zeus-panel-7gtag4.kingworker11228peekconfig.workers.dev", "zeus-panel-ehqukv.ewrw34634532.workers.dev", "zeus-panel-hrffzx.zeus-63ob04.workers.dev",
    "zeus-panel-idoxmd.zeus-ptqez6.workers.dev", "zeus-panel-tln7ap.kingworkerr.workers.dev", "zeus-panel-y7oul5.zeus-gjioyx.workers.dev",
    "zeus-panel-zfc5oc.kingworker121212.workers.dev", "zone.tr1.netlume.ir", "zula.ir"
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
