import csv
import socket
import time
import sys
from pathlib import Path

try:
    import requests
except Exception:
    requests = None

try:
    import socks as pysocks
except Exception:
    pysocks = None

INPUT = Path(__file__).parent / 'proxies.csv'
OUTPUT = Path(__file__).parent / 'proxies_tested.csv'

TCP_TIMEOUT = 5.0
HTTP_TIMEOUT = 10.0

def tcp_check(host, port, timeout=TCP_TIMEOUT):
    start = time.time()
    try:
        sock = socket.create_connection((host, int(port)), timeout=timeout)
        sock.close()
        return True, int((time.time()-start)*1000)
    except Exception as e:
        return False, None


def http_probe(proxy_url):
    if requests is None:
        return False, None, 'requests not installed'
    start = time.time()
    try:
        resp = requests.get('http://httpbin.org/ip', proxies={'http': proxy_url, 'https': proxy_url}, timeout=HTTP_TIMEOUT)
        ok = resp.status_code == 200
        latency = int((time.time()-start)*1000)
        return ok, latency, None if ok else f'status {resp.status_code}'
    except Exception as e:
        return False, None, str(e)


def test_proxy(row):
    # row is a dict with keys including ip and port and protocols
    ip = row.get('ip')
    port = row.get('port')
    protocols = row.get('protocols','').lower()
    result = {
        'ip': ip,
        'port': port,
        'protocols': protocols,
        'tcp_open': False,
        'tcp_latency_ms': '',
        'http_ok': '',
        'http_latency_ms': '',
        'error': ''
    }

    if not ip or not port:
        result['error'] = 'missing ip/port'
        return result

    ok, lat = tcp_check(ip, port)
    result['tcp_open'] = ok
    result['tcp_latency_ms'] = lat if lat is not None else ''

    # Try a higher-level check for HTTP/SOCKS if requests (and pysocks for socks) present
    if ok:
        # prefer to try an HTTP request via proxy if we can
        proxy_url = None
        if 'http' in protocols:
            proxy_url = f'http://{ip}:{port}'
        elif 'socks5' in protocols or 'socks4' in protocols or 'socks' in protocols:
            scheme = 'socks5' if 'socks5' in protocols else ('socks4' if 'socks4' in protocols else 'socks5')
            proxy_url = f'{scheme}://{ip}:{port}'

        if proxy_url and requests:
            ok2, lat2, err = http_probe(proxy_url)
            result['http_ok'] = ok2
            result['http_latency_ms'] = lat2 if lat2 is not None else ''
            if err:
                result['error'] = err
        else:
            if proxy_url and not requests:
                result['error'] = 'requests not installed; only TCP check done'
            else:
                result['error'] = 'no usable protocol parsed; only TCP check done'

    return result


def main():
    if not INPUT.exists():
        print('Input proxies.csv not found at', INPUT)
        sys.exit(1)

    rows = []
    with open(INPUT, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    print(f'Read {len(rows)} proxies from {INPUT}')

    results = []
    for i, r in enumerate(rows, start=1):
        print(f'[{i}/{len(rows)}] Testing {r.get("ip")}:{r.get("port")} ({r.get("protocols")})')
        res = test_proxy(r)
        print('  ->', res['tcp_open'], 'tcp_ms=', res['tcp_latency_ms'], 'http_ok=', res['http_ok'], 'err=', res['error'])
        results.append({**r, **res})

    # write output CSV
    fieldnames = list(results[0].keys()) if results else []
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print('\nResults written to', OUTPUT)

if __name__ == '__main__':
    main()
