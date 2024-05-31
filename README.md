# WARUNA
Water Assessment and Reporting in Unified  Network Application


Project Features:
Issue Reporting for Public Users:

Public users can report water-related issues without logging in.
Features include location details (map link or description), address, landmark, issue description, optional images, and notice date.
Interactive Map Interface:

Utilizes Leaflet library for an interactive map interface.
Displays water supply structures (pipelines, reservoirs, pumping stations) and reported issues.
Custom markers/icons for different types of structures and issues.
Features zooming, panning, and filtering of map data.
Allows toggling visibility of different layers (e.g., structures, issues).
Dashboard for Officials:

Manager Dashboard:
Assign tasks to water inspectors based on reported issues.
View reports submitted by water inspectors and manage them.
Award inspectors for their work.
Manage water supply structures (CRUD operations).
Monitor and manage IoT sensor data.
Water Inspector Dashboard:
View assigned tasks with details and map view.
Update task status (e.g., in-progress, resolved).
Submit detailed reports with findings and images.
Monitor and respond to real-time alerts from IoT sensors.
IoT Integration:

Dummy IoT sensor data generation for simulating real-time updates.
Sensors monitor key parameters like flow rates and pressure levels.
Integration with geospatial data for accurate sensor placement and visualization.
Grievance Redressal System:

Allows users to track the status of reported issues.
Admins can manage and resolve grievances efficiently.
Geospatial Database Management:

CRUD Operations: Create, retrieve, update, and delete water supply structures.
Database Schema: Utilizes SQLite database for storing geospatial data related to structures and their attributes.
Geospatial Data Visualization:

Enables visualization of geospatial data through interactive maps.
Generates heatmaps to identify areas of concern within the water supply network.
Downloadable Graphs:

Provides buttons for downloading graphs generated using Plotly and Seaborn.
Graphs offer insights into issue status over time and other analytics.
Project Structure:
Frontend:

HTML/CSS/JavaScript for the user interface.
Leaflet for the interactive map interface.
Plotly and Seaborn for generating graphs and visualizations.
Backend:

Python Flask framework for server-side logic.
SQLite database for storing geospatial and other data.
Dummy IoT sensor data generation script.
Integration with geospatial data for map visualization.
Authentication and Authorization:

User authentication and role-based access control for different dashboard functionalities.
Sessions management for maintaining user state.
File Handling:

Upload and storage of issue-related images.
Downloadable graphs in PDF or text file format.
