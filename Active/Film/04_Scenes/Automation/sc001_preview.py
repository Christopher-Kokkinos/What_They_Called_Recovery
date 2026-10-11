"""Local image-sequence viewer: no codecs, network, pip or add-ons required."""
import json


def write_viewer(path, entries):
    payload=json.dumps(entries).replace('<','\\u003c')
    path.write_text('''<!doctype html><meta charset="utf-8"><title>SC001 coarse motion review</title>
<style>body{background:#20252b;color:#eee;font:16px sans-serif;margin:20px}img{display:block;max-width:100%;width:960px}input{width:80%}button{padding:8px}#info{margin:12px 0}</style>
<h1>SC001 coarse motion review</h1><p>4 sampled frames/second • 115 seconds • silent diagnostic • timing provisional</p>
<img id="view" alt="SC001 sampled Blender frame"><div id="info"></div>
<button id="play">Play</button> <input id="scrub" type="range" min="0" value="0" step="1">
<p>Pause/scrub to inspect continuity. Use full-resolution stills for text readability. This preview samples the 24fps scene every six frames.</p>
<script>const frames='''+payload+''';let i=0,timer=null;const view=document.getElementById('view'),info=document.getElementById('info'),scrub=document.getElementById('scrub'),play=document.getElementById('play');scrub.max=frames.length-1;
function show(){const f=frames[i];view.src=f.image;info.textContent=f.shot+' | source frame '+f.frame+' | '+((f.frame-1)/24).toFixed(2)+' s | '+f.cue;scrub.value=i;}
function stop(){clearInterval(timer);timer=null;play.textContent='Play';}
play.onclick=()=>{if(timer){stop();return;}if(i===frames.length-1)i=0;play.textContent='Pause';timer=setInterval(()=>{show();if(i===frames.length-1){stop();}else{i++;}},250);};scrub.oninput=()=>{stop();i=Number(scrub.value);show();};show();
</script>''',encoding='utf-8')
