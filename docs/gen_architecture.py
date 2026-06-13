"""Generate architecture diagram matching the existing chart dark theme."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe
from pathlib import Path

# ── Colour palette (matches results_analysis.ipynb) ──────────────────────────
BG        = '#1a1a2e'
BOX_BG    = '#16213e'
SUBTLE_BG = '#1e2a4a'   # slightly lighter for inner boxes
TEXT      = '#e0e0e0'
DIM       = '#9ca3af'

P1 = '#fb923c'   # orange
P2 = '#4ade80'   # green
P3 = '#c084fc'   # purple
P4 = '#f87171'   # red / pink
P5 = '#38bdf8'   # blue

ARROW = '#e0e0e0'   # thick inter-phase arrows
SMALL = '#6b7280'   # thin inner arrows

# ── Figure setup ─────────────────────────────────────────────────────────────
FW, FH = 14, 22
fig, ax = plt.subplots(figsize=(FW, FH))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, FW)
ax.set_ylim(0, FH)
ax.axis('off')

# ── Helpers ───────────────────────────────────────────────────────────────────
def rbox(x, y, w, h, fc, ec, lw=1.5, radius=0.2, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                        boxstyle=f'round,pad=0,rounding_size={radius}',
                        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder)
    ax.add_patch(p)
    return p

def txt(x, y, s, size=10, color=TEXT, weight='normal', ha='center', va='center', zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, zorder=zorder, fontfamily='DejaVu Sans')

def phase_frame(x, y, w, h, color, num, title):
    """Draw phase outer box + coloured header band + numbered circle."""
    rbox(x, y, w, h, BOX_BG, color, lw=2, radius=0.25, zorder=2)
    # header band
    rbox(x, y + h - 0.58, w, 0.58, color, color, lw=0, radius=0.25, zorder=3)
    # fix bottom corners of header to be square
    ax.add_patch(mpatches.Rectangle((x, y + h - 0.58), w, 0.25,
                                     facecolor=color, edgecolor='none', zorder=3))
    # number badge
    ax.add_patch(plt.Circle((x + 0.45, y + h - 0.29), 0.22,
                              color='white', zorder=4))
    txt(x + 0.45, y + h - 0.29, str(num), size=13, color=color, weight='bold', zorder=5)
    txt(x + 0.82, y + h - 0.29, title, size=11, color='white', weight='bold',
        ha='left', zorder=5)

def inner_box(x, y, w, h, color, title, lines=(), zorder=3):
    rbox(x, y, w, h, SUBTLE_BG, color, lw=1.5, radius=0.18, zorder=zorder)
    txt(x + w/2, y + h - 0.28, title, size=10.5, color=color, weight='bold', zorder=zorder+1)
    for i, line in enumerate(lines):
        txt(x + w/2, y + h - 0.58 - i * 0.30, line, size=8.5, color=DIM, zorder=zorder+1)

def big_arrow(x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=ARROW,
                                lw=3.5, mutation_scale=22))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        rbox(mx - len(label)*0.065, my - 0.18, len(label)*0.13, 0.36,
             '#2a2a4a', '#3a3a5a', lw=1, radius=0.12, zorder=6)
        txt(mx, my, label, size=9, color=TEXT, weight='bold', zorder=7)

def small_arrow_h(x1, x2, y):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color=SMALL, lw=1.5, mutation_scale=14))

def small_arrow_v(x, y1, y2):
    ax.annotate('', xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle='->', color=SMALL, lw=1.5, mutation_scale=14))

# ─────────────────────────────────────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────────────────────────────────────
txt(7, 21.5, 'TripMind — System Architecture', size=17, color=TEXT, weight='bold')

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1  (y=18.8 → 21.0)
# ─────────────────────────────────────────────────────────────────────────────
P1Y, P1H = 18.8, 2.2
phase_frame(0.3, P1Y, 13.4, P1H, P1, 1, 'PHASE 1 — Synthetic Data Engine')

inner_box(0.5, P1Y+0.15, 3.4, 1.55, P1, 'GPT-4o-mini',
          ('teacher model · $4', '5,000 API calls', '20 cities · 5 budgets · 8 intents'))

small_arrow_h(3.9, 4.5, P1Y + 0.95)

inner_box(4.5, P1Y+0.15, 3.7, 1.55, P1, '3-Gate Validator',
          ('hostel check', 'savings ≥ 5% · budget bounds', '~12% rejection rate'))

small_arrow_h(8.2, 8.8, P1Y + 0.95)

inner_box(8.8, P1Y+0.15, 4.7, 1.55, P1, '5,000 Training Pairs',
          ('(baseline, optimized) itineraries', 'pivot_analysis · Alpaca format', 'checkpoint-safe · resume on crash'))

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 1 → 2
# ─────────────────────────────────────────────────────────────────────────────
big_arrow(7, P1Y, 7, P1Y - 1.05, '5,000 training pairs')

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2  (y=13.2 → 17.6)
# ─────────────────────────────────────────────────────────────────────────────
P2Y, P2H = 13.2, 4.4
phase_frame(0.3, P2Y, 13.4, P2H, P2, 2,
            'PHASE 2 — Multi-Agent Orchestration  (DeepSeek V4 Flash · $4 · 500 traces)')

# MCP subtitle
txt(7, P2Y + P2H - 0.82, '4 MCP Servers — official mcp library · SSE transport · disk cache ttl=86400s',
    size=8.5, color=DIM)

# 4 MCP server boxes
mcp_y = P2Y + P2H - 1.75
mcp_w = 3.0
for i, (name, sub) in enumerate([
    ('routing_server :8001', 'get_route · geocode_city'),
    ('hotels_server :8002',  'search_hotels · search_flights'),
    ('overpass_server :8003', 'search_pois · search_restaurants'),
    ('search_server :8004',  'web_search (DuckDuckGo)'),
]):
    bx = 0.5 + i * 3.3
    rbox(bx, mcp_y, 3.0, 0.9, SUBTLE_BG, P2, lw=1.5, radius=0.15, zorder=3)
    txt(bx + 1.5, mcp_y + 0.62, name, size=9.5, color=P2, weight='bold', zorder=4)
    txt(bx + 1.5, mcp_y + 0.28, sub, size=8, color=DIM, zorder=4)

# down arrow to supervisor
small_arrow_v(7, mcp_y, mcp_y - 0.45)

# Supervisor dashed frame
sup_y = P2Y + 0.18
sup_h = mcp_y - 0.45 - sup_y
ax.add_patch(mpatches.FancyBboxPatch((0.5, sup_y), 12.9, sup_h,
             boxstyle='round,pad=0.05', facecolor='none',
             edgecolor='#4ade8055', linewidth=1.5,
             linestyle='--', zorder=3))
txt(1.1, sup_y + sup_h - 0.22,
    'Supervisor — async · concurrency=3 · checkpoint-resume · quality filter → 500 clean traces',
    size=8, color=DIM, ha='left', zorder=4)

# 3 Agent boxes
ag_y = sup_y + 0.08
ag_h = sup_h - 0.38
aw = 3.9
for i, (name, tools, out, note) in enumerate([
    ('Analyst',   'get_route · search_hotels · search_flights', '→ cost_report',   'transit + hotel cost analysis'),
    ('Concierge', 'search_pois · search_restaurants · web_search', '→ substitutions', 'POI + dining replacements'),
    ('Optimizer', 'all tools → optimized itinerary + pivot_analysis', '→ 500 traces saved', 'final synthesis'),
]):
    bx = 0.6 + i * 4.35
    rbox(bx, ag_y, aw, ag_h, SUBTLE_BG, P2, lw=1.5, radius=0.18, zorder=3)
    txt(bx + aw/2, ag_y + ag_h - 0.28, name, size=11, color=P2, weight='bold', zorder=4)
    txt(bx + aw/2, ag_y + ag_h - 0.62, tools, size=8, color=TEXT, zorder=4)
    txt(bx + aw/2, ag_y + ag_h - 0.96, out, size=9, color=TEXT, weight='bold', zorder=4)
    txt(bx + aw/2, ag_y + 0.22, note, size=8, color=DIM, zorder=4)

small_arrow_h(4.5, 4.95, ag_y + ag_h/2)
small_arrow_h(8.85, 9.3, ag_y + ag_h/2)

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 2 → 3
# ─────────────────────────────────────────────────────────────────────────────
big_arrow(7, P2Y, 7, P2Y - 1.05, '500 agent traces + llama3.1:8b baseline')

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3  (y=8.6 → 12.0)
# ─────────────────────────────────────────────────────────────────────────────
P3Y, P3H = 8.6, 3.4
phase_frame(0.3, P3Y, 13.4, P3H, P3, 3,
            'PHASE 3 — QLoRA Fine-Tuning  (Llama 3.1 8B · Unsloth · r=8)')

for i, (name, d1, d2, d3, note) in enumerate([
    ('tripmind-ft',         'SFT on 4,749 Phase 1 pairs',   'Colab T4 · fp16 · 3 epochs',      'loss 0.225 · 4.6 GB GGUF', 'plain SFT on synthetic pairs'),
    ('tripmind-distill',    'KD on 449 Phase 2 traces',     'Lightning A100 · bf16 · 5 epochs', 'loss 0.254 · 4.6 GB GGUF', 'distilled from agent traces'),
    ('tripmind-curriculum', '2-stage: Phase 1 → Phase 2',   'Lightning A100 · lr decay 4×',     'loss 0.241/0.505 · 4.6 GB GGUF', 'sequential domain → reasoning'),
]):
    bx = 0.5 + i * 4.45
    inner_box(bx, P3Y + 0.18, 4.1, P3H - 0.78, P3, name, (d1, d2, d3, note))

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 3 → 4
# ─────────────────────────────────────────────────────────────────────────────
big_arrow(7, P3Y, 7, P3Y - 1.05, '3 fine-tuned models + baseline')

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4  (y=3.95 → 7.35)
# ─────────────────────────────────────────────────────────────────────────────
P4Y, P4H = 3.95, 3.4
phase_frame(0.3, P4Y, 13.4, P4H, P4, 4,
            'PHASE 4 — Evaluation & Red Teaming  (92 cases × 4 models × 10 metrics)')

for i, (name, lines) in enumerate([
    ('Automated Metrics',    ('JSON valid · savings · budget · schema',
                              'ROUGE-L · BERTScore F1',
                              'all-MiniLM-L6-v2 · runs locally',
                              'no API cost')),
    ('LLM-as-Judge',         ('DeepSeek V4 Flash judge',
                              'reasoning coherence',
                              'grounding accuracy',
                              '1s rate limit + disk cache')),
    ('Red Teaming · 45 cases', ('adversarial prompts',
                                'budget overrides',
                                'injection attempts',
                                'constraint refusal scoring')),
]):
    bx = 0.5 + i * 4.45
    inner_box(bx, P4Y + 0.18, 4.1, P4H - 0.78, P4, name, lines)

# ─────────────────────────────────────────────────────────────────────────────
# Arrow 4 → 5
# ─────────────────────────────────────────────────────────────────────────────
big_arrow(7, P4Y, 7, P4Y - 1.05, 'eval results + summary JSON')

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 5  (y=0.4 → 2.7)
# ─────────────────────────────────────────────────────────────────────────────
P5Y, P5H = 0.4, 2.5
phase_frame(0.3, P5Y, 13.4, P5H, P5, 5,
            'PHASE 5 — FastAPI Inference Server  (async · Pydantic · Swagger /docs)')

ep_data = [
    ('GET /health',    ('Ollama + models', 'liveness check'), 2.1),
    ('GET /models',    ('4 models + desc', 'registry listing'), 2.1),
    ('POST /optimize', ('persona → itinerary', 'model registry validated'), 3.2),
    ('GET /results/*', ('/summary · /compare', 'instant · no inference'), 2.6),
    ('Swagger /docs',  ('auto-generated', ''), 1.9),
]
ex = 0.5
for name, lines, ew in ep_data:
    is_main = 'optimize' in name
    ec = P5
    fc = '#1e3a5a' if is_main else SUBTLE_BG
    lw = 2.5 if is_main else 1.5
    rbox(ex, P5Y + 0.15, ew, P5H - 0.75, fc, ec, lw=lw, radius=0.18, zorder=3)
    nc = '#7dd3fc' if is_main else P5
    txt(ex + ew/2, P5Y + P5H - 0.95, name, size=10, color=nc, weight='bold', zorder=4)
    for j, line in enumerate(lines):
        if line:
            txt(ex + ew/2, P5Y + P5H - 1.32 - j*0.30, line, size=8.5, color=DIM, zorder=4)
    ex += ew + 0.35

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
out = Path(__file__).parent / 'architecture.png'
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print(f'Saved: {out}')
