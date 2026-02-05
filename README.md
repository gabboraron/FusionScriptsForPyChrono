# FusionScriptsForPyChrono

Scripts for exporting model data from Autodesk Fusion 360 to PyChrono physics simulations.

## Overview

This repository provides tools to bridge Autodesk Fusion 360 CAD models with PyChrono physics simulations. It includes:
- **Fusion 360 Export Script**: Extracts model geometry, mass properties, joints, and materials
- **PyChrono Loader**: Loads exported data into PyChrono simulation systems
- **Example Simulation**: Demonstrates how to run simulations with exported models

## Features

- ✅ Extract solid body geometry from Fusion 360 models
- ✅ Export mass properties (mass, center of mass, moments of inertia)
- ✅ Export joint/constraint definitions
- ✅ Generate STL files for collision geometry
- ✅ JSON-based data format for easy integration
- ✅ PyChrono loader with automatic body and constraint creation
- ✅ Support for visualization with Irrlicht

## Installation

### Fusion 360 Script Setup

1. **Copy the Export Script**:
   - Copy `ExportToPyChrono.py` to your Fusion 360 scripts folder:
     - Windows: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts`
     - macOS: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts`

2. **Load in Fusion 360**:
   - Open Fusion 360
   - Go to **Tools** → **Scripts and Add-Ins**
   - Find `ExportToPyChrono` in the list
   - Click **Run** to execute

### PyChrono Setup

1. **Install PyChrono**:
   ```bash
   pip install pychrono
   ```

2. **Install Dependencies** (optional, for visualization):
   ```bash
   pip install pychrono[irrlicht]
   ```

## Usage

### Exporting from Fusion 360

1. Open your model in Fusion 360
2. Run the `ExportToPyChrono` script from **Scripts and Add-Ins**
3. Select an output folder
4. The script will generate:
   - `<model_name>_pychrono.json` - Model data in JSON format
   - `geometries/` folder - STL files for each body

### Loading in PyChrono

```python
from pychrono_loader import load_model_from_json, create_visualization

# Load the exported model
system = load_model_from_json('path/to/model_pychrono.json')

# Create visualization
app = create_visualization(system, "My Simulation")

# Run simulation
app.SetTimestep(0.01)
while app.GetDevice().run():
    app.BeginScene()
    app.DrawAll()
    app.DoStep()
    app.EndScene()
```

### Running Example Simulation

```bash
python example_simulation.py example_model.json 5.0 0.01
```

Arguments:
- `example_model.json` - Path to exported JSON file
- `5.0` - Simulation duration in seconds
- `0.01` - Time step in seconds

## File Structure

```
FusionScriptsForPyChrono/
├── ExportToPyChrono.py      # Fusion 360 export script
├── pychrono_loader.py       # PyChrono loader module
├── example_simulation.py    # Example simulation runner
├── example_model.json       # Sample exported model data
├── README.md                # This file
└── LICENSE                  # MIT License
```

## Exported Data Format

The JSON export contains:

```json
{
  "model_name": "ModelName",
  "bodies": [
    {
      "name": "BodyName",
      "is_visible": true,
      "is_fixed": false,
      "mass_properties": {
        "mass": 10.0,
        "volume": 10000.0,
        "density": 0.001,
        "center_of_mass": {"x": 0, "y": 0, "z": 0},
        "moments_of_inertia": {
          "xx": 1.0, "yy": 1.0, "zz": 1.0,
          "xy": 0.0, "yz": 0.0, "xz": 0.0
        }
      },
      "material": {"name": "Steel", "id": "steel-1"},
      "geometry_file": "BodyName.stl"
    }
  ],
  "joints": [
    {
      "name": "JointName",
      "type": "RevoluteJointType",
      "body_one": "Body1",
      "body_two": "Body2",
      "origin": {"x": 0, "y": 0, "z": 0}
    }
  ],
  "metadata": {
    "exported_from": "Autodesk Fusion 360",
    "export_script": "ExportToPyChrono.py",
    "units": "mm"
  }
}
```

## Supported Joint Types

- **Revolute** - Rotational joint (hinge)
- **Rigid** - Fixed connection
- **Slider** - Translational joint (prismatic)

Additional joint types can be added by extending the `create_joint_from_data` function in `pychrono_loader.py`.

## Unit Conversion

- **Fusion 360**: Uses millimeters (mm) by default
- **PyChrono**: Typically uses meters (m)
- The loader automatically converts units from mm to m

## Limitations

- Currently exports solid bodies only (no surface bodies)
- Joint axis orientation is simplified
- Material properties are exported but not automatically applied to PyChrono materials
- Mesh collision may be computationally expensive for complex geometries

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**gabboraron**

## References

- [Autodesk Fusion 360 API](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A)
- [PyChrono Documentation](https://api.projectchrono.org/pychrono_introduction.html)
- [Project Chrono](https://projectchrono.org/)
