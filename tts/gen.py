# Озвучка через Azure Speech (голоса hy-AM-AnahitNeural / hy-AM-HaykNeural).
# Ключ и регион берутся из секретов репозитория AZURE_SPEECH_KEY и AZURE_SPEECH_REGION.
import os, sys, json, time, urllib.request, urllib.error
from xml.sax.saxutils import escape
KEY, REGION = os.environ.get('AZURE_SPEECH_KEY'), os.environ.get('AZURE_SPEECH_REGION')
VOICES = {'anahit': 'hy-AM-AnahitNeural', 'hayk': 'hy-AM-HaykNeural'}
os.makedirs('audio', exist_ok=True)
rows = []
for line in open('tts/list.txt', encoding='utf-8'):
    line = line.strip()
    if line and not line.startswith('#'): rows.append(line.split('|'))
missing = [r for r in rows if not os.path.exists(f'audio/{r[0]}.mp3')]
print(f'{len(rows)} в списке, нужно озвучить {len(missing)}')
if missing and not (KEY and REGION):
    print('Нет секретов AZURE_SPEECH_KEY / AZURE_SPEECH_REGION — озвучка пропущена'); missing = []
url = f'https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1'
for f, text, voice, _id in missing:
    ssml = f"<speak version='1.0' xml:lang='hy-AM'><voice name='{VOICES[voice]}'><prosody rate='-8%'>{escape(text)}</prosody></voice></speak>"
    req = urllib.request.Request(url, data=ssml.encode('utf-8'), method='POST', headers={
        'Ocp-Apim-Subscription-Key': KEY, 'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3', 'User-Agent': 'barer-tts'})
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(req, timeout=30).read()
            open(f'audio/{f}.mp3', 'wb').write(data); break
        except urllib.error.HTTPError as e:
            print('HTTP', e.code, f, e.read()[:200]); time.sleep(2 + attempt*3)
            if e.code in (401, 403): sys.exit('Ключ Azure не подошёл')
    time.sleep(0.15)
# манифест для приложения
ids, samples = {}, {}
for f, text, voice, _id in rows:
    if not os.path.exists(f'audio/{f}.mp3'): continue
    if _id.startswith('sample:'): samples.setdefault(_id, {'text': text, 'files': {}})['files'][voice] = f + '.mp3'
    else: ids[_id] = f + '.mp3'
json.dump({'ids': ids, 'samples': [samples[k] for k in sorted(samples, key=lambda x: int(x.split(':')[1]))]},
          open('audio/manifest.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('manifest:', len(ids), 'слов,', len(samples), 'проб')
