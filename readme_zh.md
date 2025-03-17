# Province Migration Dashboard

该项目是一个基于 **Streamlit**、**NetworkX** 和 **Plotly** 的中国省份迁移数据可视化仪表盘。用户可以通过选择不同的省份和迁移方向（流入/流出）来查看省份之间的迁移关系以及相关的统计数据。

## 功能简介

- **交互式地图**：展示中国各省份的位置、迁移关系及迁移流向。
- **数据筛选**：支持整体现状查看，也能单独选择某一省份进行深度分析。
- **详细数据摘要**：显示各省份的迁入、迁出以及省内迁移的统计汇总，方便用户快速了解迁移情况。
- **美观悬浮标签**：定制的悬浮标签展示详细数据，背景颜色和字体样式均可自定义。

## 数据文件

- **data/province_coordinates_china.csv**  
  包含各省份经纬度、简称和全名信息，用于在地图上绘制节点位置。

- **data/province_migration_china.csv**  
  包含省份之间的迁移数据，字段包括迁出省份、迁入省份和迁移人数。

- **data/province_migration_summary_china.csv**  
  汇总各省份的迁入、迁出和省内迁移数据，用于生成数据摘要。

## 技术栈

- **Streamlit**：用于构建 Web 应用和交互式界面。
- **NetworkX**：用于构建基于 CSV 数据的迁移图（节点与边）。
- **Plotly**：用于生成交互式地图和图表。


# Province Migration Dashboard

该项目是一个基于 **Streamlit**、**NetworkX** 和 **Plotly** 的中国省份迁移数据可视化仪表盘。用户可以通过选择不同的省份和迁移方向（流入/流出）来查看省份之间的迁移关系以及相关的统计数据。

## 功能简介

- **交互式地图**：展示中国各省份的位置、迁移关系及迁移流向。
- **数据筛选**：支持整体现状查看，也能单独选择某一省份进行深度分析。
- **详细数据摘要**：显示各省份的迁入、迁出以及省内迁移的统计汇总，方便用户快速了解迁移情况。
- **美观悬浮标签**：定制的悬浮标签展示详细数据，背景颜色和字体样式均可自定义。

## 数据文件

- **data/province_coordinates_china.csv**  
  包含各省份经纬度、简称和全名信息，用于在地图上绘制节点位置。

- **data/province_migration_china.csv**  
  包含省份之间的迁移数据，字段包括迁出省份、迁入省份和迁移人数。

- **data/province_migration_summary_china.csv**  
  汇总各省份的迁入、迁出和省内迁移数据，用于生成数据摘要。

## 技术栈

- **Streamlit**：用于构建 Web 应用和交互式界面。
- **NetworkX**：用于构建基于 CSV 数据的迁移图（节点与边）。
- **Plotly**：用于生成交互式地图和图表。

## 运行项目步骤

1. 克隆项目：
   ```bash
   git clone https://github.com/mluckydream/population-migration-model.git
2. 进入项目目录：
   ```bash
   cd population-migration-model
3. 创建虚拟环境（推荐）：
   ```bash
   python3.12 -m venv venv
4. 激活虚拟环境：
   ```bash
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
5. 安装依赖：
   ```bash
   pip install -r requirements.txt
6. 运行 Streamlit 应用：
   ```bash
   streamlit run migration_app.py



   