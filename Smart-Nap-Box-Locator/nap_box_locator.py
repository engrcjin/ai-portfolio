# --- Import Libraries ---
import pandas as pd
import folium
from geopy.distance import distance
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- GUI for File Upload and Coordinate Input ---
def run_app():
    root = tk.Tk()
    root.title("Smart Nap Box Locator")

    customers = None
    nap_boxes = None

    def upload_customers():
        nonlocal customers
        filepath = filedialog.askopenfilename(title="Select Customers CSV", filetypes=[("CSV Files", "*.csv")])
        if filepath:
            customer_entry.delete(0, tk.END)
            customer_entry.insert(0, filepath)
            customers = pd.read_csv(filepath)

            # Check if necessary columns exist
            if not {"Customer_ID", "Customer_Latitude", "Customer_Longitude"}.issubset(customers.columns):
                messagebox.showerror("Error", "Customers CSV must contain 'Customer_ID', 'Customer_Latitude', and 'Customer_Longitude' columns.")
                return

            # Populate dropdown
            customer_dropdown["values"] = customers["Customer_ID"].tolist()
            messagebox.showinfo("Loaded", f"Loaded {len(customers)} customers successfully.")

    def upload_naps():
        nonlocal nap_boxes
        filepath = filedialog.askopenfilename(title="Select Nap Boxes CSV", filetypes=[("CSV Files", "*.csv")])
        if filepath:
            nap_entry.delete(0, tk.END)
            nap_entry.insert(0, filepath)
            nap_boxes = pd.read_csv(filepath)

            if not {"NAP_ID", "NAP_Latitude", "NAP_Longitude"}.issubset(nap_boxes.columns):
                messagebox.showerror("Error", "Nap Boxes CSV must contain 'NAP_ID', 'NAP_Latitude', and 'NAP_Longitude' columns.")
                return
            messagebox.showinfo("Loaded", f"Loaded {len(nap_boxes)} NAP boxes successfully.")

    def fill_coords(event):
        """Auto-fill latitude and longitude based on selected customer."""
        if customers is not None:
            selected_id = customer_dropdown.get()
            row = customers[customers["Customer_ID"] == selected_id]
            if not row.empty:
                lat_entry.delete(0, tk.END)
                lon_entry.delete(0, tk.END)
                lat_entry.insert(0, row.iloc[0]["Customer_Latitude"])
                lon_entry.insert(0, row.iloc[0]["Customer_Longitude"])

    def process():
        try:
            if customers is None or nap_boxes is None:
                messagebox.showerror("Error", "Please upload both CSV files first.")
                return

            lat = float(lat_entry.get())
            lon = float(lon_entry.get())
            radius_m = float(radius_entry.get())

            # Compute distance
            nap_boxes["Distance_m"] = nap_boxes.apply(
                lambda row: distance((lat, lon), (row["NAP_Latitude"], row["NAP_Longitude"])).m, axis=1
            )
            nearby = nap_boxes[nap_boxes["Distance_m"] <= radius_m]

            # Map creation
            m = folium.Map(location=[lat, lon], zoom_start=16, tiles="CartoDB positron")
            folium.Marker(
                [lat, lon],
                popup=f"Customer ({lat}, {lon})",
                icon=folium.Icon(color="red", icon="user")
            ).add_to(m)

            for _, row in nearby.iterrows():
                folium.Marker(
                    [row["NAP_Latitude"], row["NAP_Longitude"]],
                    popup=f"{row['NAP_ID']} - {row['Distance_m']:.1f} m",
                    icon=folium.Icon(color="green", icon="cloud")
                ).add_to(m)

            map_path = "nap_locator_map.html"
            m.save(map_path)
            webbrowser.open(map_path)
            messagebox.showinfo("Success", f"Map generated with {len(nearby)} nearby Nap Boxes.")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    # --- GUI Layout ---
    tk.Label(root, text="Customers CSV:").grid(row=0, column=0, sticky="w")
    customer_entry = tk.Entry(root, width=50)
    customer_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=upload_customers).grid(row=0, column=2)

    tk.Label(root, text="Nap Boxes CSV:").grid(row=1, column=0, sticky="w")
    nap_entry = tk.Entry(root, width=50)
    nap_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=upload_naps).grid(row=1, column=2)

    tk.Label(root, text="Select Customer:").grid(row=2, column=0, sticky="w")
    customer_dropdown = ttk.Combobox(root, state="readonly", width=47)
    customer_dropdown.grid(row=2, column=1)
    customer_dropdown.bind("<<ComboboxSelected>>", fill_coords)

    tk.Label(root, text="Latitude:").grid(row=3, column=0, sticky="w")
    lat_entry = tk.Entry(root)
    lat_entry.grid(row=3, column=1)

    tk.Label(root, text="Longitude:").grid(row=4, column=0, sticky="w")
    lon_entry = tk.Entry(root)
    lon_entry.grid(row=4, column=1)

    tk.Label(root, text="Radius (meters):").grid(row=5, column=0, sticky="w")
    radius_entry = tk.Entry(root)
    radius_entry.insert(0, "200")
    radius_entry.grid(row=5, column=1)

    tk.Button(root, text="Generate Map", command=process, bg="#4CAF50", fg="white").grid(row=6, column=1, pady=10)

    root.mainloop()

# --- Run the App ---
if __name__ == "__main__":
    run_app()
