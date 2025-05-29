# 🧪 Object Dimension Checker from Images

This project is a simple yet effective PyQt5-based desktop application that helps verify whether a manufactured product matches its intended dimensions. By analyzing top and side view images of the object, the software performs basic dimensional measurements such as width, height, and thickness using OpenCV.

The measurements are compared to expected reference values to check if the product has been accurately formed. The application can assist quality control teams in evaluating production consistency in a practical way.

## 🎯 Features

- Manual selection of object type (e.g., matchbox, phone, round cap)
- Upload side and top view images separately
- Measure key dimensions (height, width, thickness)
- Visualize measurements on the image
- User-friendly PyQt5 GUI
- Reference-based scaling using known objects (e.g., A4 paper)

## 🛠️ Technologies Used

- Python 3.11
- PyQt5
- OpenCV
- Open3D
- NumPy

##Project Structure
```bash
3D_vs_REAL_Object_Measurement_Project/
├── Measurement Codes/
│ ├── main.py
│ ├── mainwindow.py
│ ├── mainwindow.ui
│ ├── main.spec
│ ├── init.py
│ ├── RoundCap/
│ │ ├── find_roundcap.py
│ │ ├── thickness_roundcap.py
│ │ └── measure_roundcap.py
│ └── Matchbox/
│ ├── find_matchbox.py
│ ├── thickness_matchbox.py
│ └── measure_matchbox.py
│
├── images/
│ ├── Matchbox/
│ │ ├── side image/
│ │ └── top image/
│ └── roundCap/
│ ├── side image/
│ └── top image/
│
└── 3D models/
```
## RUN
```bash
python main.py

