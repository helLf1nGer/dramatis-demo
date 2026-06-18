# -*- coding: utf-8 -*-
import pathlib

DOC = pathlib.Path("/tmp/dramatis-demo/docs/index.html")
B = pathlib.Path("/tmp/dramatis-demo/.build")
html = DOC.read_text()

def repl(s, old, new, label):
    n = s.count(old)
    assert n == 1, f"[{label}] expected exactly 1 match, found {n}"
    return s.replace(old, new)

# ---------- load generated components ----------
cards_css   = (B/"interactive-descriptive-voice-ca.css").read_text()
cards_js    = (B/"interactive-descriptive-voice-ca.js").read_text()
replay_html = (B/"replay-the-agent-trace-replay-co.html").read_text().rstrip()
replay_css  = (B/"replay-the-agent-trace-replay-co.css").read_text()
replay_js   = (B/"replay-the-agent-trace-replay-co.js").read_text()
ov_html     = (B/"a-new-how-dramatis-works-system-.html").read_text().strip()
ov_css      = (B/"a-new-how-dramatis-works-system-.css").read_text()

# ---------- critic fixes on component strings ----------
# (a) voice cue: hidden at rest, shown only on the first card of each grid (cut 12 gold prompts -> 3)
cards_css = repl(cards_css,
  ".vc-cue{display:inline;color:var(--gold);font-size:11px;letter-spacing:.02em;opacity:.55;\n  transition:opacity .25s ease}",
  ".vc-cue{display:inline;color:var(--gold);font-size:11px;letter-spacing:.02em;opacity:0;\n  transition:opacity .25s ease}\n.vc-cast > .vc-card:first-child .vc-cue{opacity:.5}",
  "cue-first-child")
# (b) overview: don't duplicate the pipeline spine in the pillar caption
ov_html = repl(ov_html,
  "<p>Analyze, cast, synthesize, process, soundscape, QA, mix, export. One coordinated agent run.</p>",
  "<p>Eight stages, one coordinated run — every action a checked, typed tool call.</p>",
  "ov-pipeline-pillar")

# ---------- fix-adjusted voice-card blocks (provider-family chips; WDH 6->4, no redundant lede) ----------
def card(prov, who, chip, voice, cue, for_, idline):
    cue_html = f' <span class="vc-cue" aria-hidden="true">why this voice ›</span>' if cue else ''
    return (f'        <div class="vc-card" tabindex="0" role="button" aria-expanded="false" data-prov="{prov}">\n'
            f'          <div class="vc-head"><span class="vc-who">{who}</span><span class="vc-chip">{chip}</span></div>\n'
            f'          <span class="vc-voice">{voice}{cue_html}</span>\n'
            f'          <div class="vc-detail"><div class="vc-detail-i">\n'
            f'            <span class="vc-for">{for_}</span>\n'
            f'            <span class="vc-id">{idline}</span>\n'
            f'          </div></div>\n'
            f'        </div>\n')

MARLEY_VC = ('      <div class="vc-cast">\n'
  + card("gemini","Narrator · Charon","Gemini TTS","warm fireside RP",True,"Warm fireside Dickensian storyteller — gentle gravitas, calm amid the dread.","Charon · Received Pronunciation")
  + card("gemini","Scrooge · Orus","Gemini TTS","thin, brittle, pinched",False,"High, thin, brittle and dry — the pinched, caustic miser.","Orus · Received Pronunciation")
  + card("gemini","Marley's Ghost · Algenib","Gemini TTS","deep, sepulchral + reverb",False,"Deep, sepulchral ghost — each word lands like a tolling bell.","Algenib · Received Pronunciation")
  + '      </div>')

ODYSSEY_VC = ('      <div class="vc-cast">\n'
  + card("gemini","Odysseus · Fenrir","Gemini TTS","deep, gravelly baritone",True,"Deep resonant baritone, gravelly — a seasoned king and survivor.","Fenrir · Received Pronunciation")
  + card("gemini","Polyphemus · Charon","Gemini TTS","deep, guttural, unrefined",False,"Massive chest resonance — a force of nature, terrifyingly arrogant.","Charon · deep, guttural")
  + card("gemini","Narrator · Fenrir","Gemini TTS","same voice as Odysseus",False,"The same voice as Odysseus — the hero recounting his own tale.","Fenrir · Received Pronunciation")
  + '      </div>')

WDH_VC = ('      <div class="vc-cast vc-cast--wide">\n'
  + card("chirp","Narrator","Google Chirp","warm, intimate storyteller",True,"Warm, intimate master storyteller by a fireside — the one role reserved for Chirp.","en-GB-Chirp3-HD-Vindemiatrix · British")
  + card("gemini","Dominic","Gemini TTS","protagonist lead",False,"Protagonist lead voice, given palace-room reverb for the dinner scene.","Alnilam · neutral British")
  + card("gemini","Pops","Gemini TTS","deep, warm elder",False,"Deep, warm elder presence anchoring the family dinner.","Algenib · neutral British")
  + card("eleven","General Fox","ElevenLabs","commanding military timbre",False,"A distinct ElevenLabs timbre, used surgically to mark the commanding military general.","cjVigY5qzO86Huf0OWal · ElevenLabs")
  + '      </div>')

# ---------- old blocks (current page) ----------
MARLEY_OLD = ('      <div class="cast">\n'
  '        <div class="voice"><span class="who">Narrator</span><span class="vo">Charon · warm, fireside RP</span></div>\n'
  '        <div class="voice"><span class="who">Scrooge</span><span class="vo">Orus · thin, brittle, pinched</span></div>\n'
  '        <div class="voice"><span class="who">Marley\'s Ghost</span><span class="vo">Algenib · deep, sepulchral + reverb</span></div>\n'
  '      </div>')
