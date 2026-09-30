"""Compare publicly hosted files to this checkout after GitHub Pages deployment."""
import hashlib
import os
from pathlib import Path
import subprocess
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = (ROOT / 'CNAME').read_text().strip()
COMMIT = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
FILES = ['index.html', 'styles.css', 'script.js', 'assets/interaction.svg',
         'assets/pridex.svg', 'assets/motion.svg', 'assets/tactile.svg',
         'assets/harbor.png', 'assets/favicon.svg']


def verify(scheme):
    base = f'{scheme}://{DOMAIN}/'
    for filename in FILES:
        route = '' if filename == 'index.html' else filename
        request = Request(f'{base}{route}?verification={COMMIT}',
                          headers={'User-Agent': 'Academic-homepage-deployment-check',
                                   'Cache-Control': 'no-cache'})
        with urlopen(request, timeout=20) as response:
            actual = response.read()
            expected = (ROOT / filename).read_bytes()
            if actual != expected:
                raise AssertionError(f'{filename}: hosted content differs from {COMMIT}')
            print(f'PASS {response.status} {response.url} '
                  f'sha256={hashlib.sha256(actual).hexdigest()}', flush=True)
    return base


# HTTPS is preferred; also test the HTTP URL used by the existing Pages setup.
# A TLS failure must be reported, never hidden by disabling certificate checks.
failures = {}
verified = {}
for attempt in range(1, 9):
    for scheme in ('https', 'http'):
        if scheme in verified:
            continue
        try:
            verified[scheme] = verify(scheme)
        except Exception as exc:
            failures[scheme] = f'{type(exc).__name__}: {exc}'
            print(f'Attempt {attempt}, {scheme}: {failures[scheme]}', flush=True)
    if len(verified) == 2:
        break
    if attempt < 8:
        time.sleep(15)

lines = [f'## Public deployment verification\n\nCommit: `{COMMIT}`\n']
for scheme in ('https', 'http'):
    if scheme in verified:
        lines.append(f'- PASS: {verified[scheme]} — all {len(FILES)} files exactly match the commit.')
    else:
        lines.append(f'- FAILED: {scheme}://{DOMAIN}/ — {failures.get(scheme)}')
summary = '\n'.join(lines) + '\n'
print(summary)
if os.environ.get('GITHUB_STEP_SUMMARY'):
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as report:
        report.write(summary)
if 'https' not in verified:
    raise SystemExit('HTTPS verification failed; see the summary for HTTP availability.')
