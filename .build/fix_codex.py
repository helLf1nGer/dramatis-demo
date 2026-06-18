# -*- coding: utf-8 -*-
import pathlib
DOC = pathlib.Path("/tmp/dramatis-demo/docs/index.html")
RM = pathlib.Path("/tmp/dramatis-demo/README.md")
h = DOC.read_text()

def one(old, new, label):
    global h
    assert h.count(old) == 1, f"[{label}] found {h.count(old)} (want 1)"
    h = h.replace(old, new)

# ---- P0 #1: chapter contradiction 46 -> 43 (note matches statline) ----
one("A feature-length original (46 chapters, 76 voices)",
    "A feature-length original (43 chapters, 76 speaking roles)", "chaptercount")

# ---- P0 #2: false repair count targets=2 -> 5 ----
one('(targets=<span class="tr-num">2</span>)', '(targets=<span class="tr-num">5</span>)', "targets")

# ---- a11y P0 (my bug): guard keydown handler against the nested .vc-play button ----
one(
  "    card.addEventListener('keydown', function(e){\n"
  "      var k = e.key;\n",
  "    card.addEventListener('keydown', function(e){\n"
  "      if(e.target && e.target.closest && e.target.closest('.vc-play')) return; // let the play button handle itself\n"
  "      var k = e.key;\n",
  "keydown-guard")

# ---- a11y: aria-expanded driven by focus; blur guarded against focus into nested button ----
one(
  "    // blur via keyboard navigation: collapse the tap-state so it doesn't linger\n"
  "    card.addEventListener('blur', function(){\n"
  "      // keep :focus-within behaviour to CSS; only clear the explicit tap flag\n"
  "      close(card);\n"
  "    });",
  "    // keyboard focus visually reveals the drawer (CSS :focus-within); keep aria in sync\n"
  "    card.addEventListener('focus', function(){ card.setAttribute('aria-expanded','true'); });\n"
  "    // collapse when focus truly leaves the card (not when it moves into the nested play button)\n"
  "    card.addEventListener('blur', function(e){\n"
  "      if(e.relatedTarget && card.contains(e.relatedTarget)) return;\n"
  "      close(card);\n"
  "    });",
  "blur-guard")

# ---- wording: 76 distinct voices -> speaking roles ----
one("<b>76</b><span>distinct character voices</span>", "<b>76</b><span>speaking roles</span>", "76roles")

# ---- wording: 4 TTS providers -> 4 TTS engines ----
one("<b>4</b><span>TTS providers, one cast</span>", "<b>4</b><span>TTS engines, one cast</span>", "4engines")

# ---- hero: distinct voice per character -> a voice to every character ----
one("casts a distinct voice per character,", "casts a voice for every character,", "hero-distinct")

# ---- centerpiece: No human edits -> No manual audio editing ----
one("loop. No human edits.</p>", "loop. No manual audio editing.</p>", "no-human-edits")

# ---- release-ready: don't style prose as a structured export verdict ----
one('verdict: <span class="tr-q">"release-ready"</span>',
    'mix review: <span class="tr-ok" style="color:var(--gold2)">approve_with_notes</span> <span class="tr-q">"release-ready"</span>',
    "release-ready")

# ---- audio aria-labels (3) ----
one('<audio controls preload="none" src="audio/marley.mp3"></audio>',
    '<audio controls preload="none" src="audio/marley.mp3" aria-label="A Christmas Carol — Marley\'s Ghost (full production audio)"></audio>', "aria-marley")
one('<audio controls preload="none" src="audio/odyssey_polyphemus.mp3"></audio>',
    '<audio controls preload="none" src="audio/odyssey_polyphemus.mp3" aria-label="The Odyssey — Cave of Polyphemus (audio)"></audio>', "aria-odyssey")
one('<audio controls preload="none" src="audio/wdh_ch42_highlight.mp3"></audio>',
    '<audio controls preload="none" src="audio/wdh_ch42_highlight.mp3" aria-label="World Dragon\'s Heir — chapter 42 highlight (audio)"></audio>', "aria-wdh")

DOC.write_text(h)
print("html fixes applied; length", len(h))

# ---- README ch43 -> ch42 ----
r = RM.read_text()
old_r = "- `wdh_ch43_highlight.mp3` — *World Dragon's Heir* (original novel), ch43 \"Royal Palace Dinner\" — dialogue highlight from a 46-chapter production."
new_r = "- `wdh_ch42_highlight.mp3` — *World Dragon's Heir* (original novel), ch42 \"Welcome Party\" — dialogue highlight from a 43-chapter production."
assert r.count(old_r) == 1, "readme line not found"
RM.write_text(r.replace(old_r, new_r))
print("readme fixed")