ODYSSEY_OLD = ('      <div class="cast">\n'
  '        <div class="voice"><span class="who">Odysseus</span><span class="vo">Fenrir · Received Pronunciation</span></div>\n'
  '        <div class="voice"><span class="who">Polyphemus</span><span class="vo">Charon · deep, guttural</span></div>\n'
  '        <div class="voice"><span class="who">Narrator</span><span class="vo">Fenrir · RP</span></div>\n'
  '      </div>')
WDH_STATLINE_OLD = ('      <div class="statline">\n'
  '        <div class="s"><b>46</b><span>chapters produced</span></div>\n'
  '        <div class="s"><b>76</b><span>distinct character voices</span></div>\n'
  '        <div class="s"><b>4</b><span>TTS providers, one cast</span></div>\n'
  '      </div>')
WDH_STATLINE_NEW = ('      <div class="statline">\n'
  '        <div class="s"><b>43</b><span>chapters produced</span></div>\n'
  '        <div class="s"><b>76</b><span>distinct character voices</span></div>\n'
  '        <div class="s"><b>4</b><span>TTS providers, one cast</span></div>\n'
  '      </div>\n' + WDH_VC)

REPLAY_OLD = ('    <div class="replay" id="replay">\n'
  '      <div class="replay-bar">\n'
  '        <span class="rb-dots"><i></i><i></i><i></i></span>\n'
  '        <span class="rb-title">dramatis · session: showcase-marley · ch01</span>\n'
  '        <button class="rb-play" id="rbPlay" type="button">▶ Replay</button>\n'
  '      </div>\n'
  '      <div class="replay-body" id="rbBody">\n'
  '        <div class="ev think">A beautiful piece — slow-burn dread in four waves. Let me break it down.</div>\n'
  '        <div class="ev call"><span class="tool">analyze_text</span><span class="res">4 scenes · 20 lines · 3 speaking parts</span></div>\n'
  '        <div class="ev think">Three registers in deliberate contrast. Auditioning candidates for each role.</div>\n'
  '        <div class="ev call"><span class="tool">audition_voice ×9</span><span class="res">Scrooge · Marley · Narrator — 3 takes each</span></div>\n'
  '        <div class="ev call"><span class="tool">evaluate_audition</span><span class="res">Orus “high, thin, dry” · Algenib “weary, sepulchral” · Charon “warm storyteller”</span></div>\n'
  '        <div class="ev call"><span class="tool">cast_voice ×3</span><span class="res">ensemble locked — high / mid / deep</span></div>\n'
  '        <div class="ev call"><span class="tool">set_audio_treatment</span><span class="res">Marley → supernatural reverb + pitch-drop</span></div>\n'
  '        <div class="ev call"><span class="tool">synthesize_batch</span><span class="res">19 line-level stems performed</span></div>\n'
  '        <div class="ev think">Stems are down — hand off to the review crew, all at once.</div>\n'
  '        <div class="ev par">\n'
  '          <div class="pa"><b>qa_engineer</b><span>transcribe + masking</span></div>\n'
  '          <div class="pa"><b>creative_dramaturg</b><span>performance vs brief</span></div>\n'
  '          <div class="pa"><b>sound_designer</b><span>build soundscape</span></div>\n'
  '        </div>\n'
  '        <div class="ev call warn"><span class="tool">qa_engineer ⚠</span><span class="res">“Much!”→“marsh” · narrator drifted +5.7 st</span></div>\n'
  '        <div class="ev call ok"><span class="tool">re-synthesize → re-verify</span><span class="res">transcript 86.5% → 99.7% · voice back in register</span></div>\n'
  '        <div class="ev call"><span class="tool">creative_dramaturg</span><span class="res">“Scrooge\'s arc perfectly realized… register clash superb”</span></div>\n'
  '        <div class="ev call"><span class="tool">design_soundscape</span><span class="res">16 cues · bells → chains → cellar-door boom → cello</span></div>\n'
  '        <div class="ev call"><span class="tool">mix_chapter → measure_masking</span><span class="res">42 layers · radio_drama · masking −4.4 dB → clear</span></div>\n'
  '        <div class="ev call ok"><span class="tool">export_chapter ✓</span><span class="res">ch01.mp3 · 3:19 · “release-ready”</span></div>\n'
  '      </div>\n'
  '    </div>')

# ---------- apply ----------
html = repl(html, MARLEY_OLD, MARLEY_VC, "marley-cast")
html = repl(html, ODYSSEY_OLD, ODYSSEY_VC, "odyssey-cast")
html = repl(html, WDH_STATLINE_OLD, WDH_STATLINE_NEW, "wdh-statline+cast")
html = repl(html, REPLAY_OLD, replay_html, "replay-markup")
html = repl(html, "<!-- GALLERY -->", ov_html + "\n\n<!-- GALLERY -->", "overview-insert")
html = repl(html, "</style>",
  "\n  /* ===== voice cards ===== */\n" + cards_css +
  "\n  /* ===== replay v2 ===== */\n" + replay_css +
  "\n  /* ===== system overview ===== */\n" + ov_css + "\n</style>", "css-append")

# replace the existing <script>...</script> (v1 replay IIFE) with v2 replay + cards
s0 = html.index("<script>"); s1 = html.index("</script>") + len("</script>")
old_script = html[s0:s1]
new_script = ("<script>\n/* ---- agent-trace replay (v2) ---- */\n" + replay_js.strip() +
              "\n\n/* ---- interactive voice cards ---- */\n" + cards_js.strip() + "\n</script>")
assert html.count(old_script) == 1, "script block not unique"
html = html.replace(old_script, new_script, 1)

DOC.write_text(html)
print("integrated OK; new length", len(html))
