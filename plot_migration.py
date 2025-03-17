from logzero import logger
import numpy as np
import networkx as nx
import plotly.graph_objects as go

def build_migration_chart(G, direction="Incoming"):
    l = 1  # 箭头长度
    widh = 0.035  # 箭头底边宽度（2*widh为三角形底边宽度)
    direction_map_dict = {
        "Incoming": {"tooltip": "Inflow % for province:", "color": "blue"},
        "Outgoing": {"tooltip": "Outflow % from source:", "color": "red"},
    }
    direction_label = direction_map_dict[direction]["tooltip"]
    edge_color = direction_map_dict[direction]["color"]

    fig = go.Figure()
    for edge in G.edges().data():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        opaq = min(0.5, edge[2].get("pct_total") / 50)
        opaq = max(0.1, opaq)
        fig.add_trace(
            go.Scattergeo(
                locationmode="country names",
                lon=[x0, x1],
                lat=[y0, y1],
                hoverinfo="none",
                mode="lines",
                line=dict(width=1.5, color=edge_color),
                opacity=opaq,
            )
        )

        # 绘制箭头三角形
        A = np.array([x0, y0])
        B = np.array([x1, y1])
        v = B - A  # 目的坐标与起始坐标之差
        w = v / np.linalg.norm(v)
        u = np.array([-w[1], w[0]]) * 10  # 垂直向量

        P = B - l * w
        S = P - widh * u
        T = P + widh * u

        fig.add_trace(
            go.Scattergeo(
                locationmode="country names",
                lon=[S[0], T[0], B[0], S[0]],
                lat=[S[1], T[1], B[1], S[1]],
                mode="lines",
                fill="toself",
                hoverinfo="none",
                opacity=opaq,
                fillcolor=edge_color,
                line_color=edge_color,
            )
        )

    node_x = []
    node_y = []
    province_migs = []
    province_names = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        province_migs.append(
            f"<i>{G.nodes[node]['province']}</i><br><br>{direction_label}<br>{G.nodes[node]['Migration']}"
        )
        province_names.append(G.nodes[node]['province'])
        node_x.append(x)
        node_y.append(y)

    fig.add_trace(
        go.Scattergeo(
            locationmode="country names",
            lon=node_x,
            lat=node_y,
            hoverinfo="text",
            hovertemplate="<b>%{text}</b><extra></extra>",
            text=province_migs,
            mode="markers",
            marker=dict(
                size=9,
                opacity=0.8,
                color="rgb(0, 200, 0)",
                line=dict(width=5, color="rgba(68, 68, 68, 0)"),
            ),
        )
    )

    # Additional trace to display province/city names as text labels on the map.
    fig.add_trace(
        go.Scattergeo(
            locationmode="country names",
            lon=node_x,
            lat=node_y,
            text=province_names,
            mode="text",
            textposition="top center",
            textfont=dict(size=10, color="#34495e"),
            hoverinfo="none",
        )
    )

    fig.update_layout(
        showlegend=False,
        geo=go.layout.Geo(
            scope="asia",  # Focusing on Asia to emphasize China
            projection_type="mercator",
            center={"lat":35.0, "lon":105.0},
            lataxis_range=[15, 55],
            lonaxis_range=[70, 140],
            showcountries=True,
            countrycolor="rgb(204,204,204)",
            subunitcolor="rgb(150,150,150)",  # Display boundaries for provinces/cities
            showland=True,
            landcolor="rgb(242,242,242)",
            coastlinecolor="rgb(204,204,204)",
            showlakes=True,
            lakecolor="rgb(255,255,255)",
        ),
        hoverlabel=dict(
            bgcolor="rgba(255,230,200,0.8)",
            font=dict(color="black", size=12),
            bordercolor="gray",
        ),
        margin=dict(l=20, r=20, t=0, b=0, pad=0),
    )

    return fig