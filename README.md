DataGenome 

DataGenome is an interactive data analysis tool that visualizes the hidden structure of dataset features.

It combines correlation analysis, 3D feature embedding, clustering, and automatic reporting to help users understand how variables behave and relate to each other.

Features

- Upload any CSV dataset
- Preview dataset instantly
- Generate feature correlation heatmap
- Build a 3D genome map of numeric features using PCA
- Automatically cluster similar features using KMeans
- Generate an auto dataset report
- Summarize dataset size and numeric feature count

Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

Project Structure

DataGenome/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── utils/
│   └── genome_analyzer.py
│
└── screenshots/
Installation

Clone the repository:

bash
git clone https://github.com/PoojaSiv0211/DataGenome.git
cd DataGenome


Create and activate virtual environment:


python -m venv venv
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Run the application:

streamlit run app.py


Example Workflow

1. Upload a CSV dataset
2. Inspect the dataset preview
3. Analyze feature correlation
4. Visualize the 3D genome map
5. Review feature clusters
6. Read the auto-generated dataset report

Example Output

The system identifies:

- strongest positive and negative correlations
- clusters of related features
- 3D placement of variables based on similarity
- automatic textual interpretation of dataset structure

Use Cases

- exploratory data analysis
- feature relationship discovery
- educational demonstrations
- mini project presentations
- dataset structure visualization

Screenshots

Dataset Preview
![Preview](screenshots/preview.png)

Correlation Heatmap
![Heatmap](screenshots/heatmap.png)

3D Genome Map
![Genome Map](screenshots/genome3d.png)

Auto Dataset Report
![Report](screenshots/report.png)

Author:
Pooja Sivaramalingam  
AI & Data Science Student