import concurrent.futures
import time
import urllib.error
import urllib.request

# Popüler Sosyal Medya, Yazılım ve İçerik Platformları
PLATFORMS = {
    # Popüler Sosyal Medya
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "X (Twitter)": "https://x.com/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Facebook": "https://www.facebook.com/{}",
    "Threads": "https://www.threads.net/@{}",
    "Telegram": "https://t.me/{}",
    "Reddit": "https://www.reddit.com/user/{}/about.json",
    # Yazılım & Geliştirici
    "GitHub": "https://api.github.com/users/{}",
    "DockerHub": "https://hub.docker.com/v2/users/{}",
    "Dev.to": "https://dev.to/{}",
    "GitLab": "https://gitlab.com/api/v4/users?username={}",
    "Replit": "https://replit.com/@{}",
    "Codechef": "https://www.codechef.com/users/{}",
    "Hackerrank": "https://www.hackerrank.com/{}",
    "PyPi": "https://pypi.org/user/{}/",
    # İçerik, Medya & Müzik
    "Spotify": "https://open.spotify.com/user/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch": "https://m.twitch.tv/{}",
    "Medium": "https://medium.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Tumblr": "https://{}.tumblr.com",
    # Oyun & Freelance
    "Steam": "https://steamcommunity.com/id/{}",
    "Chess.com": "https://api.chess.com/pub/player/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Behance": "https://www.behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Fiverr": "https://www.fiverr.com/{}",
}


def check_username(platform, url_template, username):
    url = url_template.format(username)

    # Tarayıcı taklidi yapan gelişmiş başlıklar
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=7) as response:
            if response.status == 200:
                # GitLab için özel kontrol (kullanıcı yoksa [] döner)
                if platform == "GitLab":
                    data = response.read().decode("utf-8")
                    if data == "[]":
                        return platform, False, url
                return platform, True, url
    except urllib.error.HTTPError as e:
        # 404/410 yanıtları profilin kesin olmadığını gösterir
        if e.code in [404, 410]:
            return platform, False, url
        else:
            return platform, None, f"HTTP Hata: {e.code} (Koruma/Engeller)"
    except Exception:
        return platform, None, "Zaman Aşımı / Bağlantı Sağlanamadı"

    return platform, False, url


def main():
    username = input("Taranacak Kullanıcı Adı: ").strip()
    if not username:
        print("[!] Lütfen geçerli bir kullanıcı adı girin.")
        return

    # Bekleme süresi (Saniye)
    wait_time = 7

    print(f"\n[*] '{username}' hedefi sisteme tanımlandı.")
    print("[*] Sistem hazırlanıyor, lütfen bekleyin...")

    # Canlı geri sayım
    for i in range(wait_time, 0, -1):
        print(f"\r", end="")
        time.sleep(1)

    print(
        "\n\n[+] Tarama başlatıldı! Platformlar kontrol ediliyor...\n"
        + "-" * 55
    )

    # Çoklu iş parçacığı çalıştırma
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(check_username, platform, url, username)
            for platform, url in PLATFORMS.items()
        ]

        for future in concurrent.futures.as_completed(futures):
            platform, found, url_or_msg = future.result()
            if found is True:
                print(f"[+] {platform:<15} : BULUNDU  -> {url_or_msg}")
            elif found is False:
                print(f"[-] {platform:<15} : Bulunamadı")
            else:
                print(f"[!] {platform:<15} : {url_or_msg}")

    print("-" * 55)
    print("[+] Tarama tamamlandı.")


if __name__ == "__main__":
    main()
