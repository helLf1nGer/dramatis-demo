# -*- coding: utf-8 -*-
import pathlib, re
DOC = pathlib.Path("/tmp/dramatis-demo/docs/index.html")
B = pathlib.Path("/tmp/dramatis-demo/.build")
h = DOC.read_text()

def one(s, old, new, label):
    assert s.count(old) == 1, f"[{label}] found {s.count(old)} matches (want 1)"
    return s.replace(old, new)

# ============ (1) TERMINAL: swap replay markup + CSS ============
new_markup = (B/"replay_markup.html").read_text().rstrip()
# current markup spans from the <div class="replay" to its matching close before the statline
m_start = h.index('<div class="replay" id="replay">')
m_end = h.index('<div class="statline" style="margin-top:24px">')
old_markup = h[m_start:m_end].rstrip()
assert old_markup.endswith('</div>'), "replay markup boundary unexpected"
h = h[:m_start] + new_markup + "\n\n    " + h[m_end:]

# replace the replay v2 CSS block (between its banner and the system-overview banner)
new_css = (B/"replay_css.txt").read_text().rstrip()
c_start = h.index("  /* ===== replay v2 ===== */")
c_end = h.index("  /* ===== system overview ===== */")
h = h[:c_start] + "  " + new_css + "\n\n" + h[c_end:]

# ============ (3) "why this voice" cue: make it a clear affordance, not a faux-link ============
# restyle: pill-shaped, muted, with a tiny play/expand glyph - reads as "tap me", not "link"
h = one(h,
  ".vc-cue{display:inline;color:var(--gold);font-size:11px;letter-spacing:.02em;opacity:0;\n  transition:opacity .25s ease}\n.vc-cast > .vc-card:first-child .vc-cue{opacity:.5}",
  (".vc-cue{display:inline-block;color:var(--mut);font-size:10px;letter-spacing:.04em;text-transform:uppercase;\n"
   "  border:1px solid var(--line);border-radius:999px;padding:1px 7px;opacity:0;transform:translateY(1px);\n"
   "  transition:opacity .25s ease,color .25s ease,border-color .25s ease;vertical-align:middle}\n"
   ".vc-cast > .vc-card:first-child .vc-cue{opacity:.7}\n"
   ".vc-card:hover .vc-cue{color:var(--gold);border-color:#3a3320}"),
  "cue-affordance")
# reword the cue text on every card (link-y "why this voice >" -> a tap affordance)
h = h.replace('<span class="vc-cue" aria-hidden="true">why this voice ›</span>',
              '<span class="vc-cue" aria-hidden="true">tap for casting</span>')

# ============ (2) AUDIO on Marley + Odyssey cards (per-voice samples) ============
# add a small inline ▶ control inside each vc-detail-i, before the .vc-id line.
def add_audio(html, who_marker, src):
    # find the card block containing this who, inject an audio control into its detail
    needle = f'<span class="vc-who">{who_marker}</span>'
    i = html.index(needle)
    # locate the vc-id within this card (next occurrence after needle)
    idpos = html.index('<span class="vc-id">', i)
    inject = (f'<span class="vc-sample"><button class="vc-play" type="button" data-src="audio/voices/{src}" '
              f'aria-label="Play voice sample">&#9655; hear voice</button></span>\n            ')
    return html[:idpos] + inject + html[idpos:]

for who, src in [
    ("Narrator · Charon", "marley_narrator.mp3"),
    ("Scrooge · Orus", "marley_scrooge.mp3"),
    ("Marley's Ghost · Algenib", "marley_ghost.mp3"),
    ("Odysseus · Fenrir", "odyssey_odysseus.mp3"),
    ("Polyphemus · Charon", "odyssey_polyphemus.mp3"),
]:
    h = add_audio(h, who, src)

# ============ (5) WDH gallery clip swap + research-preview honesty note ============
h = one(h, 'Chapter 43 — “Royal Palace Dinner” · 58-second highlight',
        'Chapter 42 — “Welcome Party” · 58-second highlight', "wdh-meta")
h = one(h,
  '<span class="sp">General Fox:</span> “What do you think of the fine rumours that have started\n'
  '        around you, Young Master Dominic Wavemates?”<br>\n'
  '        <span class="sp">Dominic:</span> “At least ten percent of that is true, Lord General Fox.”',
  '<span class="sp">Princess Alexis:</span> “That’s the same thing your Master threatened, the first time we tried.”<br>\n'
  '        <span class="sp">Dominic:</span> “What can I say? I learned from the best.”',
  "wdh-quote")
h = one(h, 'src="audio/wdh_ch43_highlight.mp3"', 'src="audio/wdh_ch42_highlight.mp3"', "wdh-audio")
# research-preview note on the WDH card (honest: older run, quality below the Marley showcase)
h = one(h,
  '<p class="note">A feature-length original — proof the pipeline holds a consistent cast across an\n'
  '        entire book, not just a clip.</p>',
  '<p class="note"><span class="rp-tk" style="color:var(--gold2);opacity:1;border-color:#3a3320">research preview</span> '
  'A feature-length original (46 chapters, 76 voices) from an <strong>earlier pipeline</strong> — included to show scale and '
  'multi-provider casting. Fidelity sits below the <em>Marley</em> showcase above; quality has moved fast since.</p>',
  "wdh-note")

# ============ (4) HYBRID pillar: reframe as planned/on-the-roadmap (foundation exists) ============
h = one(h, '<h3>Hybrid layers <span class="ov-soon">sound-design</span></h3>',
        '<h3>Hybrid studio + AI <span class="ov-soon">on the roadmap</span></h3>', "hybrid-h3")
h = one(h,
  '<p>Bring your own sound-design audio into the library. Voice takes: AI-synthesized today.</p>',
  '<p>Import sound-design audio today; studio-recorded voice takes alongside AI voices are next — the foundation is in place.</p>',
  "hybrid-p")

DOC.write_text(h)
print("integrate2 OK; length", len(h))
