import json
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import plotly.graph_objects as go
import pandas as pd

# ============================================================
# 1. KONFIGURASI APLIKASI
# ============================================================
st.set_page_config(
    page_title="Network Blackout",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 2. TEMA VISUAL
# ============================================================
st.markdown("""
<style>

:root {
    --bg: #08060D;
    --panel: #120C1B;
    --panel2: #191025;
    --border: #59452B;
    --purple: #B832F0;
    --lavender: #DDA5FF;
    --text: #F6EEFC;
    --muted: #B7A6C4;
    --green: #F4D77A;
    --red: #FF647C;
}

/* FRAME UTAMA JUDUL */
.network-banner {
    background:
        radial-gradient(
            ellipse at 90% 10%,
            rgba(244, 215, 122, 0.13),
            transparent 42%
        ),
        linear-gradient(135deg, #171020, #100B17);

    border: 1px solid #B99B52;
    border-radius: 22px;
    padding: 30px;
    margin: 8px 0 26px 0;
    box-shadow: 0 8px 28px rgba(244, 215, 122, 0.08);
}

.network-banner .project-label {
    color: #F4D77A;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 10px;
}

.network-banner .banner-tag {
    display: inline-block;
    border: 1px solid #8D7540;
    border-radius: 30px;
    padding: 6px 12px;
    color: #F4D77A;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.network-banner h1 {
    color: #FFF8E5 !important;
    font-size: clamp(30px, 4vw, 46px);
    line-height: 1.15;
    margin: 5px 0 12px 0;
}

.network-banner h1 span {
    color: #F4D77A;
}

.network-banner p {
    color: #E4D7ED;
    line-height: 1.8;
    margin-bottom: 10px;
}

.network-banner .banner-features {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 18px;
}

.network-banner .banner-feature {
    color: #F4D77A;
    background: rgba(244, 215, 122, 0.08);
    border: 1px solid rgba(244, 215, 122, 0.3);
    border-radius: 20px;
    padding: 7px 11px;
    font-size: 11px;
}

.network-banner .network-credit {
    color: #D5C5A0;
    font-size: 12px;
    border-left: 3px solid #F4D77A;
    padding: 5px 0 5px 12px;
    margin-top: 22px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. BANNER UTAMA
# ============================================================

st.markdown("""
<div class="network-banner">

<div class="banner-tag">
    🌐 GRAPH SIMULATION PROJECT
</div>

<h1>NETWORK <span>BLACKOUT</span></h1>

<p style="font-size:18px;">
    Simulasi dan Analisis Kegagalan Jaringan
</p>

<p>
    Pelajari bagaimana kegagalan router memengaruhi konektivitas
    komputer menuju server. Amati perubahan topologi, identifikasi
    perangkat yang kehilangan akses, dan bandingkan dampak
    kegagalan pada setiap router.
</p>

<div class="banner-features">
    <span class="banner-feature">◈ Visualisasi Graf</span>
    <span class="banner-feature">◈ Simulasi Kegagalan</span>
    <span class="banner-feature">◈ Animasi Jaringan</span>
    <span class="banner-feature">◈ Analisis Konektivitas</span>
</div>

<div class="network-credit">
    Developed by <b>Azzah Fatimatu Zahrah</b><br>
    240601110019
</div>

</div>
""", unsafe_allow_html=True)

# ============================================================
# 4. MEMBANGUN TOPOLOGI JARINGAN
# ============================================================
@st.cache_resource
def create_network():
    graph = nx.Graph()

    devices = {
        "S": {"type": "server", "label": "Server"},
        "R1": {"type": "router", "label": "Router 1"},
        "R2": {"type": "router", "label": "Router 2"},
        "R3": {"type": "router", "label": "Router 3"},
        "R4": {"type": "router", "label": "Router 4"},
        "R5": {"type": "router", "label": "Router 5"},
        **{
            f"C{i}": {
                "type": "computer",
                "label": f"Komputer {i}"
            }
            for i in range(1, 10)
        },
    }

    graph.add_nodes_from(
        (node, attrs) for node, attrs in devices.items()
    )

    connections = [
        ("S", "R1"),
        ("R1", "R2"),
        ("R1", "R3"),
        ("R2", "R3"),
        ("R2", "R4"),
        ("R3", "R5"),
        ("R2", "C1"),
        ("R2", "C2"),
        ("R4", "C3"),
        ("R4", "C4"),
        ("R3", "C5"),
        ("R3", "C6"),
        ("R5", "C7"),
        ("R5", "C8"),
        ("R5", "C9"),
    ]

    graph.add_edges_from(connections)
    return graph


G = create_network()
SOURCE = "S"
ROUTER_OPTIONS = ["R1", "R2", "R3", "R4", "R5"]

POSITIONS = {
    "S": (0, 2),
    "R1": (1, 2),
    "R2": (2, 3),
    "R3": (2, 1),
    "R4": (3, 4),
    "R5": (3, 0),
    "C1": (4, 4.5),
    "C2": (4, 3.5),
    "C3": (4.5, 4),
    "C4": (4.5, 3),
    "C5": (4, 1.5),
    "C6": (4, 0.5),
    "C7": (5, 1),
    "C8": (5, 0),
    "C9": (5.5, 0.5),
}


# ============================================================
# 5. ANALISIS KEGAGALAN ROUTER
# ============================================================
def analyze_failure(router_failed):
    graph_after = G.copy()

    if router_failed in graph_after:
        graph_after.remove_node(router_failed)

    if SOURCE in graph_after:
        reachable = set(
            nx.node_connected_component(graph_after, SOURCE)
        )
    else:
        reachable = set()

    computers = [
        node for node, data in G.nodes(data=True)
        if data["type"] == "computer"
    ]

    connected = [
        node for node in computers
        if node in reachable
    ]

    disconnected = [
        node for node in computers
        if node not in reachable
    ]

    components = list(nx.connected_components(graph_after))

    return {
        "graph": graph_after,
        "reachable": reachable,
        "connected": connected,
        "disconnected": disconnected,
        "components": components,
    }


# ============================================================
# 6. VISUALISASI GRAF PLOTLY
# ============================================================
def draw_network(router_failed=None, step=0):
    fig = go.Figure()

    if step == 0:
        graph_view = G.copy()
        reachable = set(G.nodes)
    else:
        result = analyze_failure(router_failed)
        graph_view = result["graph"]
        reachable = result["reachable"]

    active_x, active_y = [], []
    inactive_x, inactive_y = [], []

    for u, v in graph_view.edges():
        x0, y0 = POSITIONS[u]
        x1, y1 = POSITIONS[v]

        if u in reachable and v in reachable:
            target_x, target_y = active_x, active_y
        else:
            target_x, target_y = inactive_x, inactive_y

        target_x.extend([x0, x1, None])
        target_y.extend([y0, y1, None])

    if inactive_x:
        fig.add_trace(go.Scatter(
            x=inactive_x,
            y=inactive_y,
            mode="lines",
            line=dict(
                color="#6B536F",
                width=2,
                dash="dot"
            ),
            hoverinfo="skip",
            name="Jalur tanpa akses server",
        ))

    if active_x:
        fig.add_trace(go.Scatter(
            x=active_x,
            y=active_y,
            mode="lines",
            line=dict(color="#A94BDB", width=2.5),
            hoverinfo="skip",
            name="Koneksi ke server",
        ))

    groups = {
        "Server": {
            "nodes": [],
            "color": "#F5C451",
            "symbol": "diamond",
        },
        "Router aktif": {
            "nodes": [],
            "color": "#B832F0",
            "symbol": "square",
        },
        "Komputer terhubung": {
            "nodes": [],
            "color": "#38D996",
            "symbol": "circle",
        },
        "Komputer terputus": {
            "nodes": [],
            "color": "#FF647C",
            "symbol": "circle",
        },
    }

    for node, data in graph_view.nodes(data=True):
        if data["type"] == "server":
            group = "Server"
        elif data["type"] == "router":
            group = "Router aktif"
        elif node in reachable:
            group = "Komputer terhubung"
        else:
            group = "Komputer terputus"

        groups[group]["nodes"].append(node)

    for group_name, info in groups.items():
        nodes = info["nodes"]

        if not nodes:
            continue

        fig.add_trace(go.Scatter(
            x=[POSITIONS[n][0] for n in nodes],
            y=[POSITIONS[n][1] for n in nodes],
            mode="markers+text",
            text=nodes,
            textposition="bottom center",
            textfont=dict(color="#F6EEFC", size=11),
            marker=dict(
                size=25 if group_name == "Server" else 21,
                color=info["color"],
                symbol=info["symbol"],
                line=dict(color="#FFFFFF", width=1),
            ),
            name=group_name,
            customdata=[G.nodes[n]["label"] for n in nodes],
            hovertemplate="%{customdata}<extra></extra>",
        ))

    if step > 0 and router_failed in POSITIONS:
        x, y = POSITIONS[router_failed]

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            text=[router_failed + " MATI"],
            textposition="top center",
            textfont=dict(color="#FF8797", size=11),
            marker=dict(
                size=29,
                color="#FF647C",
                symbol="x",
                line=dict(color="#FF647C", width=3),
            ),
            name="Router gagal",
            hovertemplate=(
                "Router gagal: "
                + router_failed
                + "<extra></extra>"
            ),
        ))

    if step == 0:
        title = "Kondisi Awal Jaringan"
    elif step == 1:
        title = f"Simulasi Kegagalan Router {router_failed}"
    else:
        title = f"Analisis Dampak Router {router_failed}"

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color="#DDA5FF", size=19),
            x=0.02,
        ),
        height=560,
        autosize=True,
        plot_bgcolor="#0C0812",
        paper_bgcolor="#0C0812",
        font=dict(color="#F6EEFC", size=11),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.10,
            x=0.02,
            font=dict(color="#E4D7ED", size=10),
        ),
        margin=dict(l=20, r=20, t=60, b=95),
        xaxis=dict(
            visible=False,
            range=[-0.5, 6.3],
            fixedrange=True,
        ),
        yaxis=dict(
            visible=False,
            range=[-0.8, 5.2],
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1,
        ),
    )

    return fig


# ============================================================
# 7. SIDEBAR PENGATURAN
# ============================================================
with st.sidebar:
    st.markdown("## 🌐 Network Blackout")
    st.caption("Panel pengaturan simulasi")
    st.divider()

    if st.button("↺ Reset simulasi", use_container_width=True):
        st.session_state["router_failed"] = "R3"
        st.session_state["stage"] = "Kondisi awal"
        st.rerun()

    st.markdown("### ⚙️ Pengaturan")

    router_failed = st.selectbox(
        "Pilih router yang akan dimatikan",
        ROUTER_OPTIONS,
        format_func=lambda r: f"{r} — Router {r[1]}",
        key="router_failed",
        help="Pilih router untuk melihat perubahan konektivitas.",
    )

    stage_labels = [
        "Kondisi awal",
        "Router dimatikan",
        "Analisis konektivitas",
    ]

    stage_label = st.radio(
        "Tahap simulasi",
        stage_labels,
        key="stage",
        help="Pilih kondisi jaringan yang ingin diamati.",
    )

    step = stage_labels.index(stage_label)

    st.divider()
    st.markdown("### 📖 Petunjuk")

    st.markdown("""
    <div class="small-note">
        <b>1.</b> Pilih router yang ingin diuji.<br><br>
        <b>2.</b> Pilih tahap simulasi.<br><br>
        <b>3.</b> Amati perubahan warna perangkat.<br><br>
        <b>4.</b> Baca hasil analisis untuk mengetahui
        komputer mana yang kehilangan akses ke server.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🎨 Legenda")

    st.markdown("""
    <div class="small-note">
        🟡 Server<br>
        🟣 Router aktif<br>
        🟢 Komputer terhubung<br>
        🔴 Router gagal / perangkat terputus<br>
        ┄ Jalur tanpa akses ke server
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("Network Blackout · Graph Simulation")


# ============================================================
# 8. STATUS DAN METRIK
# ============================================================
result = analyze_failure(router_failed)

if step == 0:
    connected_count = 9
    disconnected_count = 0
    component_count = nx.number_connected_components(G)
    status_text = "Kondisi normal"
else:
    connected_count = len(result["connected"])
    disconnected_count = len(result["disconnected"])
    component_count = len(result["components"])
    status_text = (
        "Kegagalan disimulasikan"
        if step == 1
        else "Analisis selesai"
    )

st.markdown("## Dashboard Jaringan")

st.caption(
    "Pantau kondisi jaringan dan dampak kegagalan router "
    "berdasarkan topologi graf."
)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Total perangkat",
    G.number_of_nodes(),
    help="Server, router, dan komputer dalam topologi.",
)

metric2.metric(
    "Komputer terhubung",
    connected_count,
    delta=f"{connected_count}/9 komputer",
    delta_color="normal",
)

metric3.metric(
    "Komputer terputus",
    disconnected_count,
    delta=(
        "Kehilangan akses server"
        if disconnected_count
        else "Tidak ada"
    ),
    delta_color="inverse" if disconnected_count else "off",
)

metric4.metric(
    "Komponen jaringan",
    component_count,
    help="Kelompok perangkat yang masih saling terhubung.",
)

if step == 0:
    st.success(
        "Jaringan berada pada kondisi awal. "
        "Belum ada router yang dimatikan."
    )
elif step == 1:
    st.warning(
        f"Simulasi kegagalan {router_failed} aktif. "
        "Amati perangkat yang masih memiliki jalur menuju server."
    )
else:
    st.info(
        f"Analisis konektivitas untuk kegagalan {router_failed} "
        "ditampilkan di bawah."
    )


# ============================================================
# 9. VISUALISASI TOPOLOGI
# ============================================================
st.markdown("## 🕸️ Visualisasi Topologi")

st.caption(
    "Arahkan kursor ke perangkat untuk melihat namanya. "
    "Warna menunjukkan status konektivitas."
)

st.plotly_chart(
    draw_network(router_failed, step),
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "responsive": True,
    },
    key="network_plot",
)


# ============================================================
# 10. ANIMASI JARINGAN SVG
# ============================================================
def make_smooth_html(router_failed, step):
    analysis = analyze_failure(router_failed) if step > 0 else None

    graph_view = G.copy() if step == 0 else analysis["graph"]
    reachable = (
        set(G.nodes)
        if step == 0
        else analysis["reachable"]
    )

    nodes = []

    for node, attrs in G.nodes(data=True):
        x, y = POSITIONS[node]

        nodes.append({
            "id": node,
            "x": float(x),
            "y": float(y),
            "type": attrs["type"],
            "active": node in reachable,
            "failed": node == router_failed and step > 0,
        })

    edges = [
        {"source": u, "target": v}
        for u, v in graph_view.edges()
    ]

    payload = json.dumps({
        "nodes": nodes,
        "edges": edges,
        "step": step,
    }).replace("</", "<\\/")

    html = r'''
<div style="
    font-family:Arial,sans-serif;
    color:#F6EEFC;
    background:#0C0812;
    padding:14px;
    border:1px solid #39204A;
    border-radius:14px;
    box-sizing:border-box;
    width:100%;
">
    <div style="
        display:flex;
        align-items:center;
        flex-wrap:wrap;
        gap:9px;
        margin-bottom:12px;
    ">
        <button id="play" style="
            background:#A900DE;
            color:white;
            border:1px solid #C65AFF;
            border-radius:8px;
            padding:9px 16px;
            cursor:pointer;
            font-weight:bold;
        ">▶ Play</button>

        <button id="pause" style="
            background:#211329;
            color:white;
            border:1px solid #6B2B86;
            border-radius:8px;
            padding:9px 16px;
            cursor:pointer;
        ">Ⅱ Pause</button>

        <button id="resetAnim" style="
            background:#15101C;
            color:#DDA5FF;
            border:1px solid #543468;
            border-radius:8px;
            padding:9px 14px;
            cursor:pointer;
        ">↺ Ulangi</button>

        <span id="status" style="
            color:#DDA5FF;
            font-size:12px;
        ">Animasi siap</span>
    </div>

    <div style="width:100%;overflow:hidden;">
        <svg id="network"
             viewBox="0 0 900 520"
             preserveAspectRatio="xMidYMid meet"
             style="
                 display:block;
                 width:100%;
                 height:auto;
                 background:
                   radial-gradient(ellipse at center,
                   #191025 0%, #0C0812 75%);
                 border:1px solid #39204A;
                 border-radius:10px;
             ">
        </svg>
    </div>

    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:12px;
        color:#CBB8D8;
        font-size:11px;
        margin-top:12px;
        line-height:1.8;
    ">
        <span>🟡 Server</span>
        <span>🟣 Router aktif</span>
        <span>🟢 Komputer terhubung</span>
        <span>🔴 Router gagal / komputer terputus</span>
    </div>

    <div style="
        font-size:11px;
        color:#9F8BAC;
        margin-top:5px;
    ">
        Titik putih bergerak menggambarkan aliran data pada jalur aktif.
    </div>
</div>

<script>
const data = PAYLOAD_PLACEHOLDER;
const svg = document.getElementById("network");
const ns = "http://www.w3.org/2000/svg";

const X = x => 65 + x * 145;
const Y = y => 455 - y * 87;

const byId = Object.fromEntries(
    data.nodes.map(n => [n.id, n])
);

function element(tag, attrs, parent = svg) {
    const el = document.createElementNS(ns, tag);

    Object.entries(attrs).forEach(([key, value]) => {
        el.setAttribute(key, value);
    });

    parent.appendChild(el);
    return el;
}

// Menggambar koneksi di belakang perangkat.
data.edges.forEach(edge => {
    const a = byId[edge.source];
    const b = byId[edge.target];
    const active = a.active && b.active;

    element("line", {
        x1: X(a.x),
        y1: Y(a.y),
        x2: X(b.x),
        y2: Y(b.y),
        stroke: active ? "#8540A5" : "#4A3B52",
        "stroke-width": active ? 3 : 2,
        "stroke-dasharray": active ? "none" : "5 5",
        "stroke-linecap": "round"
    });
});

// Menggambar perangkat dan label.
data.nodes.forEach(node => {
    const color = node.failed
        ? "#FF647C"
        : node.type === "server"
            ? "#F5C451"
            : node.type === "router"
                ? "#B832F0"
                : node.active
                    ? "#38D996"
                    : "#FF647C";

    const radius = node.type === "server" ? 19 : 14;

    if (node.failed) {
        element("circle", {
            cx: X(node.x),
            cy: Y(node.y),
            r: 25,
            fill: "none",
            stroke: "#FF647C",
            "stroke-width": 2,
            "stroke-dasharray": "5 4"
        });
    }

    element("circle", {
        cx: X(node.x),
        cy: Y(node.y),
        r: radius + 5,
        fill: color,
        opacity: 0.12
    });

    element("circle", {
        cx: X(node.x),
        cy: Y(node.y),
        r: radius,
        fill: color,
        stroke: "#FFFFFF",
        "stroke-width": 1.3
    });

    const text = element("text", {
        x: X(node.x),
        y: Y(node.y) + 4,
        "text-anchor": "middle",
        fill: "#FFFFFF",
        "font-size": node.type === "server" ? 12 : 10,
        "font-weight": "bold"
    });

    text.textContent = node.id;

    const label = element("text", {
        x: X(node.x),
        y: Y(node.y) + radius + 16,
        "text-anchor": "middle",
        fill: node.failed ? "#FF8797" : "#DDA5FF",
        "font-size": 10,
        "font-family": "Arial, sans-serif"
    });

    label.textContent = node.failed
        ? "MATI"
        : node.type === "server"
            ? "Server"
            : node.type === "router"
                ? "Router"
                : "";
});

// Membuat partikel yang bergerak pada jalur aktif.
const particles = [];

data.edges.forEach(edge => {
    const a = byId[edge.source];
    const b = byId[edge.target];

    const particle = element("circle", {
        r: 4.5,
        fill: "#FFFFFF",
        stroke: "#DDA5FF",
        "stroke-width": 1,
        opacity: 0
    });

    particles.push({
        p: particle,
        a: a,
        b: b,
        t: Math.random()
    });
});

let running = false;
let frame = null;

function animate() {
    if (!running) return;

    particles.forEach(particle => {
        particle.t = (particle.t + 0.0045) % 1;

        const active =
            particle.a.active && particle.b.active;

        particle.p.setAttribute(
            "opacity",
            active ? 1 : 0
        );

        particle.p.setAttribute(
            "cx",
            X(
                particle.a.x
                + (particle.b.x - particle.a.x) * particle.t
            )
        );

        particle.p.setAttribute(
            "cy",
            Y(
                particle.a.y
                + (particle.b.y - particle.a.y) * particle.t
            )
        );
    });

    frame = requestAnimationFrame(animate);
}

function pauseAnimation(message) {
    running = false;

    if (frame !== null) {
        cancelAnimationFrame(frame);
        frame = null;
    }

    document.getElementById("status").textContent = message;
}

document.getElementById("play").onclick = () => {
    if (!running) {
        running = true;

        document.getElementById("status").textContent =
            "Animasi berjalan";

        animate();
    }
};

document.getElementById("pause").onclick = () => {
    pauseAnimation("Animasi dijeda");
};

document.getElementById("resetAnim").onclick = () => {
    pauseAnimation("Animasi diulang");

    particles.forEach(particle => {
        particle.t = Math.random();
        particle.p.setAttribute("opacity", 0);
    });
};
</script>
'''

    return html.replace("PAYLOAD_PLACEHOLDER", payload)


st.markdown("## 🎬 Animasi Jaringan")

st.caption(
    "Gunakan Play untuk menjalankan animasi aliran data, "
    "Pause untuk menjeda, dan Ulangi untuk mengatur ulang partikel."
)

components.html(
    make_smooth_html(router_failed, step),
    height=690,
    scrolling=False,
)


# ============================================================
# 11. ANALISIS OTOMATIS
# ============================================================
st.markdown("## 🔎 Hasil Analisis Konektivitas")

if step == 0:
    st.markdown("""
    <div class="section-card">
        <span class="status-pill">● Jaringan normal</span>
        <p>
            Seluruh sembilan komputer memiliki jalur menuju server.
            Belum ada router yang dinonaktifkan, sehingga topologi
            ditampilkan dalam kondisi awal.
        </p>
        <p>
            Pilih router dan ubah tahap simulasi di panel kiri untuk
            mengamati perubahan konektivitas setelah kegagalan.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    failed_neighbors = list(G.neighbors(router_failed))

    disconnected_names = [
        G.nodes[n]["label"] for n in result["disconnected"]
    ]

    connected_names = [
        G.nodes[n]["label"] for n in result["connected"]
    ]

    if disconnected_count == 0:
        impact_text = (
            f"Router {router_failed} gagal, tetapi seluruh komputer "
            "masih mempunyai jalur menuju server. Pada topologi ini, "
            "jalur alternatif menjaga konektivitas komputer."
        )
    else:
        impact_text = (
            f"Kegagalan {router_failed} menyebabkan "
            f"{disconnected_count} dari 9 komputer kehilangan akses "
            "ke server. Perangkat yang terputus tidak lagi berada "
            "dalam komponen graf yang sama dengan server."
        )

    st.markdown(f"""
    <div class="section-card">
        <span class="status-pill">● {status_text}</span>
        <p>{impact_text}</p>
        <p>
            <b>Router yang gagal:</b> {router_failed}<br>
            <b>Perangkat yang terhubung langsung ke router:</b>
            {", ".join(failed_neighbors) if failed_neighbors else "Tidak ada"}<br>
            <b>Jumlah komponen setelah kegagalan:</b>
            {component_count}
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### 🟢 Komputer terhubung")

        if connected_names:
            st.success(", ".join(connected_names))
        else:
            st.info("Tidak ada komputer yang terhubung ke server.")

    with right:
        st.markdown("### 🔴 Komputer terputus")

        if disconnected_names:
            st.error(", ".join(disconnected_names))
        else:
            st.success("Tidak ada komputer yang kehilangan akses.")

    if step == 2:
        with st.expander("Lihat komponen jaringan setelah kegagalan"):
            for i, component in enumerate(
                result["components"],
                start=1
            ):
                members = sorted(component)
                server_present = SOURCE in component

                st.markdown(
                    f"**Komponen {i}** — "
                    f"{'Memuat server' if server_present else 'Tidak terhubung ke server'}"
                )

                st.write(", ".join(members))


# ============================================================
# 12. PERBANDINGAN SKENARIO KEGAGALAN
# ============================================================
st.markdown("## 📊 Perbandingan Skenario")

st.caption(
    "Bandingkan dampak jika masing-masing router gagal."
)

comparison = []

for router in ROUTER_OPTIONS:
    scenario = analyze_failure(router)

    comparison.append({
        "Router gagal": router,
        "Komputer terhubung": len(scenario["connected"]),
        "Komputer terputus": len(scenario["disconnected"]),
        "Jumlah komponen": len(scenario["components"]),
    })

comparison_df = pd.DataFrame(comparison)

st.dataframe(
    comparison_df,
    hide_index=True,
    use_container_width=True,
)

fig_compare = go.Figure()

fig_compare.add_trace(go.Bar(
    x=comparison_df["Router gagal"],
    y=comparison_df["Komputer terhubung"],
    name="Komputer terhubung",
    marker_color="#F4D77A",
))

fig_compare.add_trace(go.Bar(
    x=comparison_df["Router gagal"],
    y=comparison_df["Komputer terputus"],
    name="Komputer terputus",
    marker_color="#FF647C",
))

fig_compare.update_layout(
    barmode="group",
    title=dict(
        text="Dampak Kegagalan terhadap Komputer",
        font=dict(color="#DDA5FF", size=18),
    ),
    height=360,
    paper_bgcolor="#0C0812",
    plot_bgcolor="#0C0812",
    font=dict(color="#F6EEFC"),
    margin=dict(l=20, r=20, t=60, b=35),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        x=0,
    ),
    xaxis=dict(title="Router yang gagal"),
    yaxis=dict(
        title="Jumlah komputer",
        range=[0, 9],
        dtick=1,
        gridcolor="#39204A",
    ),
)

st.plotly_chart(
    fig_compare,
    use_container_width=True,
    config={"displayModeBar": False},
)

# ============================================================
# 13. INTERPRETASI DAN BATASAN
# ============================================================
st.markdown("## 📘 Memahami Hasil Simulasi")

with st.container(border=True):
    st.markdown("### 1. Bagaimana konektivitas dihitung?")
    st.write(
        "Jaringan direpresentasikan sebagai graf: perangkat menjadi "
        "simpul (node), sedangkan koneksi antarperangkat menjadi sisi "
        "(edge). Ketika router gagal, simpul router tersebut dihapus "
        "dari salinan graf. Program kemudian mencari komponen "
        "terhubung yang memuat server."
    )

    st.markdown("### 2. Apa arti komputer terhubung?")
    st.write(
        "Komputer dianggap terhubung apabila masih berada dalam "
        "komponen graf yang sama dengan server. Komputer yang berada "
        "di komponen lain dianggap kehilangan akses ke server, "
        "walaupun mungkin masih terhubung dengan perangkat lain."
    )

    st.markdown(
        "### 3. Mengapa kegagalan router memberikan dampak berbeda?"
    )
    st.write(
        "Setiap router memiliki posisi dan koneksi yang berbeda. "
        "Router yang menjadi bagian penting jalur menuju server "
        "dapat menyebabkan lebih banyak komputer kehilangan akses. "
        "Jalur alternatif dapat membantu mempertahankan konektivitas."
    )

    st.markdown("### 4. Apa batasan model ini?")
    st.write(
        "Simulasi ini mengukur keterhubungan topologi, bukan kinerja "
        "jaringan nyata. Kapasitas bandwidth, latensi, kehilangan "
        "paket, protokol routing, dan proses pemulihan otomatis "
        "belum dimodelkan."
    )

st.warning(
    "Hasil berlaku untuk topologi simulasi yang didefinisikan "
    "dalam kode ini. Hasil bukan pengukuran jaringan fisik."
)
