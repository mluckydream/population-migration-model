import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st

ALL_PROVINCES_TITLE = "OVERALL CHINA"
DIRECT_DICT = {"Outgoing": "mig_province", "Incoming": "province"}
OPPOSITE_DICT = {"Incoming": "mig_province", "Outgoing": "province"}


def get_coordinates():
    province_coordinates = pd.read_csv("data/province_coordinates_china.csv")

    print(province_coordinates.head())
    province_coordinates["pos"] = [
        (i, j) for i, j in zip(province_coordinates.longitude, province_coordinates.latitude)
    ]
    province_coordinates["name"] = province_coordinates.name.str.upper()
    return province_coordinates


def compute_edges(province_migration, threshold, province=None, direction="Incoming"):

    assert direction is not None
    assert province is not None

    df_direction = DIRECT_DICT[direction]
    df_opposite_direction = OPPOSITE_DICT[direction]

    # 将相关字段统一转为大写
    province_migration[df_direction] = province_migration[df_direction].str.upper()
    province_migration[df_opposite_direction] = province_migration[df_opposite_direction].str.upper()

    if province != ALL_PROVINCES_TITLE:
        province = province.upper()
        province_migration = province_migration.loc[lambda x: x[df_direction] == province]
    else:
        threshold = min(threshold, 5)
    province_migration["rank"] = province_migration.groupby(df_direction)["household_weight"].rank("dense", ascending=False)

    province_migration_total = province_migration.groupby(df_direction)["household_weight"].sum()
    province_migration = (
        province_migration.assign(
            pct_total=np.round(
                province_migration.household_weight
                / province_migration[df_direction].map(province_migration_total)
                * 100,
                2,
            )
        )
        .loc[lambda x: x["rank"] <= threshold]
        .sort_values(by="pct_total", ascending=False)
    )
    province_migration["combine"] = (
        province_migration[df_opposite_direction]
        + " "
        + province_migration.pct_total.astype(str)
        + "% Total: "
        + province_migration["household_weight"].astype(int).map("{:,d}".format)
    )

    return province_migration

def compute_nodes(province_coordinates, migration_edges, direction="Incoming"):

    df_direction = DIRECT_DICT[direction]

    total_migration = pd.DataFrame(
        migration_edges.groupby(df_direction)["combine"]
        .transform(lambda x: "<br>".join(x))
        .reset_index(drop=True)
        .drop_duplicates()
    )
    total_migration["province"] = migration_edges[df_direction].unique()
    province_coordinates["Migration"] = (
        province_coordinates["name"]
        .map(dict(zip(total_migration.province, total_migration["combine"])))
        .fillna("")
    )
    return province_coordinates


def build_network(nodes, edges):
    node_dict = nodes.set_index("name").to_dict("index")
    G = nx.from_pandas_edgelist(
        edges,
        source="mig_province",
        target="province",
        edge_attr=["household_weight", "pct_total"],
        create_using=nx.DiGraph(),
    )
    nx.set_node_attributes(G, node_dict)
    return G


def do_the_whole_thing():
    """ Thinking about making this call all of the previous functions"""
    pass


def table_edges(edges, direction):
    direction_map_dict = {
        "Incoming": {"colname": "% of Incoming Migration from Source"},
        "Outgoing": {"colname": "% of Outgoing Migration from Source"},
    }
    edges = (
        edges.drop(columns="combine")
        .sort_values(by="pct_total", ascending=False)
        .assign(
            household_weight=lambda x: x.household_weight.astype(int).map(
                "{:,d}".format
            ),
            pct_total=lambda x: np.round(x.pct_total, 2).astype(str) + "%",
            hack="",
        )
        .set_index("hack")
    )[["mig_province", "province", "household_weight", "pct_total"]]
    edges.columns = [
        "Source Province",
        "Destination Province",
        "Total People",
        direction_map_dict[direction].get("colname"),
    ]
    return edges


def paginate_dataframe(dataframe, page_size, page_num):

    page_size = page_size

    if page_size is None:

        return None

    offset = page_size * (page_num - 1)

    return dataframe[offset : offset + page_size]


def display_province(province):
    return province if province != ALL_PROVINCES_TITLE else ""

def display_province_summary(province, df):
    if province == ALL_PROVINCES_TITLE:
        return ""
    else:
        # 将 summary 中的 province 转成大写再比较
        province_upper = province.upper()
        df = (
            df.loc[lambda x: x.province.str.upper() == province_upper]
            .reset_index()
            .assign(
                total_migration=lambda x: x.inbound_migration
                + x.outbound_migration
                + x.within_province_migration
            )
        )

        if df.empty:
            return "No data available for the selected province."

        total_migration = df.total_migration.iloc[0]

        inbound_migration = df.inbound_migration.iloc[0]
        inbound_pct_total = f"{round(inbound_migration / total_migration * 100,1)}%"
        outbound_migration = df.outbound_migration.iloc[0]
        outbound_pct_total = f"{round(outbound_migration / total_migration * 100,1)}%"
        within_province_migration = df.within_province_migration.iloc[0]
        within_province_pct_total = f"{round(within_province_migration / total_migration * 100,1)}%"

        return f"""
        **Inbound Migration Total (%):** 
        
        {"{:,}".format(inbound_migration)} ({inbound_pct_total})

        **Outbound Migration Total (%):** 
        
        {"{:,}".format(outbound_migration)} ({outbound_pct_total}) 

        **Within Province Migration Total (%):** 
        
        {"{:,}".format(within_province_migration)} ({within_province_pct_total})
        """
        return f"""
        **Inbound Migration Total (%):** 
        
        {"{:,}".format(inbound_migration)} ({inbound_pct_total})

        **Outbound Migration Total (%):** 
        
        {"{:,}".format(outbound_migration)} ({outbound_pct_total}) 

        **Within Province Migration Total (%):** 
        
        {"{:,}".format(within_province_migration)} ({within_province_pct_total})
        """