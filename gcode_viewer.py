import sys
import re
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtWidgets

def parse_gcode_segments(filename):
    """
    Parse a G-code file and extract extrusion and travel segments.

    Args:
        filename (str): Path to the G-code file.

    Returns:
        extrusion_segments (list): List of [start, end] points for extrusion moves.
        travel_segments (list): List of [start, end] points for travel moves.
    """
    extrusion_segments = []  # Segments where material is extruded
    travel_segments = []     # Segments where the hotend travels without extrusion
    x = y = z = e = 0.0     # Current coordinates and extrusion value
    last_pos = [x, y, z]    # Previous position
    last_e = e              # Previous extrusion value
    with open(filename, 'r') as f:
        for line in f:
            # Only process G0/G1 movement commands
            if line.startswith('G0') or line.startswith('G1'):
                match_x = re.search(r'X([-+]?\d*\.?\d+)', line)
                match_y = re.search(r'Y([-+]?\d*\.?\d+)', line)
                match_z = re.search(r'Z([-+]?\d*\.?\d+)', line)
                match_e = re.search(r'E([-+]?\d*\.?\d+)', line)
                if match_x:
                    x = float(match_x.group(1))
                if match_y:
                    y = float(match_y.group(1))
                if match_z:
                    z = float(match_z.group(1))
                if match_e:
                    e_new = float(match_e.group(1))
                else:
                    e_new = e
                new_pos = [x, y, z]
                # Only add a segment if the position changed
                if new_pos != last_pos:
                    if e_new > last_e:
                        # Extrusion move (material deposited)
                        extrusion_segments.append([last_pos.copy(), new_pos.copy()])
                    else:
                        # Travel move (no material)
                        travel_segments.append([last_pos.copy(), new_pos.copy()])
                last_pos = new_pos
                last_e = e_new
                e = e_new
    return extrusion_segments, travel_segments

class GCodeViewer(QtWidgets.QWidget):
    """
    Widget to display a 3D visualization of G-code toolpaths.
    Shows extrusion moves in yellow and travel moves in blue.
    """
    def __init__(self, gcode_path):
        super().__init__()
        self.setWindowTitle('Simple 3D G-code Visualizer')
        layout = QtWidgets.QVBoxLayout(self)
        self.view = gl.GLViewWidget()
        layout.addWidget(self.view)
        self.view.setCameraPosition(distance=100)

        # Parse G-code and get segments
        extrusion_segments, travel_segments = parse_gcode_segments(gcode_path)

        # Draw extrusion moves (yellow, thicker)
        if extrusion_segments:
            extrusion_lines = np.array(extrusion_segments).reshape(-1, 3)
            plt1 = gl.GLLinePlotItem(
                pos=extrusion_lines,
                color=(1,1,0,1),  # Yellow
                width=2,
                antialias=True,
                mode='lines')
            self.view.addItem(plt1)

        # Draw travel moves (blue, thinner)
        if travel_segments:
            travel_lines = np.array(travel_segments).reshape(-1, 3)
            plt2 = gl.GLLinePlotItem(
                pos=travel_lines,
                color=(0,0,1,0.5),  # Blue, semi-transparent
                width=1,
                antialias=True,
                mode='lines')
            self.view.addItem(plt2)

        # Mark start and end points
        all_segments = extrusion_segments + travel_segments
        if all_segments:
            # First point (green)
            first_point = all_segments[0][0]
            first_marker = gl.GLScatterPlotItem(
                pos=[first_point],
                color=(0, 1, 0, 1),  # Green
                size=15,
                pxMode=False)
            self.view.addItem(first_marker)
            
            # Last point (red)
            last_point = all_segments[-1][1]
            last_marker = gl.GLScatterPlotItem(
                pos=[last_point],
                color=(1, 0, 0, 1),  # Red
                size=15,
                pxMode=False)
            self.view.addItem(last_marker)

        self.resize(800, 600)

def main():
    """
    Entry point for the G-code visualizer.
    Usage: python gcode_viewer.py <file.gcode>
    """
    import os
    if len(sys.argv) < 2:
        print('Uso: python gcode_viewer.py <archivo.gcode>')
        sys.exit(1)
    # Solo permitir nombres de archivo, sin rutas
    filename = sys.argv[1]
    if os.path.basename(filename) != filename or '..' in filename or filename.startswith('/') or filename.startswith('\\'):
        print('Error: Solo se permite el nombre del archivo dentro de la carpeta input/')
        sys.exit(1)
    input_folder = os.path.join(os.path.dirname(__file__), 'input')
    gcode_path = os.path.join(input_folder, filename)
    if not os.path.isfile(gcode_path):
        print(f'Error: El archivo {filename} no existe en la carpeta input/')
        sys.exit(1)
    app = QtWidgets.QApplication([])
    viewer = GCodeViewer(gcode_path)
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
