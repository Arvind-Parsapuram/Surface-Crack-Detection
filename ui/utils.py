from .config import CLASSES, SEVERITY_ORDER, SEVERITY_COLOR, ACCENT

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def compute_stats(history):
    total = len(history)
    cracks = sum(1 for h in history if h.get("predicted_class", "").lower() != "no crack")
    no_cracks = total - cracks
    avg_conf = (sum(h.get("confidence", 0) for h in history) / total) if total else 0.0
    return total, cracks, no_cracks, avg_conf


def class_distribution(history):
    counts = {c: 0 for c in CLASSES}
    for h in history:
        cls = h.get("predicted_class", "")
        for c in CLASSES:
            if c.lower() in cls.lower():
                counts[c] += 1
                break
    return counts


def severity_distribution(history):
    counts = {s: 0 for s in SEVERITY_ORDER}
    for h in history:
        sev = h.get("severity_label")
        if sev in counts:
            counts[sev] += 1
    total = sum(counts.values())
    return counts, total


def donut_chart(counts):
    labels = [k for k, v in counts.items() if v > 0]
    values = [v for v in counts.values() if v > 0]
    if not values or not PLOTLY_AVAILABLE:
        return None
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.6,
        marker=dict(colors=["#6C5CE7", "#00b894", "#fdcb6e", "#e17055"]),
        textinfo="none",
    )])
    fig.update_layout(
        showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=220,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
