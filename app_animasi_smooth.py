
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Network Blackout",
    page_icon="🌐",
    layout="wide"
)

# ==========================================
# 2. STYLE
# ==========================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b0617, #160b2c, #090512);
    color: #f4edff;
}

[data-testid="stSidebar"] {
    background: #120a21;
    border-right: 1px solid #48276c;
}

h1, h2, h3 {
    color: #d8b4fe !important;
}

p, label, span {
    color: #eee5ff;
}

.network-banner {
    background: linear-gradient(120deg, #291044, #54218a, #281044);
    border: 1px solid #9b5de5;
    border-radius: 18px;
    padding: 26px;
    margin-bottom: 24px;
    box-shadow: 0 0 22px #8b5cf633;
}

.network-banner h1 {
    color: #ffffff !important;
    margin: 0;
}

.network-banner p {
    color: #e9d5ff;
    margin-bottom: 0;
}

.section-card {
    background: #170d27;
    border: 1px solid #49266b;
    border-radius: 14px;
    padding: 18px;
    margin: 10px 0;
}

div[data-testid="stMetric"] {
    background: #1b1030;
    border: 1px solid #57327c;
    border-radius: 12px;
    padding: 14px;
}

div[data-testid="stMetric"] label {
    color: #c4a5fd !important;
}

div[data-testid="stMetricValue"] {
    color: #f5eaff !important;
}

.stButton button {
    background: #7c3aed;
    color: white;
    border: none;
    border-radius: 10px;
}

.stButton button:hover {
    background: #9333ea;
    color: white;
    border: 1px solid #d8b4fe;
}

hr {
    border-color: #48276c;
}

.network-credit {
    text-align: center;
    color: #a78bfa;
    padding: 20px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BANNER
# ==========================================

st.markdown("""
<div class="network-banner">
    <div style="
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 3px;
        color: #c084fc;
        margin-bottom: 8px;
    ">PROYEK 05</div>

    <h1>🌐 Network Blackout</h1>

    <p>
        Simulasi kegagalan router, analisis konektivitas,
        dan visualisasi dampak gangguan pada jaringan komputer.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. MEMBUAT TOPOLOGI JARINGAN
# ==========================================

G = nx.Graph()

nodes = {
    "S": {"type": "server", "label": "Server"},
    "R1": {"type": "router", "label": "Router 1"},
    "R2": {"type": "router", "label": "Router 2"},
    "R3": {"type": "router", "label": "Router 3"},
    "R4": {"type": "router", "label": "Router 4"},
    "R5": {"type": "router", "label": "Router 5"},
    "C1": {"type": "computer", "label": "PC 1"},
    "C2": {"type": "computer", "label": "PC 2"},
    "C3": {"type": "computer", "label": "PC 3"},
    "C4": {"type": "computer", "label": "PC 4"},
    "C5": {"type": "computer", "label": "PC 5"},
    "C6": {"type": "computer", "label": "PC 6"},
    "C7": {"type": "computer", "label": "PC 7"},
    "C8": {"type": "computer", "label": "PC 8"},
    "C9": {"type": "computer", "label": "PC 9"},
}

for node, attributes in nodes.items():
    G.add_node(node, **attributes)

edges = [
    ("S", "R1"),
    ("S", "R2"),
    ("S", "R3"),
    ("R1", "R2"),
    ("R2", "R3"),
    ("R1", "R4"),
    ("R2", "R4"),
    ("R2", "R5"),
    ("R3", "R5"),
    ("R1", "C1"),
    ("R1", "C2"),
    ("R2", "C3"),
    ("R2", "C4"),
    ("R3", "C5"),
    ("R3", "C6"),
    ("R4", "C7"),
    ("R4", "C8"),
    ("R5", "C9"),
]

G.add_edges_from(edges)

# Posisi node agar tampilan jaringan tetap rapi
pos = {
    "S": (0, 3),
    "R1": (-2, 2),
    "R2": (0, 2),
    "R3": (2, 2),
    "R4": (-1.5, 0.7),
    "R5": (1.5, 0.7),
    "C1": (-3, 0.5),
    "C2": (-2.5, -0.3),
    "C3": (-0.5, 0.2),
    "C4": (0.3, -0.3),
    "C5": (2.5, 0.5),
    "C6": (3, -0.3),
    "C7": (-2, -1),
    "C8": (-1, -1.3),
    "C9": (2, -1),
}

# ==========================================
# 5. ANALISIS KEGAGALAN
# ==========================================

def analyze_failure(router_failed):
    graph_test = G.copy()

    if router_failed != "Tidak ada":
        graph_test.remove_node(router_failed)

    if "S" in graph_test:
        reachable = nx.node_connected_component(graph_test, "S")
    else:
        reachable = set()

    computers = [f"C{i}" for i in range(1, 10)]

    connected = [
        computer for computer in computers
        if computer in reachable
    ]

    disconnected = [
        computer for computer in computers
        if computer not in reachable
    ]

    total = len(computers)
    connected_count = len(connected)
    disconnected_count = len(disconnected)

    availability = (
        connected_count / total * 100
        if total else 0
    )

    return {
        "graph": graph_test,
        "connected": connected,
        "disconnected": disconnected,
        "connected_count": connected_count,
        "disconnected_count": disconnected_count,
        "availability": availability,
    }

# ==========================================
# 6. VISUALISASI GRAF
# ==========================================

def draw_network(router_failed="Tidak ada"):
    result = analyze_failure(router_failed)
    graph_test = result["graph"]

    edge_x = []
    edge_y = []
    edge_colors = []

    for u, v in graph_test.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

        if u in result["connected"] or v in result["connected"]:
            edge_colors.append("#a78bfa")
        else:
            edge_colors.append("#57327c")

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            color="#8b5cf6",
            width=2
        ),
        hoverinfo="none",
        showlegend=False
    )

    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []

    for node in graph_test.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        if node == "S":
            node_text.append("Server")
            node_colors.append("#22c55e")
            node_sizes.append(30)

        elif node.startswith("R"):
            node_text.append(node)

            if node == router_failed:
                node_colors.append("#ef4444")
            else:
                node_colors.append("#a855f7")

            node_sizes.append(25)

        else:
            node_text.append(node)

            if node in result["connected"]:
                node_colors.append("#38bdf8")
            else:
                node_colors.append("#ef4444")

            node_sizes.append(17)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="bottom center",
        textfont=dict(
            color="#f3e8ff",
            size=11
        ),
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(
                color="#f5eaff",
                width=1
            )
        ),
        hovertext=node_text,
        hoverinfo="text",
        showlegend=False
    )

    fig = go.Figure(
        data=[edge_trace, node_trace]
    )

    fig.update_layout(
        height=570,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            visible=False,
            range=[-3.7, 3.7]
        ),
        yaxis=dict(
            visible=False,
            range=[-1.8, 3.7],
            scaleanchor="x",
            scaleratio=1
        ),
        showlegend=False
    )

    return fig

# ==========================================
# 7. SIDEBAR KONTROL
# ==========================================

st.sidebar.title("🎛️ Kontrol Simulasi")
st.sidebar.markdown("---")

router_options = [
    "Tidak ada",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
]

router_failed = st.sidebar.selectbox(
    "Pilih router yang mengalami kegagalan:",
    router_options,
    index=0
)

st.sidebar.markdown("""
### 🎨 Keterangan warna

🟢 Server utama

🟣 Router aktif

🔵 Komputer terhubung

🔴 Router gagal atau komputer terputus
""")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Pilih router untuk melihat perubahan konektivitas jaringan."
)

# ==========================================
# 8. HASIL ANALISIS
# ==========================================

result = analyze_failure(router_failed)

st.subheader("📊 Ringkasan Kondisi Jaringan")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Komputer",
    9
)

col2.metric(
    "Komputer Terhubung",
    result["connected_count"]
)

col3.metric(
    "Komputer Terputus",
    result["disconnected_count"]
)

col4.metric(
    "Ketersediaan",
    f"{result['availability']:.1f}%"
)

# ==========================================
# 9. VISUALISASI DAN ANIMASI
# ==========================================

st.markdown("---")
st.subheader("🖥️ Visualisasi Topologi Jaringan")

if router_failed == "Tidak ada":
    st.info(
        "Semua router dalam kondisi normal. "
        "Pilih router di sidebar untuk menyimulasikan kegagalan."
    )
else:
    st.warning(
        f"Simulasi kegagalan aktif pada router {router_failed}."
    )

left, right = st.columns([3, 1])

with left:
    st.plotly_chart(
        draw_network(router_failed),
        use_container_width=True
    )

with right:
    st.markdown("""
    <div class="section-card">
        <h3>📌 Status Simulasi</h3>
    """, unsafe_allow_html=True)

    if router_failed == "Tidak ada":
        st.success("Jaringan normal")
    else:
        st.error(f"{router_failed} gagal")

    st.markdown(
        f"""
        <div class="section-card">
            <p><b>Komputer terhubung:</b></p>
            <p>{result['connected_count']} dari 9</p>
            <p><b>Komputer terputus:</b></p>
            <p>{result['disconnected_count']} dari 9</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 10. ANIMASI STATUS
# ==========================================

st.markdown("---")
st.subheader("✨ Animasi Status Jaringan")

animation_color = (
    "#22c55e"
    if router_failed == "Tidak ada"
    else "#ef4444"
)

animation_title = (
    "JARINGAN NORMAL"
    if router_failed == "Tidak ada"
    else f"ROUTER {router_failed} MENGALAMI GANGGUAN"
)

animation_description = (
    "Seluruh komputer memiliki jalur koneksi ke server."
    if router_failed == "Tidak ada"
    else (
        f"{result['connected_count']} komputer masih terhubung "
        f"dan {result['disconnected_count']} komputer terputus."
    )
)

animation_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #11091f;
    color: #f3e8ff;
}
.panel {
    box-sizing: border-box;
    width: 100%;
    padding: 25px;
    border: 1px solid #6d28d9;
    border-radius: 16px;
    background: linear-gradient(135deg, #211036, #10091c);
    text-align: center;
}
.dot {
    display: inline-block;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    margin-right: 8px;
    background: STATUS_COLOR;
    animation: pulse 1.3s infinite;
}
h2 {
    color: STATUS_COLOR;
    font-size: 20px;
}
p {
    color: #e9d5ff;
    line-height: 1.6;
}
.track {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 24px 0;
    flex-wrap: wrap;
}
.node {
    padding: 12px 15px;
    border: 1px solid #a78bfa;
    border-radius: 10px;
    background: #32134e;
    animation: glow 2s infinite alternate;
}
.line {
    width: 35px;
    height: 3px;
    background: #a78bfa;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 STATUS_SHADOW; }
    70% { box-shadow: 0 0 0 12px transparent; }
    100% { box-shadow: 0 0 0 0 transparent; }
}
@keyframes glow {
    from { opacity: 0.65; }
    to { opacity: 1; }
}
</style>
</head>
<body>
<div class="panel">
    <div><span class="dot"></span><b>PEMANTAUAN JARINGAN</b></div>
    <h2>ANIMATION_TITLE</h2>
    <div class="track">
        <div class="node">Server</div>
        <div class="line"></div>
        <div class="node">Router</div>
        <div class="line"></div>
        <div class="node">Komputer</div>
    </div>
    <p>ANIMATION_DESCRIPTION</p>
</div>
</body>
</html>
"""

animation_html = (
    animation_html
    .replace("STATUS_COLOR", animation_color)
    .replace("STATUS_SHADOW", animation_color + "88")
    .replace("ANIMATION_TITLE", animation_title)
    .replace("ANIMATION_DESCRIPTION", animation_description)
)

components.html(
    animation_html,
    height=250,
    scrolling=False
)

# ==========================================
# 11. TABEL PERBANDINGAN
# ==========================================

st.markdown("---")
st.subheader("📋 Perbandingan Kondisi Jaringan")

comparison_rows = []

for router in router_options:
    router_result = analyze_failure(router)

    comparison_rows.append({
        "Kondisi": (
            "Normal"
            if router == "Tidak ada"
            else f"Router {router} gagal"
        ),
        "Komputer Terhubung": router_result["connected_count"],
        "Komputer Terputus": router_result["disconnected_count"],
        "Ketersediaan (%)": round(
            router_result["availability"],
            1
        )
    })

df_comparison = pd.DataFrame(comparison_rows)

st.dataframe(
    df_comparison,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 12. INTERPRETASI HASIL
# ==========================================

st.markdown("---")
st.subheader("🔎 Interpretasi Hasil")

if router_failed == "Tidak ada":
    st.markdown("""
    <div class="section-card">
        <h3>✅ Kondisi Normal</h3>
        <p>
            Dalam kondisi normal, seluruh komputer memiliki jalur
            konektivitas menuju server berdasarkan topologi graf.
            Tidak ada router yang sengaja dinonaktifkan dalam simulasi.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(
        f"""
        <div class="section-card">
            <h3>⚠️ Analisis Kegagalan Router {router_failed}</h3>
            <p>
                Setelah router {router_failed} dihapus dari graf,
                terdapat {result['connected_count']} komputer yang
                masih terhubung dengan server dan
                {result['disconnected_count']} komputer yang terputus.
            </p>
            <p>
                Hasil ini menunjukkan bahwa dampak kegagalan router
                bergantung pada posisi router dan ketersediaan jalur
                alternatif di dalam topologi jaringan.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("### 💡 Kesimpulan")

st.write(
    "Router yang memiliki peran penting dalam menghubungkan "
    "bagian jaringan dapat menyebabkan gangguan konektivitas "
    "ketika gagal. Jalur alternatif dapat membantu menjaga "
    "koneksi selama masih tersedia jalur dari komputer ke server."
)

st.warning(
    "Catatan: simulasi ini menghitung konektivitas berdasarkan "
    "topologi graf. Kapasitas jaringan, latensi, kehilangan paket, "
    "dan proses pemulihan otomatis belum dimodelkan."
)

# ==========================================
# 13. FOOTER
# ==========================================

st.markdown("""
<div class="network-credit">
    🌐 Network Blackout | Simulasi dan Analisis Kegagalan Jaringan
</div>
""", unsafe_allow_html=True)
