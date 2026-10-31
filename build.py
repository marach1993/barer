import datetime
w=open('words.txt',encoding='utf-8').read().strip()
assert '`' not in w and '\\' not in w and '${' not in w
v=datetime.date.today().isoformat()
body=open('app.html',encoding='utf-8').read().replace('__WORDS__',w).replace('__VERSION__',v).replace('__CURSIVE__',open('cursive.json').read())
open('artifact.html','w',encoding='utf-8').write(body)
full='<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n'+body+'\n</body>\n</html>\n'
open('index.html','w',encoding='utf-8').write(full)
