import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import pdfkit
import numpy as np
import csv
import random


def generate_dummy_geospatial_data(filename, num_points):
    # Generate dummy geospatial data
    data = pd.DataFrame()

    # Generate random coordinates (latitude and longitude)
    data['Latitude'] = np.random.uniform(low=-90, high=90, size=num_points)
    data['Longitude'] = np.random.uniform(low=-180, high=180, size=num_points)

    # Generate other dummy attributes such as water source type, infrastructure type, terrain features, etc.
    data['Water_Source'] = np.random.choice(['River', 'Lake', 'Reservoir', 'Groundwater'], size=num_points)
    data['Infrastructure_Type'] = np.random.choice(['Pipeline', 'Channel', 'Reservoir', 'Treatment Plant'], size=num_points)
    data['Terrain_Features'] = np.random.choice(['Flat', 'Hilly', 'Mountainous'], size=num_points)
    data['Land_Use'] = np.random.choice(['Urban', 'Suburban', 'Rural'], size=num_points)

    # Save the generated data as a CSV file
    data.to_csv(filename, index=False)

def generate_dummy_iot_data(filename, num_entries):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Flow Rate', 'Pressure Level', 'Latitude', 'Longitude'])
        for _ in range(num_entries):
            timestamp = '2024-05-31 12:00:00'  # Dummy timestamp
            flow_rate = random.uniform(0.5, 10)  # Random flow rate
            pressure_level = random.uniform(10, 50)  # Random pressure level
            latitude = random.uniform(12.9, 13)  # Random latitude within specified range
            longitude = random.uniform(77.4, 77.6)  # Random longitude within specified range
            writer.writerow([timestamp, flow_rate, pressure_level, latitude, longitude])

class GraphGenerator:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
    
    def generate_map_graph(self):
        # Create a map centered at a specific location
        map_graph = folium.Map(location=[self.df['Latitude'].mean(), self.df['Longitude'].mean()], zoom_start=10)

        # Add markers for each data point
        for _, row in self.df.iterrows():
            folium.Marker([row['Latitude'], row['Longitude']]).add_to(map_graph)

        # Save the map as an HTML file
        map_graph_path = 'templates/map_graph.html'
        map_graph.save(map_graph_path)

        return map_graph_path

    def generate_heatmap(self):
        try:
            # Create a heatmap using seaborn
            plt.figure(figsize=(10, 6))
            heatmap = sns.heatmap(self.df[['Latitude', 'Longitude']].pivot_table(index='Latitude', columns='Longitude', aggfunc='size'), cmap='YlGnBu')

            # Save the heatmap as an image
            heatmap_path = 'static/images/heatmap.png'
            heatmap.figure.savefig(heatmap_path)

            return heatmap_path
        except Exception as e:
            print(f"Error generating heatmap: {e}")
            return None

    def generate_seaborn_graphs(self):
        try:
            # Example seaborn graphs
            # Scatter plot
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=self.df, x='Flow Rate', y='Pressure Level')
            scatter_path = 'static/images/scatter_plot.png'
            plt.savefig(scatter_path)

            # Histogram
            plt.figure(figsize=(10, 6))
            sns.histplot(data=self.df, x='Flow Rate', bins=20, kde=True)
            hist_path = 'static/images/histogram.png'
            plt.savefig(hist_path)

            # Box plot
            plt.figure(figsize=(10, 6))
            sns.boxplot(data=self.df, x='Pressure Level')
            box_path = 'static/images/box_plot.png'
            plt.savefig(box_path)

            # Pairplot
            plt.figure(figsize=(12, 8))
            sns.pairplot(self.df[['Flow Rate', 'Pressure Level', 'Latitude', 'Longitude']])
            pairplot_path = 'static/images/pairplot.png'
            plt.savefig(pairplot_path)

            return [scatter_path, hist_path, box_path, pairplot_path]
        except Exception as e:
            print(f"Error generating Seaborn graphs: {e}")
            return None

    def generate_additional_seaborn_graphs(self):
        # Generate and save Seaborn graph 2
        sns.scatterplot(x='Flow Rate', y='Pressure Level', data=self.df)
        plt.title('Flow Rate vs Pressure Level')
        plt.xlabel('Flow Rate')
        plt.ylabel('Pressure Level')
        seaborn_graph2_path = 'static/images/seaborn_graph2.png'
        plt.savefig(seaborn_graph2_path)
        plt.close()

        # Generate and save Seaborn graph 3
        sns.histplot(self.df['Flow Rate'], kde=True)
        plt.title('Distribution of Flow Rate')
        plt.xlabel('Flow Rate')
        plt.ylabel('Frequency')
        seaborn_graph3_path = 'static/images/seaborn_graph3.png'
        plt.savefig(seaborn_graph3_path)
        plt.close()

        # Generate and save Seaborn graph 4
        sns.histplot(self.df['Pressure Level'], kde=True)
        plt.title('Distribution of Pressure Level')
        plt.xlabel('Pressure Level')
        plt.ylabel('Frequency')
        seaborn_graph4_path = 'static/images/seaborn_graph4.png'
        plt.savefig(seaborn_graph4_path)
        plt.close()

        return [seaborn_graph2_path, seaborn_graph3_path, seaborn_graph4_path]

    @staticmethod
    def download_graphs_pdf(graph_images):
        try:
            # Convert HTML files to PDF
            pdfkit_options = {
                'page-size': 'A4',
                'orientation': 'Landscape'
            }
            pdfkit.from_file(graph_images[:2], 'static/iotgraphs_report.pdf', options=pdfkit_options)

            # Return the PDF file path
            return 'static/iotgraphs_report.pdf'
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
import os

