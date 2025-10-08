# 🧭 Smart Nap Box Locator  
*A simple desktop app that helps ISPs visualize nearby NAP boxes relative to a customer’s location.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-ff69b4?logo=python)
![Folium](https://img.shields.io/badge/Map-Folium-success?logo=leaflet)
![GeoPy](https://img.shields.io/badge/Distance-GeoPy-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🌟 Overview
The **Smart Nap Box Locator** is a Python-based graphical application that assists Internet Service Providers (ISPs) in finding the nearest **Network Access Point (NAP) boxes** to a given **customer location**.

This tool combines:
- **Data handling** with `pandas`
- **Distance calculation** with `geopy`
- **Interactive maps** with `folium`
- **User-friendly GUI** with `tkinter`

---

## 🧩 Features
✅ Upload **Customer** and **NAP Box** CSV files  
✅ Automatically validate CSV formats  
✅ Select a customer and auto-fill coordinates  
✅ Specify search **radius in meters**  
✅ Visualize customer and nearby NAP boxes on a **live interactive map**  
✅ Automatically opens in your browser after generation  
