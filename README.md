# FusionScriptsForPyChrono

A collection of scripts for exporting model data from Autodesk Fusion 360 to use with PyChrono physics simulations.

## Overview

This repository provides tools and scripts to bridge Autodesk Fusion 360 CAD models with PyChrono physics simulations. The goal is to streamline the workflow of designing mechanical systems in Fusion 360 and simulating their physical behavior using the PyChrono physics engine.

## What is Autodesk Fusion 360?

[Autodesk Fusion 360](https://www.autodesk.com/products/fusion-360/) is a cloud-based 3D modeling, CAD, CAM, CAE, and PCB software platform for product design and manufacturing. Key features include:

- **Parametric and Direct Modeling**: Create complex 3D models with history-based parametric modeling or direct shape manipulation
- **Assembly Design**: Build assemblies with joints, constraints, and motion studies
- **Simulation**: Built-in stress analysis, thermal simulation, and motion studies
- **API & Scripting**: Python and C++ APIs for automation and custom functionality
- **Collaboration**: Cloud-based storage and version control for team projects

### Fusion 360 Scripting

Fusion 360 supports scripting through its API, allowing users to:
- Automate repetitive design tasks
- Export custom data formats
- Create custom commands and tools
- Extract geometry, mass properties, and assembly information
- Access joint definitions and motion constraints

Scripts can be written in **Python** or **C++** and are accessed through the **Scripts and Add-Ins** dialog in Fusion 360.

## What is PyChrono?

[PyChrono](https://projectchrono.org/) is the Python interface to Project Chrono, a physics-based simulation infrastructure. It specializes in:

- **Multibody Dynamics**: Simulation of rigid and flexible body systems
- **Contact Mechanics**: Advanced collision detection and contact force computation
- **Vehicle Dynamics**: Specialized modules for simulating wheeled and tracked vehicles
- **Robotics**: Simulation of robotic systems with motors, sensors, and control
- **Finite Element Analysis**: Structural analysis with FEA capabilities
- **Fluid-Solid Interaction**: Coupling with SPH and other fluid solvers

### Why Use PyChrono with Fusion 360?

1. **Accurate Physics**: PyChrono provides more detailed physics simulation than Fusion 360's built-in motion study
2. **Custom Scenarios**: Test designs under specific conditions not available in Fusion 360
3. **Automation**: Run batch simulations with different parameters
4. **Advanced Analysis**: Access to specialized physics modules (granular materials, fluids, etc.)
5. **Python Ecosystem**: Integrate with scientific Python libraries (NumPy, Matplotlib, etc.)

## Installation

### Prerequisites

- **Autodesk Fusion 360**: Download and install from [Autodesk website](https://www.autodesk.com/products/fusion-360/)
- **Python**: Version 3.7 or higher
- **PyChrono**: Install via pip or conda

### Installing PyChrono

```bash
# Using pip
pip install pychrono

# Or using conda (recommended)
conda install -c projectchrono pychrono
```

### Setting Up Fusion 360 Scripts

1. Open Fusion 360
2. Go to **Tools** → **Add-Ins** → **Scripts and Add-Ins**
3. Click the **+** button next to "My Scripts"
4. Navigate to this repository's scripts folder
5. Select a script to run

## Usage

### Basic Workflow

1. **Design in Fusion 360**: Create your mechanical system with proper joints and constraints
2. **Export Model Data**: Run a Fusion 360 script to export geometry, mass properties, and joint information
3. **Create PyChrono Simulation**: Use the exported data to set up a physics simulation
4. **Analyze Results**: Run the simulation and visualize/analyze the results

### Example Structure

```
FusionScriptsForPyChrono/
├── fusion_scripts/          # Fusion 360 Python scripts
│   ├── export_assembly.py   # Export complete assembly data
│   └── export_joints.py     # Export joint definitions
├── pychrono_scripts/        # PyChrono simulation scripts
│   ├── import_model.py      # Import Fusion 360 data
│   └── run_simulation.py    # Run physics simulation
└── examples/                # Example projects
    └── simple_mechanism/    # Complete example workflow
```

## Features (Planned)

- [ ] Export geometric data (meshes, primitives)
- [ ] Export mass and inertia properties
- [ ] Export joint definitions and constraints
- [ ] Convert Fusion 360 materials to PyChrono material properties
- [ ] Generate PyChrono simulation templates
- [ ] Visualization tools for comparing results

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- New export features
- Additional simulation examples
- Documentation improvements
- Performance optimizations

## Resources

### Autodesk Fusion 360
- [Fusion 360 API Documentation](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A)
- [Fusion 360 API Samples](https://github.com/AutodeskFusion360/Fusion360Samples)
- [Fusion 360 Community Forums](https://forums.autodesk.com/t5/fusion-360/ct-p/1234)

### PyChrono
- [PyChrono Documentation](https://api.projectchrono.org/pychrono_introduction.html)
- [PyChrono Tutorials](https://github.com/projectchrono/chrono/tree/main/src/demos/python)
- [Project Chrono Website](https://projectchrono.org/)

### Tutorials
- [Getting Started with Fusion 360 API](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A)
- [PyChrono Getting Started Guide](https://api.projectchrono.org/tutorial_table_of_content_pychrono.html)

## License

This project is licensed under the Mozilla Public License Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Autodesk for providing the Fusion 360 API
- Project Chrono team for developing the PyChrono physics engine
- The open-source community for various tools and libraries

## Status

⚠️ **This project is in early development.** Scripts and features are being actively developed. Check back for updates or watch the repository for notifications.
