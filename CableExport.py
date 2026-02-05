"""
Code to export cables (sketch lines) from Fusion 360 to a CSV file with world coordinates.
The CSV format is:
StartX,StartY,StartZ,EndX,EndY,EndZ

This script should be run in Fusion 360's scripting environment. 
It will prompt the user to select sketch lines (representing cables) and then save their start and end points in world coordinates to a CSV file. 
The coordinates are converted from centimeters (Fusion's default unit) to meters for compatibility with PyChrono.
"""
import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # 1. Check if there is a selection
        sel = ui.activeSelections
        if sel.count == 0:
            ui.messageBox('Error: Please first select the cable lines in the sketch!')
            return

        # 2. Open save dialog
        fileDlg = ui.createFileDialog()
        fileDlg.isMultiSelectEnabled = False
        fileDlg.title = 'Save cable coordinates to CSV'
        fileDlg.filter = 'CSV files (*.csv)'
        
        if fileDlg.showSave() != adsk.core.DialogResults.DialogOK:
            return
        
        filename = fileDlg.filename

        # 3. Extract and write data
        count = 0
        with open(filename, 'w') as f:
            # Write header (required for Pandas)
            f.write('StartX,StartY,StartZ,EndX,EndY,EndZ\n')
            
            for i in range(sel.count):
                entity = sel.item(i).entity
                
                # Only process if it's a line (SketchLine)
                if isinstance(entity, adsk.fusion.SketchLine):
                    # Extract world coordinates (WorldGeometry)
                    # Fusion default unit is Centimeter
                    start_point = entity.startSketchPoint.worldGeometry
                    end_point = entity.endSketchPoint.worldGeometry
                    
                    # Convert to METERS (/100), as PyChrono uses SI units
                    sx = start_point.x / 100.0
                    sy = start_point.y / 100.0
                    sz = start_point.z / 100.0
                    
                    ex = end_point.x / 100.0
                    ey = end_point.y / 100.0
                    ez = end_point.z / 100.0
                    
                    # Write row to file
                    f.write(f"{sx},{sy},{sz},{ex},{ey},{ez}\n")
                    count += 1
        
        ui.messageBox(f'Success! Coordinates of {count} cables exported to:\n{filename}')

    except:
        if ui:
            ui.messageBox('An error occurred:\n{}'.format(traceback.format_exc()))
