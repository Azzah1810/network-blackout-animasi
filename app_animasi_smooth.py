
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import json

st.set_page_config(
    page_title="Network Blackout",
    page_icon="🌐",
    layout="wide"
)
# ==========================================
# TEMA VISUAL NETWORK BLACKOUT
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: #FFFFFF;
}

[data-testid="stHeader"] {
    background-color: #000000;
}

[data-testid="stSidebar"] {
    background-color: #100B14;
    border-right: 1px solid #49235A;
}

h1, h2, h3 {
    color: #DDA5FF;
}

div[data-testid="stMetric"] {
    background: #100B14;
    border: 1px solid #49235A;
    border-radius: 12px;
    padding: 14px;
}

div.stButton > button {
    background: #A900DE;
    color: white;
    border: 1px solid #C412FF;
    border-radius: 9px;
}

div.stButton > button:hover {
    background: #C412FF;
    color: white;
}

.network-banner {
    background:
        radial-gradient(ellipse at 80% 50%,
            #42105F 0%, #180821 35%, #050505 75%);
    border: 1px solid #A900DE;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 24px;
}

.network-banner h1 {
    color: white;
    font-size: 42px;
    margin: 0;
}

.network-banner h1 span {
    color: #C412FF;
}

.network-banner p {
    color: #E8D9F0;
    line-height: 1.7;
}

.network-credit {
    color: #DDA5FF;
    font-size: 13px;
    border-left: 3px solid #C412FF;
    padding-left: 12px;
    margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# BANNER UTAMA
# ==========================================

st.markdown("""
st.markdown("""
<div class="network-banner">
    <div style="color:#C412FF; font-size:12px;
                letter-spacing:3px; font-weight:bold;">
        GRAPH SIMULATION PROJECT
    </div>

    <h1>NETWORK <span>BLACKOUT</span></h1>

    <p style="font-size:18px;">
        Simulasi dan Analisis Kegagalan Jaringan
    </p>

    <p>
        Mempelajari dampak kegagalan router terhadap
        konektivitas komputer ke server melalui visualisasi graf.
    </p>

    <div style="color:#DDA5FF; font-size:13px;">
        ◈ Visualisasi Graf &nbsp; | &nbsp;
        ◈ Simulasi Kegagalan &nbsp; | &nbsp;
        ◈ Analisis Konektivitas
    </div>

    <div class="network-credit">
        Developed by <b>Azzah Fatimatu Zahrah</b><br>
        240601110019
    </div>
</div>
""", unsafe_allow_html=True)
        ◈ Analisis Konektivitas
    </div>

    <div class="network-credit">
        Developed by <b>Azzah Fatimatu Zahrah</b><br>
        240601110019
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. MEMBANGUN TOPOLOGI JARINGAN
# ==========================================

@st.cache_resource
def create_network():
    graph = nx.Graph()

    devices = {
        "S":  {"type": "server",   "label": "Server"},
        "R1": {"type": "router",   "label": "Router 1"},
        "R2": {"type": "router",   "label": "Router 2"},
        "R3": {"type": "router",   "label": "Router 3"},
        "R4": {"type": "router",   "label": "Router 4"},
        "R5": {"type": "router",   "label": "Router 5"},
        "C1": {"type": "computer", "label": "Komputer 1"},
        "C2": {"type": "computer", "label": "Komputer 2"},
        "C3": {"type": "computer", "label": "Komputer 3"},
        "C4": {"type": "computer", "label": "Komputer 4"},
        "C5": {"type": "computer", "label": "Komputer 5"},
        "C6": {"type": "computer", "label": "Komputer 6"},
        "C7": {"type": "computer", "label": "Komputer 7"},
        "C8": {"type": "computer", "label": "Komputer 8"},
        "C9": {"type": "computer", "label": "Komputer 9"},
    }

    for node, attributes in devices.items():
        graph.add_node(node, **attributes)

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

POSITIONS = {
    "S":  (0, 2),
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

# ==========================================
# 2. PERHITUNGAN KEGAGALAN ROUTER
# ==========================================

def analyze_failure(router_failed):
    graph_after = G.copy()
    graph_after.remove_node(router_failed)

    reachable = set(
        nx.node_connected_component(graph_after, SOURCE)
    )

    computers = [
        node for node, data in G.nodes(data=True)
        if data["type"] == "computer"
    ]

    connected = [node for node in computers if node in reachable]
    disconnected = [
        node for node in computers if node not in reachable
    ]

    return {
        "graph": graph_after,
        "reachable": reachable,
        "connected": connected,
        "disconnected": disconnected,
        "components": list(nx.connected_components(graph_after)),
    }


# ==========================================
# 3. VISUALISASI JARINGAN INTERAKTIF
# ==========================================

def draw_network(router_failed=None, step=0):
    fig = go.Figure()

    if step == 0:
        graph_view = G.copy()
        reachable = set(G.nodes)
    else:
        result = analyze_failure(router_failed)
        graph_view = result["graph"]
        reachable = result["reachable"]

    # Gambar koneksi
    edge_x, edge_y = [], []

    for u, v in graph_view.edges():
        x0, y0 = POSITIONS[u]
        x1, y1 = POSITIONS[v]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="#9CA3AF", width=2),
        hoverinfo="skip",
        name="Koneksi",
    ))

    # Kelompokkan perangkat berdasarkan status
    groups = {
        "Server": {"nodes": [], "color": "#EAB308", "symbol": "diamond"},
        "Router aktif": {"nodes": [], "color": "#3B82F6", "symbol": "square"},
        "Komputer terhubung": {"nodes": [], "color": "#22C55E", "symbol": "circle"},
        "Tanpa akses server": {"nodes": [], "color": "#F87171", "symbol": "circle"},
    }

    for node, data in graph_view.nodes(data=True):
        if data["type"] == "server":
            group = "Server"
        elif data["type"] == "router":
            group = "Router aktif"
        elif node in reachable:
            group = "Komputer terhubung"
        else:
            group = "Tanpa akses server"

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
            marker=dict(
                size=24,
                color=info["color"],
                symbol=info["symbol"],
                line=dict(color="white", width=1)
            ),
            name=group_name,
            customdata=[
                G.nodes[n]["label"] for n in nodes
            ],
            hovertemplate="%{customdata}<extra></extra>",
        ))

    # Tampilkan lokasi router yang gagal
    if step > 0 and router_failed:
        x, y = POSITIONS[router_failed]

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            text=[router_failed + " MATI"],
            textposition="top center",
            marker=dict(
                size=28,
                color="red",
                symbol="x",
                line=dict(width=3, color="red")
            ),
            name="Router mati",
            hovertemplate="Router gagal: " + router_failed + "<extra></extra>",
        ))

    if step == 0:
        title = "Kondisi Awal Jaringan"
    elif step == 1:
        title = f"Router {router_failed} Dimatikan"
    else:
        title = f"Dampak Kegagalan Router {router_failed}"

    fig.update_layout(
        title=title,
        height=600,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        margin=dict(l=20, r=20, t=60, b=100),
        xaxis=dict(visible=False, range=[-0.5, 6.2]),
        yaxis=dict(visible=False, range=[-0.7, 5.2]),
    )

    return fig


# ==========================================
# 4. ANTARMUKA APLIKASI
# ==========================================

st.title("🌐 Network Blackout")
st.write(
    "Simulasi kegagalan router dan dampaknya terhadap "
    "konektivitas komputer ke server."
)

st.info(
    "Model menggunakan topologi jaringan simulasi dengan "
    "15 perangkat dan 15 koneksi."
)

router_options = ["R1", "R2", "R3", "R4", "R5"]

router_failed = st.selectbox(
    "Pilih router yang akan dimatikan",
    router_options,
)

step_label = st.radio(
    "Tahap simulasi",
    [
        "1. Kondisi awal",
        "2. Router dimatikan",
        "3. Dampak konektivitas",
    ],
    horizontal=True,
)

step = [
    "1. Kondisi awal",
    "2. Router dimatikan",
    "3. Dampak konektivitas",
].index(step_label)

if step == 0:
    st.caption("Semua perangkat ditampilkan dalam kondisi awal.")
else:
    st.caption(
        f"Simulasi menunjukkan kondisi setelah {router_failed} gagal."
    )

result = analyze_failure(router_failed)

if step == 0:
    connected_count = 9
    disconnected_count = 0
    component_count = 1
else:
    connected_count = len(result["connected"])
    disconnected_count = len(result["disconnected"])
    component_count = len(result["components"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total perangkat", G.number_of_nodes())
col2.metric("Komputer terhubung", connected_count)
col3.metric("Komputer terputus", disconnected_count)
col4.metric("Komponen jaringan", component_count)



def make_smooth_html(router_failed, step):
    import json

    result = analyze_failure(router_failed) if step > 0 else None
    graph_view = G.copy() if step == 0 else result["graph"]
    reachable = set(G.nodes) if step == 0 else result["reachable"]

    positions = {
        node: [float(x), float(y)]
        for node, (x, y) in POSITIONS.items()
    }

    nodes = []
    for node, data in G.nodes(data=True):
        x, y = positions[node]
        active = node in reachable
        failed = node == router_failed and step > 0
        nodes.append({
            "id": node,
            "x": x,
            "y": y,
            "type": data["type"],
            "active": active,
            "failed": failed
        })

    edges = []
    for u, v in graph_view.edges():
        edges.append({"source": u, "target": v})

    payload = json.dumps({
        "nodes": nodes,
        "edges": edges,
        "step": step
    })

    return """
    <div style="font-family:Arial,sans-serif;color:#222">
      <div style="display:flex;gap:8px;margin-bottom:8px">
        <button id="play">▶ Play</button>
        <button id="pause">Ⅱ Pause</button>
        <span id="status">Animasi siap</span>
      </div>
      <svg id="network" viewBox="0 0 900 480"
           style="width:100%;background:#fafafa;border:1px solid #ddd;border-radius:8px">
      </svg>
    </div>
    <script>
    const data = PAYLOAD_PLACEHOLDER;
    const svg = document.getElementById("network");
    const ns = "http://www.w3.org/2000/svg";
    const X = x => 70 + x * 145;
    const Y = y => 420 - y * 85;
    const byId = Object.fromEntries(data.nodes.map(n => [n.id,n]));
    function element(tag, attrs) {
      const el = document.createElementNS(ns,tag);
      Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));
      svg.appendChild(el);
      return el;
    }
    data.edges.forEach(e => {
      const a=byId[e.source], b=byId[e.target];
      element("line",{
        x1:X(a.x),y1:Y(a.y),x2:X(b.x),y2:Y(b.y),
        stroke:"#9ca3af","stroke-width":3
      });
    });
    data.nodes.forEach(n => {
      const color = n.failed ? "#dc2626" : n.active ? "#16a34a" : "#9ca3af";
      element("circle",{cx:X(n.x),cy:Y(n.y),r:n.type==="server"?19:14,fill:color});
      const t=element("text",{x:X(n.x),y:Y(n.y)+4,"text-anchor":"middle",
        fill:"white","font-size":n.type==="server"?12:10,"font-weight":"bold"});
      t.textContent=n.id;
    });
    const particles=[];
    data.edges.forEach(e=>{
      const a=byId[e.source],b=byId[e.target];
      const p=element("circle",{r:5,fill:"#f59e0b",opacity:0});
      particles.push({p,a,b,t:Math.random()});
    });
    let running=false, frame=0;
    function animate(){
      if(!running)return;
      particles.forEach(q=>{
        q.t=(q.t+0.006)%1;
        const reachable= q.a.active && q.b.active;
        q.p.setAttribute("opacity",reachable?1:0);
        q.p.setAttribute("cx",X(q.a.x+(q.b.x-q.a.x)*q.t));
        q.p.setAttribute("cy",Y(q.a.y+(q.b.y-q.a.y)*q.t));
      });
      frame=requestAnimationFrame(animate);
    }
    document.getElementById("play").onclick=()=>{
      if(!running){running=true;document.getElementById("status").textContent="Animasi berjalan";animate();}
    };
    document.getElementById("pause").onclick=()=>{
      running=false;cancelAnimationFrame(frame);
      document.getElementById("status").textContent="Animasi dijeda";
    };
    </script>
    """.replace("PAYLOAD_PLACEHOLDER", payload)


st.plotly_chart(
    draw_network(router_failed, step),
    use_container_width=True,
)

st.subheader("Animasi jaringan")
components.html(
    make_smooth_html(router_failed, step),
    height=540,
    scrolling=False,
)

if step == 2:
    st.subheader("Hasil analisis")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Komputer yang masih terhubung")
        st.write(result["connected"] or "Tidak ada")

    with col2:
        st.error("Komputer yang kehilangan akses")
        st.write(result["disconnected"] or "Tidak ada")

    st.write(
        "**Jumlah komponen setelah kegagalan:**",
        len(result["components"])
    )

    with st.expander("Lihat komponen jaringan"):
        for i, component in enumerate(result["components"], start=1):
            st.write(f"Komponen {i}: {sorted(component)}")

# ==========================================
# 5. PERBANDINGAN SKENARIO
# ==========================================

st.subheader("Perbandingan skenario kegagalan")

comparison = []

for router in router_options:
    data = analyze_failure(router)
    comparison.append({
        "Router mati": router,
        "Komputer terhubung": len(data["connected"]),
        "Komputer terputus": len(data["disconnected"]),
        "Jumlah komponen": len(data["components"]),
    })

st.dataframe(
    pd.DataFrame(comparison),
    hide_index=True,
    use_container_width=True,
)

st.subheader("Interpretasi dan batasan")

st.write(
    "Dampak kegagalan router ditentukan oleh posisi router, "
    "struktur jaringan, dan ketersediaan jalur alternatif. "
    "Derajat router saja tidak cukup untuk menjelaskan seluruh dampaknya."
)

st.warning(
    "Simulasi ini hanya menguji konektivitas berdasarkan topologi. "
    "Kapasitas jaringan, latensi, kehilangan paket, dan pemulihan otomatis "
    "belum dimodelkan."
)