class GeospatialGraphGenerator:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
    
    def generate_map_graph(self):
        # Create a map centered at a specific location
        map_graph = folium.Map(location=[self.df['Latitude'].mean(), self.df['Longitude'].mean()], zoom_start=2)

        # Add markers for each data point
        for _, row in self.df.iterrows():
            folium.Marker([row['Latitude'], row['Longitude']]).add_to(map_graph)

        # Save the map as an HTML file
        map_graph_path = 'templates/geospatial_map_graph.html'
        map_graph.save(map_graph_path)

        return map_graph_path

    def generate_heatmap(self):
        try:
            # Create a heatmap using seaborn
            plt.figure(figsize=(10, 6))
            heatmap = sns.heatmap(self.df[['Latitude', 'Longitude']].pivot_table(index='Latitude', columns='Longitude', aggfunc='size'), cmap='YlGnBu')

            # Save the heatmap as an image
            heatmap_path = 'static/images/geospatial_heatmap.png'
            heatmap.figure.savefig(heatmap_path)

            return heatmap_path
        except Exception as e:
            print(f"Error generating heatmap: {e}")
            return None

    def generate_infrastructure_distribution(self):
        try:
            # Count the number of each infrastructure type
            infrastructure_count = self.df['Infrastructure_Type'].value_counts()

            # Plot the distribution of infrastructure types
            plt.figure(figsize=(10, 6))
            sns.barplot(x=infrastructure_count.index, y=infrastructure_count.values)
            plt.xlabel('Infrastructure Type')
            plt.ylabel('Count')
            plt.title('Distribution of Infrastructure Types')
            infrastructure_distribution_path = 'static/images/geospatial_infrastructure_distribution.png'
            plt.savefig(infrastructure_distribution_path)

            return infrastructure_distribution_path
        except Exception as e:
            print(f"Error generating infrastructure distribution plot: {e}")
            return None

    def generate_infrastructure_per_terrain(self):
        try:
            # Plot the number of each infrastructure type per terrain feature
            plt.figure(figsize=(12, 8))
            sns.countplot(data=self.df, x='Infrastructure_Type', hue='Terrain_Features')
            plt.xlabel('Infrastructure Type')
            plt.ylabel('Count')
            plt.title('Infrastructure Types per Terrain Features')
            infrastructure_per_terrain_path = 'static/images/geospatial_infrastructure_per_terrain.png'
            plt.savefig(infrastructure_per_terrain_path)

            return infrastructure_per_terrain_path
        except Exception as e:
            print(f"Error generating infrastructure per terrain plot: {e}")
            return None

    def generate_infrastructure_per_water_source(self):
        try:
            # Plot the number of each infrastructure type per water source
            plt.figure(figsize=(12, 8))
            sns.countplot(data=self.df, x='Infrastructure_Type', hue='Water_Source')
            plt.xlabel('Infrastructure Type')
            plt.ylabel('Count')
            plt.title('Infrastructure Types per Water Source')
            infrastructure_per_water_source_path = 'static/images/geospatial_infrastructure_per_water_source.png'
            plt.savefig(infrastructure_per_water_source_path)

            return infrastructure_per_water_source_path
        except Exception as e:
            print(f"Error generating infrastructure per water source plot: {e}")
            return None

if __name__ == "__main__":
    csv_file = 'data/dummy_iot_data.csv'
    csv_file2 = 'data/dummy_geospatial_data.csv'
    generate_dummy_iot_data(csv_file, 100)
    generate_dummy_geospatial_data(csv_file2, 100)
    graph_gen = GraphGenerator(csv_file)
    map_graph_path = graph_gen.generate_map_graph()
    heatmap_path = graph_gen.generate_heatmap()
    seaborn_graphs = graph_gen.generate_seaborn_graphs()
    additional_seaborn_graphs = graph_gen.generate_additional_seaborn_graphs()
    graph_gen = GeospatialGraphGenerator(csv_file2)
    map_graph_path = graph_gen.generate_map_graph()
    heatmap_path = graph_gen.generate_heatmap()
    infrastructure_distribution_path = graph_gen.generate_infrastructure_distribution()
    infrastructure_per_terrain_path = graph_gen.generate_infrastructure_per_terrain()
    infrastructure_per_water_source_path = graph_gen.generate_infrastructure_per_water_source()
    print("Geospatial data graphs generated successfully!")

   
