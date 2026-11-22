# Generates audio/<file>.mp3 for each line "file|text|voice" in tts/list.txt (skips existing files).
import asyncio, os, edge_tts
os.makedirs('audio', exist_ok=True)
async def main():
    vs = await edge_tts.list_voices()
    print('hy voices:', [v['ShortName'] for v in vs if v['Locale'].lower().startswith('hy')])
    print('total voices:', len(vs))
    for line in open('tts/list.txt', encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'): continue
        f, text, voice = line.split('|')
        out = f'audio/{f}.mp3'
        if os.path.exists(out) and os.path.getsize(out) > 0: continue
        ok = False
        for attempt in range(3):
            try:
                await edge_tts.Communicate(text, voice).save(out); ok = os.path.getsize(out) > 0
                if ok: break
            except Exception as e:
                print('retry', f, voice, repr(e)); await asyncio.sleep(2)
        if not ok and os.path.exists(out): os.remove(out)
        print('done' if ok else 'FAILED', f)
asyncio.run(main())
