# Сборка index.html (Telegram / GitHub Pages) и artifact.html + список для озвучки tts/list.txt
import datetime, hashlib, re, os
w = open('words.txt', encoding='utf-8').read().strip()
assert '`' not in w and '\\' not in w and '${' not in w
v = datetime.date.today().isoformat()
body = open('app.html', encoding='utf-8').read().replace('__WORDS__', w).replace('__VERSION__', v).replace('__CURSIVE__', open('cursive.json').read())
open('artifact.html', 'w', encoding='utf-8').write(body)
full = '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n'
open('index.html', 'w', encoding='utf-8').write(full)

# --- список для озвучки (тот же normHy, что в приложении) ---
def norm_hy(s):
    s = s.lower().replace('եւ', 'և')
    s = re.sub('[՛՞՜]', '', s)
    s = re.sub(r'[։՝,.!?:;«»"\'()\-–—]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()
fid = lambda key: hashlib.sha1(key.encode('utf-8')).hexdigest()[:12]
lines = ['# file|text|voice|id   (id "sample:N" = проба голосов; иначе id слова в приложении)']
for k, t in enumerate(open('tts/samples.txt', encoding='utf-8').read().strip().split('\n')):
    for voice in ('anahit', 'hayk'):
        lines.append(f'{fid("s:"+voice+":"+t)}|{t}|{voice}|sample:{k}')
if os.path.exists('tts/ALL_WORDS'):   # включается после одобрения голоса владельцем
    voice = open('tts/ALL_WORDS').read().strip() or 'anahit'
    seen = set()
    for line in w.split('\n'):
        hy = line.split('|')[0].split(';')[0].strip()
        key = norm_hy(hy)
        if key in seen: continue
        seen.add(key)
        lines.append(f'{fid("w:"+voice+":"+key)}|{hy}|{voice}|{key}')
open('tts/list.txt', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
