# Quick Start Guide

This guide will help you get started with exporting Fusion 360 models for PyChrono simulations.

## Step 1: Install Fusion 360 Script

1. **Locate Your Scripts Folder**:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts`
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts`

2. **Copy the Script**:
   - Copy `ExportToPyChrono.py` to your scripts folder
   - Restart Fusion 360 if it's already running

3. **Verify Installation**:
   - In Fusion 360, go to **Tools** → **Scripts and Add-Ins**
   - Look for `ExportToPyChrono` in the **My Scripts** tab
   - If you see it, installation was successful!

## Step 2: Export Your First Model

1. **Open a Model** in Fusion 360
   - Create a simple model or open an existing one
   - Make sure it has at least one solid body

2. **Run the Export Script**:
   - Go to **Tools** → **Scripts and Add-Ins**
   - Select `ExportToPyChrono`
   - Click **Run**

3. **Select Output Folder**:
   - Choose where to save the exported files
   - Click **OK**

4. **Check the Output**:
   - You should see:
     - `<model_name>_pychrono.json` - Model data
     - `geometries/` folder - STL files for each body

## Step 3: Install PyChrono

```bash
# Install PyChrono
pip install pychrono

# Optional: Install visualization support
pip install pychrono[irrlicht]
```

## Step 4: Run a Simulation

1. **Validate Your Export**:
   ```bash
   python utils.py validate model_pychrono.json
   ```

2. **View Model Summary**:
   ```bash
   python utils.py summary model_pychrono.json
   ```

3. **Run the Simulation**:
   ```bash
   python example_simulation.py model_pychrono.json
   ```

## Example: Simple Pendulum

Let's create a simple pendulum in Fusion 360 and export it:

### In Fusion 360:

1. Create a new design
2. Create a rectangular ground plane (100mm × 100mm × 10mm)
3. Create a cylindrical pendulum arm (10mm diameter, 100mm long)
4. Create a revolute joint connecting them
5. Run the export script

### In Python:

```python
from pychrono_loader import load_model_from_json, create_visualization

# Load the model
system = load_model_from_json('pendulum_pychrono.json')

# Create visualization
app = create_visualization(system, "Pendulum Simulation")
app.SetTimestep(0.01)

# Run simulation
while app.GetDevice().run():
    app.BeginScene()
    app.DrawAll()
    app.DoStep()
    app.EndScene()
```

## Troubleshooting

### Script Doesn't Appear in Fusion 360

- **Problem**: Script not showing in Scripts and Add-Ins
- **Solution**: 
  - Check that you copied it to the correct folder
  - Restart Fusion 360
  - Make sure the file has a `.py` extension

### Export Creates Empty JSON

- **Problem**: JSON file is generated but has no bodies
- **Solution**:
  - Make sure your model has solid bodies (not just sketches)
  - Check that bodies are visible
  - Try exporting individual components

### PyChrono Import Error

- **Problem**: `ImportError: No module named pychrono`
- **Solution**:
  ```bash
  pip install pychrono
  ```

### STL Files Not Generated

- **Problem**: JSON exports but no geometries folder
- **Solution**:
  - Check that you have write permissions in the output folder
  - Make sure bodies are solid (not surface or mesh bodies)
  - Try exporting to a different folder

### Visualization Window Doesn't Open

- **Problem**: Simulation runs but no window appears
- **Solution**:
  - Install Irrlicht support: `pip install pychrono[irrlicht]`
  - If still failing, run headless simulation instead
  - Check that your display is available (not SSH session without X11)

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore `example_simulation.py` for more simulation options
- Check `utils.py` for data validation and conversion tools
- Modify `export_config.json` to customize export settings

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Validate your export: `python utils.py validate your_model.json`
3. Check model summary: `python utils.py summary your_model.json`
4. Open an issue on GitHub with:
   - Error message
   - Model JSON file (if possible)
   - Steps to reproduce

## Tips for Best Results

1. **Keep Models Simple**: Start with simple models before trying complex assemblies
2. **Name Components**: Give meaningful names to bodies and joints in Fusion 360
3. **Check Mass Properties**: Verify that Fusion 360 calculated mass properties correctly
4. **Test Incrementally**: Export and test frequently during model development
5. **Use Appropriate Units**: Remember Fusion 360 uses mm, PyChrono typically uses m

Happy simulating! 🚀
