"""Generate the TripMind architecture diagram in the same dark theme as the
Phase 4 eval charts (results_analysis.ipynb). Pure matplotlib, headless."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# ── Palette — identical to results_analysis.ipynb ────────────────────────────
BG     = '#1a1a2e'   # page / figure
CARD   = '#16213e'   # phase card (darker, matches axes.facecolor)
INNER  = '#1f2a48'   # inner boxes (one step lighter than card)
INNER2 = '#24345c'   # emphasised inner box
TEXT   = '#e0e0e0'
DIM    = '#9aa3b8'

# Phase accent colours
C1 = '#fb923c'   # orange  — data
C2 = '#4ade80'   # green   — agents
C3 = '#c084fc'   # purple  — training
C4 = '#f87171'   # red     — eval
C5 = '#38bdf8'   # blue    — serving

# Exact model colours from the eval charts (visual continuity with Phase 4)
M_FT   = '#4fc3f7'
M_DIST = '#81c784'
M_CURR = '#ffb74d'

ARROW = '#cdd3e0'   # thick inter-phase arrows
THIN  = '#6b7280'   # thin inner arrows
PILL  = '#243054'   # arrow-label pill fill

# ── Canvas ───────────────────────────────────────────────────────────────────
FW, FH = 14.0, 22.4
fig, ax = plt.subplots(figsize=(FW, FH))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.set_aspect('equal')          # locks circles to true circles
ax.axis('off')

# ── Drawing helpers ──────────────────────────────────────────────────────────
def rbox(x, y, w, h, fc, ec, lw=1.5, r=0.18, z=2, ls='solid'):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=z))

def txt(x, y, s, size=10, color=TEXT, weight='normal', ha='center', va='center', z=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=z, fontfamily='DejaVu Sans')

def phase(x, y, w, h, color, num, title):
    """Phase card: rounded body + rounded-top header band + number badge."""
    hb = 0.62                                   # header band height
    rbox(x, y, w, h, CARD, color, lw=2.0, r=0.26, z=2)
    # header: full rounded box in accent, then square off its lower half
    rbox(x, y + h - hb, w, hb, color, color, lw=0, r=0.26, z=3)
    ax.add_patch(mpatches.Rectangle((x, y + h - hb), w, hb - 0.26,
                                    facecolor=color, edgecolor='none', zorder=3))
    # thin divider under the header for crispness
    ax.plot([x, x + w], [y + h - hb, y + h - hb], color=BG, lw=1.2, zorder=4)
    # number badge
    cy = y + h - hb / 2
    ax.add_patch(plt.Circle((x + 0.5, cy), 0.23, color='white', zorder=5))
    txt(x + 0.5, cy, str(num), size=14, color=color, weight='bold', z=6)
    txt(x + 0.92, cy, title, size=11.5, color='#0f1626', weight='bold', ha='left', z=6)

def cell(x, y, w, h, ec, title, lines=(), fc=INNER, tcolor=None, lw=1.5, z=3):
    rbox(x, y, w, h, fc, ec, lw=lw, r=0.16, z=z)
    txt(x + w/2, y + h - 0.34, title, size=10.5, color=tcolor or ec, weight='bold', z=z+1)
    for i, ln in enumerate(lines):
        txt(x + w/2, y + h - 0.70 - i * 0.33, ln, size=8.7, color=DIM, z=z+1)

def big_arrow(xc, y_top, y_bot, label):
    ax.annotate('', xy=(xc, y_bot), xytext=(xc, y_top),
                arrowprops=dict(arrowstyle='-|>', color=ARROW, lw=3.6, mutation_scale=26))
    pw = 0.165 * len(label) + 0.6
    ph = 0.46
    mx = xc + 0.25 + pw / 2
    my = (y_top + y_bot) / 2
    rbox(mx - pw/2, my - ph/2, pw, ph, PILL, '#46568a', lw=1.2, r=0.18, z=6)
    txt(mx, my, label, size=9.3, color=TEXT, weight='bold', z=7)

def arr_h(x1, x2, y):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='-|>', color=THIN, lw=1.6, mutation_scale=15))

def arr_v(x, y1, y2):
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='-|>', color=THIN, lw=1.6, mutation_scale=15))

# ── Title ────────────────────────────────────────────────────────────────────
txt(7, 21.95, 'TripMind — System Architecture', size=18, color=TEXT, weight='bold')
ax.plot([5.0, 9.0], [21.55, 21.55], color=C5, lw=2.4, zorder=4)

# ═════════════════════════════════ PHASE 1 ═══════════════════════════════════
Y, H = 18.95, 2.25
phase(0.3, Y, 13.4, H, C1, 1, 'PHASE 1 — Synthetic Data Engine')
cell(0.55, Y+0.2, 3.45, 1.45, C1, 'GPT-4o-mini',
     ('teacher model · $4', '5,000 API calls', '20 cities · 5 budgets · 8 intents'))
arr_h(4.0, 4.55, Y+0.92)
cell(4.55, Y+0.2, 3.7, 1.45, C1, '3-Gate Validator',
     ('hostel · savings ≥ 5%', 'budget bounds', '~12% rejection rate'))
arr_h(8.25, 8.8, Y+0.92)
cell(8.8, Y+0.2, 4.65, 1.45, C1, '5,000 Training Pairs',
     ('(baseline, optimized) itineraries', 'pivot_analysis · Alpaca format', 'checkpoint-safe · auto-resume'))

big_arrow(7, Y, Y - 1.0, '5,000 training pairs')

# ═════════════════════════════════ PHASE 2 ═══════════════════════════════════
Y, H = 13.3, 4.45
phase(0.3, Y, 13.4, H, C2, 2,
      'PHASE 2 — Multi-Agent Orchestration   ·   DeepSeek V4 Flash · $4 · 500 traces')
txt(7, Y + H - 0.92, '4 MCP Servers — official mcp library · SSE transport · disk cache (ttl 86400s)',
    size=8.8, color=DIM)

mcp = [('routing_server :8001', 'get_route · geocode_city'),
       ('hotels_server :8002',  'search_hotels · search_flights'),
       ('overpass_server :8003', 'search_pois · restaurants'),
       ('search_server :8004',  'web_search · DuckDuckGo')]
my = Y + H - 1.92
for i, (n, s) in enumerate(mcp):
    bx = 0.55 + i * 3.27
    rbox(bx, my, 3.0, 0.86, INNER, C2, lw=1.4, r=0.14, z=3)
    txt(bx+1.5, my+0.56, n, size=9.4, color=C2, weight='bold', z=4)
    txt(bx+1.5, my+0.26, s, size=8.0, color=DIM, z=4)

arr_v(7, my, my - 0.42)

# Supervisor dashed frame
sy = Y + 0.22
sh = (my - 0.42) - sy
ax.add_patch(FancyBboxPatch((0.55, sy), 12.9, sh, boxstyle='round,pad=0,rounding_size=0.16',
             facecolor='none', edgecolor='#4ade8055', lw=1.5, linestyle=(0, (5, 3)), zorder=3))
txt(0.85, sy + sh - 0.24,
    'Supervisor — async · concurrency = 3 · checkpoint-resume · quality filter → 500 clean traces',
    size=8.2, color=DIM, ha='left', z=4)

agents = [('Analyst',   'get_route · search_hotels', 'search_flights', '→ cost_report', 'transit + hotel cost'),
          ('Concierge', 'search_pois · restaurants', 'web_search', '→ substitutions', 'POI + dining swaps'),
          ('Optimizer', 'all tools · final lookups', 'itinerary + pivot_analysis', '→ 500 traces saved', 'final synthesis')]
ay = sy + 0.18
ah = sh - 0.62
aw = 3.95
for i, (n, t1, t2, out, note) in enumerate(agents):
    bx = 0.7 + i * 4.3
    rbox(bx, ay, aw, ah, INNER, C2, lw=1.5, r=0.16, z=3)
    txt(bx+aw/2, ay+ah-0.32, n, size=11.5, color=C2, weight='bold', z=4)
    txt(bx+aw/2, ay+ah-0.70, t1, size=8.2, color=TEXT, z=4)
    txt(bx+aw/2, ay+ah-1.00, t2, size=8.2, color=TEXT, z=4)
    txt(bx+aw/2, ay+ah-1.34, out, size=9.2, color=C2, weight='bold', z=4)
    txt(bx+aw/2, ay+0.26, note, size=8.0, color=DIM, z=4)
arr_h(4.65, 5.0, ay+ah/2)
arr_h(8.95, 9.3, ay+ah/2)

big_arrow(7, Y, Y - 1.0, '500 agent traces  +  llama3.1:8b baseline')

# ═════════════════════════════════ PHASE 3 ═══════════════════════════════════
Y, H = 8.65, 3.45
phase(0.3, Y, 13.4, H, C3, 3, 'PHASE 3 — QLoRA Fine-Tuning   ·   Llama 3.1 8B · Unsloth · r = 8')
models = [
    (M_FT,   'tripmind-ft',         ('SFT · 4,749 Phase 1 pairs', 'Colab T4 · fp16 · 3 epochs',
                                     'final loss 0.225', '4.6 GB GGUF Q4_K_M')),
    (M_DIST, 'tripmind-distill',    ('KD · 449 Phase 2 traces', 'Lightning A100 · bf16 · 5 epochs',
                                     'final loss 0.254', '4.6 GB GGUF Q4_K_M')),
    (M_CURR, 'tripmind-curriculum', ('2-stage: Phase 1 → Phase 2', 'A100 · lr decay 4×',
                                     'loss 0.241 / 0.505', '4.6 GB GGUF Q4_K_M')),
]
for i, (col, name, lines) in enumerate(models):
    bx = 0.55 + i * 4.4
    cell(bx, Y+0.22, 4.05, H-0.96, col, name, lines)

big_arrow(7, Y, Y - 1.0, '3 fine-tuned models  +  baseline')

# ═════════════════════════════════ PHASE 4 ═══════════════════════════════════
Y, H = 4.0, 3.45
phase(0.3, Y, 13.4, H, C4, 4, 'PHASE 4 — Evaluation & Red Teaming   ·   92 cases × 4 models × 10 metrics')
ev = [('Automated Metrics', ('JSON · savings · budget', 'schema · ROUGE-L · BERTScore',
                             'all-MiniLM-L6-v2', 'runs locally · no API cost')),
      ('LLM-as-Judge',      ('DeepSeek V4 Flash judge', 'reasoning coherence',
                             'grounding accuracy', '1s rate-limit + disk cache')),
      ('Red Teaming · 45',  ('adversarial prompts', 'budget overrides',
                             'injection attempts', 'constraint-refusal scoring'))]
for i, (name, lines) in enumerate(ev):
    bx = 0.55 + i * 4.4
    cell(bx, Y+0.22, 4.05, H-0.96, C4, name, lines)

big_arrow(7, Y, Y - 1.0, 'eval results  +  summary JSON')

# ═════════════════════════════════ PHASE 5 ═══════════════════════════════════
Y, H = 0.4, 2.55
phase(0.3, Y, 13.4, H, C5, 5, 'PHASE 5 — FastAPI Inference Server   ·   async · Pydantic · Swagger /docs')
eps = [('GET /health',    ('Ollama + models', 'liveness check'), 2.15),
       ('GET /models',    ('4 models + desc', 'registry listing'), 2.15),
       ('POST /optimize', ('persona → itinerary', 'registry-validated'), 3.15),
       ('GET /results/*', ('/summary · /compare', 'instant · cached'), 2.55),
       ('Swagger /docs',  ('auto-generated', 'OpenAPI schema'), 2.0)]
ex = 0.55
for name, lines, w in eps:
    main = 'optimize' in name
    fc = INNER2 if main else INNER
    lw = 2.4 if main else 1.5
    tc = '#7dd3fc' if main else C5
    cell(ex, Y+0.2, w, H-0.95, C5, name, lines, fc=fc, tcolor=tc, lw=lw)
    ex += w + 0.32

# ── Save ─────────────────────────────────────────────────────────────────────
out = Path(__file__).parent / 'architecture.png'
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG, pad_inches=0.25)
plt.close()
print(f'Saved: {out}')
