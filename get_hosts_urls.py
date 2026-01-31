from urllib.parse import urlparse

INPUT_FILE = "Urls.txt"
OUTPUT_FILE = "hosts.txt"

hosts = set()

with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        try:
            parsed = urlparse(line)
            if parsed.netloc:
                hosts.add(parsed.netloc)
        except:
            pass

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for host in sorted(hosts):
        f.write(host + "\n")

print(f"Total unique hosts: {len(hosts)}")
print(f"Saved in: {OUTPUT_FILE}")
