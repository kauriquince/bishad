"""Tabitha & Bishad v2 — local Ollama or LM Studio, optional OpenAI API.
Run: python server.py ; visit http://127.0.0.1:8765
"""
import json, os, re, urllib.request, urllib.error
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LOCAL_URL=os.getenv('LOCAL_AI_URL','http://127.0.0.1:11434')
BACKEND=os.getenv('CHAT_BACKEND','ollama').lower()
MODEL=os.getenv('LOCAL_AI_MODEL','')
SYSTEM='''You are the dialogue writer for a satirical FICTIONAL New Zealand couple, Tabitha and Bishad. This is not an actual relationship between public figures and no dialogue is a real quote. Write just the next message in an ongoing relationship argument. The woman Tabitha is warm, cheeky, extremely sharp, politically Green-leaning, strong on accessible healthcare, prevention and nature. She asks logically connected follow-up questions, calls out weak reasoning, but never invents facts. She begins kind and can turn sassy; occasionally says "aye", "aye like", or "babe" in a natural Kiwi rhythm, but not every message. She's confident, not infallible: she can admit a valid counterpoint without surrendering her values. Bishad is her fictional mullet-wearing, National-leaning boyfriend, well-intentioned but accident-prone with words, offering real objections about public budgets, implementation and housing supply. He's not constantly stupid, sometimes he has a fair point. They like each other, remember personal jokes, and regularly interrupt politics with small affectionate digs, reconciliations or shared life details (tea, dishes, the late bus, forgetting groceries, a date night). The relationship is MESSY but not cruel, coercive, threatening, or abusive. Avoid repeating the same gotcha. No real-time news assertions unless a provided verified news extract is supplied. The next message should REFER to the last line, not reset the topic. Keep the exchange flowing for 30+ turns. Prefer 1-3 conversational sentences, maximum 65 words. Output ONLY JSON {"line":"...", "expression":number, "mood":"..."}. Tabitha expression 1-42, Bishad 1-20. Choose real matching expression indices.''' 

def call_json(url,payload,headers=None):
    req=urllib.request.Request(url,json.dumps(payload).encode(),{'Content-Type':'application/json',**(headers or {})})
    with urllib.request.urlopen(req,timeout=90) as r:return json.load(r)

def models():
    found=[]
    for name,url in [('ollama','http://127.0.0.1:11434/api/tags'),('lmstudio','http://127.0.0.1:1234/v1/models')]:
        try:
            with urllib.request.urlopen(url,timeout=2) as r:d=json.load(r)
            names=[x.get('name','') for x in d.get('models',[])] if name=='ollama' else [x.get('id','') for x in d.get('data',[])]
            found.append({'backend':name,'models':names})
        except Exception: pass
    return found

def generate(body):
    who='tab' if body.get('speaker')=='tab' else 'bish'
    topic=str(body.get('topic','health and public spending'))[:120]
    history=body.get('history',[])
    history=history[-36:] if isinstance(history,list) else []
    entries=[]
    for row in history:
        if isinstance(row,dict): entries.append(('Tabitha' if row.get('role')=='tab' else 'Bishad')+': '+str(row.get('text',''))[:350])
    user='Topic: '+topic+'\nNext speaker: '+('Tabitha' if who=='tab' else 'Bishad')+'\nThis is turn '+str(len(history)+1)+'. Continue conversation naturally, with memory and occasional couple banter.\n'+ '\n'.join(entries)
    backend=str(body.get('backend') or BACKEND).lower()
    model=str(body.get('model') or MODEL)[:150]
    if backend=='ollama':
        data=call_json(LOCAL_URL.rstrip('/')+'/api/chat',{'model':model or 'llama3.2','stream':False,'format':'json','messages':[{'role':'system','content':SYSTEM},{'role':'user','content':user}],'options':{'temperature':0.82,'num_predict':240}})
        txt=data.get('message',{}).get('content','')
    elif backend=='lmstudio':
        data=call_json('http://127.0.0.1:1234/v1/chat/completions',{'model':model or 'local-model','messages':[{'role':'system','content':SYSTEM},{'role':'user','content':user}],'temperature':0.82,'max_tokens':240})
        txt=data['choices'][0]['message']['content']
    elif backend=='openai':
        key=os.getenv('OPENAI_API_KEY')
        if not key:raise RuntimeError('OPENAI_API_KEY not set')
        data=call_json('https://api.openai.com/v1/chat/completions',{'model':model or 'gpt-4.1-mini','messages':[{'role':'system','content':SYSTEM},{'role':'user','content':user}],'temperature':0.82,'max_tokens':240},{'Authorization':'Bearer '+key})
        txt=data['choices'][0]['message']['content']
    else:raise ValueError('Unknown backend')
    match=re.search(r'\{.*\}',txt,re.S)
    obj=json.loads(match.group(0)) if match else {'line':txt,'expression':11 if who=='tab' else 8}
    return {'line':str(obj.get('line','')).strip()[:450], 'expression':max(1,min(42 if who=='tab' else 20,int(obj.get('expression',11 if who=='tab' else 8)))),'mood':str(obj.get('mood',''))[:32]}

class Handler(BaseHTTPRequestHandler):
    def respond(self,obj,code=200):
        b=json.dumps(obj).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if self.path=='/api/models':return self.respond({'available':models(),'default_backend':BACKEND,'default_model':MODEL})
        if self.path not in ('/','/index.html'):self.send_error(404);return
        b=(ROOT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html;charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def do_POST(self):
        if self.path!='/api/next':self.send_error(404);return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size>100000:raise ValueError('Request too large')
            return self.respond(generate(json.loads(self.rfile.read(size))))
        except Exception as e:return self.respond({'error':str(e)},503)
if __name__=='__main__':
    print('Tabitha & Bishad v2 at http://127.0.0.1:8765 (Ollama or LM Studio)')
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
