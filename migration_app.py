from logzero import logger

import pandas as pd
import streamlit as st

import data_munging
import plot_migration

from data_munging import ALL_PROVINCES_TITLE

padding = 0
st.set_page_config(page_title="Migration Network", layout="wide", page_icon="📍")

# Custom CSS for overall page and sidebar customization
st.markdown(
    """
    <style>
    .small-font {
        font-size:12px;
        font-style: italic;
        color: #b1a7a6;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

TABLE_PAGE_LEN = 10

province_coordinates = data_munging.get_coordinates()
province_migration = pd.read_csv("data/province_migration_china.csv")
province_summary = pd.read_csv("data/province_migration_summary_china.csv")

st.title("Province Movement")
province_choices = list(province_coordinates["name"])
province_choices.insert(0, ALL_PROVINCES_TITLE)

with st.sidebar.form(key="my_form"):
    selectbox_province = st.selectbox("Choose a province", province_choices)
    selectbox_direction = st.selectbox("Choose a direction", ["Incoming", "Outgoing"])
    slider_threshold = st.slider(
        "Set top N Migration per province",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        format="%i",
    )
    st.markdown(
        '<p class="small-font">Results Limited to top 5 per Province in overall China</p>',
        unsafe_allow_html=True,
    )
    pressed = st.form_submit_button("Build Migration Map")

expander = st.sidebar.expander("What is this?")
expander.write(
    """
This app allows users to view migration between provinces.
Overall China plots all provinces with substantial migration-based relationships with other provinces.
Any other option plots only migration from or to a given province. This map will be updated
to show migration once new census data comes out.

Incoming: Shows for a given province, the percent of their **total inbound migration from** another province.

Outgoing: Shows for a given province, the percent of their **total outbound migration to** another province.
"""
)

network_place, _, descriptor = st.columns([6, 1, 3])
network_loc = network_place.empty()

# Create starting graph
descriptor.subheader(data_munging.display_province(selectbox_province))
descriptor.write(data_munging.display_province_summary(selectbox_province, province_summary))

edges = data_munging.compute_edges(
    province_migration,
    threshold=slider_threshold,
    province=ALL_PROVINCES_TITLE,
    direction=selectbox_direction,
)

nodes = data_munging.compute_nodes(
    province_coordinates, edges, direction=selectbox_direction
)
G = data_munging.build_network(nodes, edges)
logger.info("Graph Created, doing app stuff")

migration_plot = plot_migration.build_migration_chart(G, selectbox_direction)
network_loc.plotly_chart(migration_plot)

st.header("Migration Table")
table_loc = st.empty()
clean_edges = data_munging.table_edges(edges, selectbox_direction)
table_loc.table(clean_edges.head(20))

if pressed:
    edges = data_munging.compute_edges(
        province_migration,
        threshold=slider_threshold,
        province=selectbox_province,
        direction=selectbox_direction,
    )

    nodes = data_munging.compute_nodes(
        province_coordinates, edges, direction=selectbox_direction
    )
    G = data_munging.build_network(nodes, edges)
    migration_plot = plot_migration.build_migration_chart(G, selectbox_direction)
    network_loc.plotly_chart(migration_plot)

    clean_edges = data_munging.table_edges(edges, selectbox_direction)
    table_loc.table(clean_edges.head(20))