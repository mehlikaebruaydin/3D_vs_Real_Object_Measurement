
import sys
import os

# RoundCap klasörünü import yoluna ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'RoundCap'))

from RoundCap import measure_roundcap
import find_roundcap



import cv2
import numpy as np
from RoundCap import thickness_roundcap
from RoundCap import measure_roundcap
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from main_window import Ui_MainWindow


from Matchbox import measure_matchbox
from Matchbox import thickness_matchbox


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.obj_type = None
        self.side_img_path = None
        self.top_img_path = None
        self.kalinlik = None
        self.genislik = None
        self.yukseklik = None

        self.ui.matchbox_button.clicked.connect(lambda: self.show_measurement_page("Matchbox"))
        self.ui.roundcap_button.clicked.connect(lambda: self.show_measurement_page("RoundCap"))
        self.ui.btn_upload_side.clicked.connect(self.upload_side_image)
        self.ui.btn_upload_top.clicked.connect(self.upload_top_image)
        self.ui.btn_upload_stl.clicked.connect(self.upload_stl)
        self.ui.btn_back.clicked.connect(self.show_home_page)

    def show_home_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_measurement_page(self, obj_type):
        self.obj_type = obj_type
        self.ui.label_selected_object.setText(f"Selected: {obj_type}")
        self.ui.label_side_image.clear()
        self.ui.label_top_image.clear()
        self.ui.result_display.clear()
        self.ui.label_result_diff.clear()
        self.side_img_path = None
        self.top_img_path = None
        self.kalinlik = None
        self.genislik = None
        self.yukseklik = None
        self.ui.stackedWidget.setCurrentIndex(1)

    def upload_side_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Side View Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.side_img_path = file_path
            pixmap = QPixmap(file_path).scaled(180, 160, Qt.KeepAspectRatio)
            self.ui.label_side_image.setPixmap(pixmap)
            try:
                if self.obj_type == "Matchbox":
                    thickness = thickness_matchbox.yukseklik(self.side_img_path)
                elif self.obj_type == "RoundCap":
                    thickness = thickness_roundcap.roundcap_yukseklik(self.side_img_path)
                else:
                    raise ValueError("Unsupported object type.")

                if isinstance(thickness, (int, float)):
                    self.kalinlik = thickness
                    self.ui.result_display.setText(
                        f"Thickness measured: {thickness:.2f} cm\n\nNow upload top view."
                    )
                else:
                    raise ValueError("Invalid thickness value.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Side view processing error:\n{str(e)}")

    def upload_top_image(self):
        if not self.kalinlik:
            QMessageBox.warning(self, "Warning", "Please measure thickness first (upload side view).")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Top View Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.top_img_path = file_path
            pixmap = QPixmap(file_path).scaled(180, 160, Qt.KeepAspectRatio)
            self.ui.label_top_image.setPixmap(pixmap)
            try:
                if self.obj_type == "Matchbox":
                    result_img, width, height = measure_matchbox.kibrit_olc(self.top_img_path, self.kalinlik)
                elif self.obj_type == "RoundCap":
                    result_img, width, height , results_dict = measure_roundcap.cap_olcum(self.top_img_path, self.kalinlik)
                    self.genislik = width
                    self.yukseklik = height
                    self.roundcap_results = results_dict
                else:
                    raise ValueError("Unsupported object.")

                if result_img is not None:
                    rgb_image = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    self.ui.result_display.setPixmap(QPixmap.fromImage(q_img).scaled(520, 440, Qt.KeepAspectRatio))

                    self.genislik = width
                    self.yukseklik = height
                else:
                    raise ValueError("Object not found in image.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Top view processing error:\n{str(e)}")

    def upload_stl(self):
        stl_path, _ = QFileDialog.getOpenFileName(None, "STL File", "", "STL Files (*.stl)")
        if not stl_path:
            return

        try:
            threading.Thread(target=self.show_stl_window, args=(stl_path,), daemon=True).start()

            if self.obj_type == "RoundCap":
                if not all([self.kalinlik, self.genislik, self.yukseklik]):
                    raise ValueError("Lütfen önce üst ve yan görüntüleri yükleyin.")

                # RoundCap için STL ölçüleri sabit
                stl_results = {
                    "diameter": 5.00,
                    "radius": 2.50,
                    "circumference": 15.71,
                    "area": 19.63,
                    "height": 2.00
                }

                # OpenCV ölçümleri
                opencv_results = self.roundcap_results  # cap_olcum() fonksiyonundan dönen dict

                # ❗️Height = thickness olacak
                opencv_yukseklik = opencv_results.get("thickness", 0)

                result_text = "3D MODEL vs REAL Comparison:\n\n"
                for key in ["diameter", "radius", "circumference", "area", "height"]:
                    stl_val = stl_results[key]
                    opencv_val = opencv_results.get(key, 0) if key != "height" else opencv_yukseklik
                    diff = abs(stl_val - opencv_val)
                    label = {
                        "diameter": "Diameter",
                        "radius": "Radius",
                        "circumference": "Circumference",
                        "area": "Area",
                        "height": "Thickness"
                    }[key]
                    unit = "cm²" if key == "area" else "cm"

                    result_text += f"{label} (3D MODEL): {stl_val:.2f} {unit}\n"
                    result_text += f"{label} (REAL): {opencv_val:.2f} {unit}\n"
                    result_text += f"Difference: {diff:.2f} {unit}\n\n"

                self.ui.label_result_diff.setText(result_text.strip())



            elif self.obj_type == "Matchbox":

                if not all([self.kalinlik, self.genislik, self.yukseklik]):
                    raise ValueError("Lütfen önce üst ve yan görüntüleri yükleyin.")

                stl_results = {

                    "genislik": 4.0,

                    "yukseklik": 6.0,

                    "kalinlik": 2.0

                }

                opencv_results = {

                    "genislik": self.genislik,

                    "yukseklik": self.yukseklik,

                    "kalinlik": self.kalinlik

                }

                result_text = "3D MODEL vs REAL Comparison (Matchbox):\n\n"

                for key in ["genislik", "yukseklik", "kalinlik"]:
                    stl_val = stl_results[key]
                    opencv_val = opencv_results.get(key, 0)
                    diff = abs(stl_val - opencv_val)
                    label = {
                        "genislik": "Width",
                        "yukseklik": "Height",
                        "kalinlik": "Thickness"
                    }[key]

                    result_text += f"{label} (3D MODEL): {stl_val:.2f} cm\n"
                    result_text += f"{label} (REAL): {opencv_val:.2f} cm\n"
                    result_text += f"Difference: {diff:.2f} cm\n\n"

                self.ui.label_result_diff.setText(result_text.strip())

        except Exception as e:  # ✅ bu satır eksikse hata alırsın
            QMessageBox.critical(self, "Hata", f"3D karşılaştırma hatası:\n{str(e)}")

    def show_stl_window(self, path):
        import open3d as o3d
        mesh = o3d.io.read_triangle_mesh(path)
        mesh.compute_vertex_normals()
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="STL Preview", width=500, height=500)
        vis.add_geometry(mesh)
        vis.run()
        vis.destroy_window()

    def show_error(self, message):
        QMessageBox.critical(self, "Hata", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = MainApp()
    pencere.show()
    sys.exit(app.exec_())
