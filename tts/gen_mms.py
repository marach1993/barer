# Offline Armenian TTS with Meta MMS (facebook/mms-tts-hye). Lines "file|text|mms" in tts/list.txt.
import os, subprocess, torch, scipy.io.wavfile as wf
from transformers import VitsModel, AutoTokenizer
os.makedirs('audio', exist_ok=True)
m = VitsModel.from_pretrained('facebook/mms-tts-hye'); tok = AutoTokenizer.from_pretrained('facebook/mms-tts-hye')
torch.manual_seed(1)
for line in open('tts/list.txt', encoding='utf-8'):
    line = line.strip()
    if not line or line.startswith('#'): continue
    f, text, voice = line.split('|')
    if voice != 'mms': continue
    out = f'audio/{f}.mp3'
    if os.path.exists(out) and os.path.getsize(out) > 0: continue
    ids = tok(text.lower(), return_tensors='pt')
    print(f, 'tokens', ids['input_ids'].shape, tok.convert_ids_to_tokens(ids['input_ids'][0])[:30])
    with torch.no_grad(): w = m(**ids).waveform[0].numpy()
    wf.write('/tmp/t.wav', m.config.sampling_rate, w)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','/tmp/t.wav','-ac','1','-b:a','48k',out], check=True)
    print('done', f, os.path.getsize(out))
