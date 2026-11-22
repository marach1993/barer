# Generates audio/<file>.mp3 for each line "file|text|voice" in tts/list.txt (skips existing files).
import asyncio, os, edge_tts
os.makedirs('audio', exist_ok=True)
async def main():
    for line in open('tts/list.txt', encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'): continue
        f, text, voice = line.split('|')
        out = f'audio/{f}.mp3'
        if os.path.exists(out): continue
        for attempt in range(3):
            try:
                await edge_tts.Communicate(text, voice, rate='-10%').save(out); break
            except Exception as e:
                print('retry', f, e); await asyncio.sleep(2)
asyncio.run(main())
