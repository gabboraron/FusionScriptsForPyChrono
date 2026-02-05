"""
Fusion 360 Script to Export Model Data for PyChrono Simulations
================================================================

This script extracts model data from Autodesk Fusion 360 and exports it
in a format suitable for PyChrono physics simulations.

Usage:
    1. Open your model in Fusion 360
    2. Run this script from Scripts and Add-Ins
    3. Select output directory for exported data
    4. The script will generate JSON files with model data

Author: gabboraron
License: MIT
"""

import adsk.core
import adsk.fusion
import traceback
import json
import os
from pathlib import Path


def run(context):
    """Main entry point for the Fusion 360 script."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get the active design
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('No active design found. Please open a design first.')
            return
        
        # Get the root component
        rootComp = design.rootComponent
        
        # Ask user for output directory
        folderDlg = ui.createFolderDialog()
        folderDlg.title = 'Select Output Folder for PyChrono Export'
        dlgResult = folderDlg.showDialog()
        if dlgResult != adsk.core.DialogResults.DialogOK:
            return
        
        output_dir = folderDlg.folder
        
        # Extract model data
        model_data = extract_model_data(rootComp, design)
        
        # Export to JSON
        output_path = os.path.join(output_dir, f'{design.rootComponent.name}_pychrono.json')
        export_to_json(model_data, output_path)
        
        # Export STL files for geometry
        export_geometries(rootComp, output_dir)
        
        ui.messageBox(f'Export completed successfully!\n\nFiles saved to:\n{output_dir}')
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def extract_model_data(rootComp, design):
    """
    Extract relevant model data from Fusion 360 component.
    
    Args:
        rootComp: Root component of the design
        design: Active design object
    
    Returns:
        Dictionary containing model data for PyChrono
    """
    model_data = {
        'model_name': rootComp.name,
        'bodies': [],
        'joints': [],
        'materials': [],
        'metadata': {
            'exported_from': 'Autodesk Fusion 360',
            'export_script': 'ExportToPyChrono.py',
            'units': 'mm'  # Fusion 360 default
        }
    }
    
    # Extract bodies
    for occurrence in rootComp.allOccurrences:
        for body in occurrence.bodies:
            if body.isSolid:
                body_data = extract_body_data(body, occurrence)
                if body_data:
                    model_data['bodies'].append(body_data)
    
    # Also extract bodies from root component
    for body in rootComp.bodies:
        if body.isSolid:
            body_data = extract_body_data(body, None)
            if body_data:
                model_data['bodies'].append(body_data)
    
    # Extract joints
    joints = rootComp.allJoints
    for joint in joints:
        joint_data = extract_joint_data(joint)
        if joint_data:
            model_data['joints'].append(joint_data)
    
    return model_data


def extract_body_data(body, occurrence):
    """
    Extract data from a single body.
    
    Args:
        body: Fusion 360 body object
        occurrence: Occurrence containing the body (or None for root)
    
    Returns:
        Dictionary with body data
    """
    body_data = {
        'name': body.name,
        'is_visible': body.isVisible,
        'mass_properties': {},
        'material': None,
        'geometry_file': f'{body.name}.stl'
    }
    
    # Get physical properties
    physical_props = body.physicalProperties
    if physical_props:
        try:
            # Get mass properties
            body_data['mass_properties'] = {
                'mass': physical_props.mass,  # kg
                'volume': physical_props.volume,  # cm^3
                'area': physical_props.area,  # cm^2
                'density': physical_props.density,  # kg/cm^3
                'center_of_mass': {
                    'x': physical_props.centerOfMass.x,
                    'y': physical_props.centerOfMass.y,
                    'z': physical_props.centerOfMass.z
                }
            }
            
            # Get moments of inertia
            (returnValue, xx, yy, zz, xy, yz, xz) = physical_props.getXYZMomentsOfInertia()
            if returnValue:
                body_data['mass_properties']['moments_of_inertia'] = {
                    'xx': xx,
                    'yy': yy,
                    'zz': zz,
                    'xy': xy,
                    'yz': yz,
                    'xz': xz
                }
        except:
            pass
    
    # Get material
    if body.material:
        body_data['material'] = {
            'name': body.material.name,
            'id': body.material.id
        }
    
    # Get transformation if part of occurrence
    if occurrence:
        transform = occurrence.transform
        body_data['transform'] = {
            'translation': {
                'x': transform.translation.x,
                'y': transform.translation.y,
                'z': transform.translation.z
            }
        }
    
    return body_data


def extract_joint_data(joint):
    """
    Extract data from a joint.
    
    Args:
        joint: Fusion 360 joint object
    
    Returns:
        Dictionary with joint data
    """
    joint_data = {
        'name': joint.name,
        'type': joint.jointMotion.jointType.toString(),
        'is_suppressed': joint.isSuppressed
    }
    
    # Get connected bodies
    if joint.occurrenceOne:
        joint_data['body_one'] = joint.occurrenceOne.name
    
    if joint.occurrenceTwo:
        joint_data['body_two'] = joint.occurrenceTwo.name
    
    # Get joint origin
    geometry_or_origin = joint.geometryOrOriginOne
    if geometry_or_origin:
        origin = geometry_or_origin.origin
        if origin:
            joint_data['origin'] = {
                'x': origin.x,
                'y': origin.y,
                'z': origin.z
            }
    
    return joint_data


def export_to_json(data, output_path):
    """
    Export model data to JSON file.
    
    Args:
        data: Dictionary containing model data
        output_path: Path to output JSON file
    """
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)


def export_geometries(rootComp, output_dir):
    """
    Export body geometries as STL files.
    
    Args:
        rootComp: Root component
        output_dir: Directory to save STL files
    """
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    exportMgr = design.exportManager
    
    # Create geometry subdirectory
    geom_dir = os.path.join(output_dir, 'geometries')
    if not os.path.exists(geom_dir):
        os.makedirs(geom_dir)
    
    # Export each body as STL
    all_bodies = []
    
    # Get bodies from occurrences
    for occurrence in rootComp.allOccurrences:
        for body in occurrence.bodies:
            if body.isSolid:
                all_bodies.append((body, body.name))
    
    # Get bodies from root
    for body in rootComp.bodies:
        if body.isSolid:
            all_bodies.append((body, body.name))
    
    # Export each body
    for body, name in all_bodies:
        try:
            stl_path = os.path.join(geom_dir, f'{name}.stl')
            stlOptions = exportMgr.createSTLExportOptions(body, stl_path)
            stlOptions.sendToPrintUtility = False
            exportMgr.execute(stlOptions)
        except:
            pass  # Continue with other bodies if one fails
