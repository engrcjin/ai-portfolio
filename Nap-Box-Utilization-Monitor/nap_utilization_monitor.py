# --- NAP Box Utilization Monitor (VS Code Version) ---
import pandas as pd
import matplotlib.pyplot as plt
import folium
import tkinter as tk
from tkinter import filedialog, messagebox

# --- 1. File Upload Function ---
def load_csv():
    file_path = filedialog.askopenfilename(
        title="Select NAP Box CSV File",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if not file_path:
        messagebox.showwarning("No File", "Please select a CSV file.")
        return None
    return pd.read_csv(file_path)

# --- 2. Utilization Calculation ---
def calculate_utilization(df):
    df['utilization'] = (df['used_ports'] / df['total_ports']) * 100

    def classify(u):
        if u >= 90:
            return 'Critical'
        elif u >= 80:
            return 'High'
        else:
            return 'Normal'

    df['status'] = df['utilization'].apply(classify)
    return df

# --- 3. Show Results ---
def show_results(df):
    print("\n📊 NAP Box Utilization Summary:\n")
    print(df[['name', 'place', 'used_ports', 'total_ports', 'utilization', 'status']])

        # --- Bar Chart Visualization (with place names) ---
    plt.figure(figsize=(10, 6))

    # Combine NAP name and place for clear labeling
    df['label'] = df['name'] + "\n" + df['place']

    colors = ['green' if u < 80 else 'orange' if u < 90 else 'red' for u in df['utilization']]
    plt.bar(df['label'], df['utilization'], color=colors)

    plt.axhline(80, color='orange', linestyle='--', label='High (80%)')
    plt.axhline(90, color='red', linestyle='--', label='Critical (90%)')

    plt.title('NAP Box Utilization by Location')
    plt.xlabel('NAP Box and Place')
    plt.ylabel('Utilization (%)')
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.legend()
    plt.tight_layout()
    plt.show()


    # Folium Map
    map_center = [df['lat'].mean(), df['lon'].mean()]
    m = folium.Map(location=map_center, zoom_start=10)

    for _, row in df.iterrows():
        if row['status'] == 'Normal':
            color = 'green'
        elif row['status'] == 'High':
            color = 'orange'
        else:
            color = 'darkred'

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=9,
            popup=f"{row['name']} ({row['utilization']:.1f}%) - {row['status']}\n{row['place']}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8
        ).add_to(m)

    # Legend
    legend_html = '''
         <div style="position: fixed; 
                     bottom: 50px; left: 50px; width: 170px; height: 110px; 
                     border:2px solid grey; z-index:9999; font-size:14px;
                     background-color: white; opacity: 0.85;
                     padding: 10px;">
         <b>📍 Legend</b><br>
         <i style="background:green; width:10px; height:10px; float:left; margin-right:8px; opacity:0.8;"></i> Normal (&lt;80%)<br>
         <i style="background:orange; width:10px; height:10px; float:left; margin-right:8px; opacity:0.8;"></i> High (80–90%)<br>
         <i style="background:darkred; width:10px; height:10px; float:left; margin-right:8px; opacity:0.8;"></i> Critical (&gt;90%)<br>
         </div>
         '''
    m.get_root().html.add_child(folium.Element(legend_html))
    m.save("nap_utilization_map.html")

    print("\n🗺️ Map saved as 'nap_utilization_map.html'. Open it in your browser.")

# --- 4. GUI App ---
def run_app():
    root = tk.Tk()
    root.title("NAP Box Utilization Monitor")

    def process_file():
        df = load_csv()
        if df is not None:
            df = calculate_utilization(df)
            show_results(df)

    btn = tk.Button(root, text="Upload NAP Box CSV", command=process_file, bg="#3498db", fg="white", padx=10, pady=5)
    btn.pack(padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_app()
