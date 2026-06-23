# fraud_graph.py
import pandas as pd
import networkx as nx
from pyvis.network import Network

# ----------------------------------------------------------------------
# OPTIONAL: import Sentinel Graph SDK – will be used only if available
# ----------------------------------------------------------------------
try:
    from sentinelgraph import FraudRingDetector   # type: ignore
    SENTINEL_AVAILABLE = True
except Exception:          # pragma: no‑cover
    SENTINEL_AVAILABLE = False


# ----------------------------------------------------------------------
# Helper: turn the transaction dataframe into a graph of accounts
# ----------------------------------------------------------------------
def build_transaction_graph(df: pd.DataFrame) -> nx.Graph:
    """
    The CSV you posted does NOT have explicit sender/receiver columns.
    For a demo we create a static node called "💳 Your Account" and connect it
    to the merchant name that appears in the *description* column.
    """
    # Ensure amount is numeric – any bad rows become NaN → drop them
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    G = nx.Graph()

    USER = "💳 Your Account"
    # Create the two columns that the rest of the code expects
    df["source_account"] = USER
    df["target_account"] = df["description"].astype(str)

    for _, row in df.iterrows():
        src = row["source_account"]
        tgt = row["target_account"]
        weight = float(row["amount"])

        # Add or update a weighted edge
        if G.has_edge(src, tgt):
            G[src][tgt]["weight"] += weight
        else:
            G.add_edge(src, tgt, weight=weight)

    return G


# ----------------------------------------------------------------------
# Main function – detects fraud rings and returns a PyVis HTML canvas
# ----------------------------------------------------------------------
def detect_fraud_rings(
    df: pd.DataFrame,
    min_cycle_len: int = 3,
    min_weight: float = 10_000,
) -> dict:
    """
    Returns:
        - "graph_html": HTML string (embedding ready for Streamlit)
        - "rings":     list of rings (each ring = list of node IDs)
        - "message":   short human‑readable text
    """
    G = build_transaction_graph(df)

    # ------------------------------------------------- ring detection
    if SENTINEL_AVAILABLE:
        detector = FraudRingDetector(
            min_cycle_length=min_cycle_len,
            min_edge_weight=min_weight,
        )
        rings = detector.find_rings(G)                     # list[List[str]]
    else:
        # Fallback: look for any simple cycle with enough nodes
        rings = [
            list(cycle)
            for cycle in nx.cycle_basis(G)
            if len(cycle) >= min_cycle_len
        ]

    # ------------------------------------------------- visualisation (PyVis)
    net = Network(height="600px", width="100%", notebook=False)
    net.from_nx(G)

    # Highlight nodes that belong to a ring
    ring_nodes = {n for ring in rings for n in ring}
    for node in net.nodes:
        if node["id"] in ring_nodes:
            node["color"] = "red"
            node["borderWidth"] = 2
            node["title"] = "🚨 Suspected fraud node"

    # Thicken/colour expensive edges – safe get() with default = 0
    for edge in net.edges:
        src, tgt = edge["from"], edge["to"]
        weight = G[src][tgt].get("weight", 0)   # <-- safe access
        if weight > min_weight:
            edge["width"] = 3
            edge["color"] = "orange"

    graph_html = net.generate_html()

    # ------------------------------------------------- friendly message
    if rings:
        message = f"🔎 Detected **{len(rings)}** suspicious ring(s). Click a red node for details."
    else:
        message = "✅ No fraud rings were detected with the current thresholds."

    return {"graph_html": graph_html, "rings": rings, "message": message}