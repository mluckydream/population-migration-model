# Province Migration Dashboard

This project is a China province migration data visualization dashboard built using **Streamlit**, **NetworkX**, and **Plotly**. Users can view migration relationships and statistics between provinces by selecting different provinces and migration directions (Inbound/Outbound).

## Features

- **Interactive Map**: Display the locations of provinces, migration relationships, and migration flows across China.
- **Data Filtering**: Allows viewing an overall overview or detailed analysis by selecting a specific province.
- **Detailed Summary**: Shows statistical summaries of inbound, outbound, and intra-province migration data for quick insights.
- **Stylish Hover Labels**: Custom hover labels display detailed data with customizable background colors and font styles.

## Data Files

- **data/province_coordinates_china.csv**  
  Contains latitude, longitude, abbreviation, and full name information for each province to plot node positions on the map.

- **data/province_migration_china.csv**  
  Contains migration data between provinces, including source province, destination province, and migration counts.

- **data/province_migration_summary_china.csv**  
  Summarizes inbound, outbound, and intra-province migration data for each province, used to generate data summaries.

## Tech Stack

- **Streamlit**: For building the web application and interactive interface.
- **NetworkX**: For constructing the migration graph based on the CSV data (nodes and edges).
- **Plotly**: For generating interactive maps and charts.



## Steps to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/mluckydream/population-migration-model.git
2. Clone the repository:
   ```bash
    git clone https://github.com/mluckydream/population-migration-model.git
3. Create a virtual environment (recommended):
   ```bash
     python3.12 -m venv venv
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # or on Windows:
   venv\Scripts\activate
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
6. Run the Streamlit application:
   ```bash
     streamlit run migration_app.py