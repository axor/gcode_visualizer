# Simple 3D G-code Visualizer

This tool visualizes 3D printer G-code files in 3D using PyQtGraph.

## Uso seguro
- Coloca tus archivos `.gcode` en la carpeta `input/`.
- Ejecuta el visualizador pasando solo el nombre del archivo, por ejemplo:
  ```
  python gcode_viewer.py archivo.gcode
  ```
- El script solo abrirá archivos dentro de `input/` para evitar vulnerabilidades de path-injection.

## Requisitos
- Python 3
- pyqtgraph
- PyQt5
- numpy

Instala dependencias con:
```
pip install pyqtgraph PyQt5 numpy
```

## Buenas prácticas
- No subas archivos personales o sensibles a este repositorio.
- Usa la carpeta `input/` solo para archivos G-code que quieras visualizar.
