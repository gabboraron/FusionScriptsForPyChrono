"""
PyChrono Loader Module
======================

This module loads exported Fusion 360 data and creates PyChrono simulation objects.

Usage:
    from pychrono_loader import load_model_from_json
    
    system = load_model_from_json('model_pychrono.json', 'geometries/')
    # system now contains PyChrono bodies and constraints

Author: gabboraron
License: MIT
"""

import json
import os
from pathlib import Path

try:
    import pychrono as chrono
    import pychrono.irrlicht as chronoirr
    PYCHRONO_AVAILABLE = True
except ImportError:
    PYCHRONO_AVAILABLE = False
    print("Warning: PyChrono not installed. This module requires PyChrono to function.")


def load_model_from_json(json_path, geometry_dir=None):
    """
    Load a Fusion 360 exported model into PyChrono.
    
    Args:
        json_path: Path to the JSON file exported from Fusion 360
        geometry_dir: Directory containing STL geometry files
    
    Returns:
        chrono.ChSystem: PyChrono system with loaded bodies and constraints
    """
    if not PYCHRONO_AVAILABLE:
        raise ImportError("PyChrono is not installed. Please install it first.")
    
    # Load JSON data
    with open(json_path, 'r') as f:
        model_data = json.load(f)
    
    # Create PyChrono system
    system = chrono.ChSystemNSC()
    system.Set_G_acc(chrono.ChVectorD(0, -9.81, 0))  # Set gravity
    
    # Set geometry directory
    if geometry_dir is None:
        geometry_dir = os.path.join(os.path.dirname(json_path), 'geometries')
    
    # Create bodies
    body_map = {}
    for body_data in model_data.get('bodies', []):
        body = create_body_from_data(body_data, geometry_dir, system)
        if body:
            body_map[body_data['name']] = body
    
    # Create joints/constraints
    for joint_data in model_data.get('joints', []):
        create_joint_from_data(joint_data, body_map, system)
    
    return system


def create_body_from_data(body_data, geometry_dir, system):
    """
    Create a PyChrono body from exported data.
    
    Args:
        body_data: Dictionary with body data
        geometry_dir: Directory containing geometry files
        system: PyChrono system to add body to
    
    Returns:
        chrono.ChBody: Created body
    """
    # Create body
    body = chrono.ChBody()
    body.SetName(body_data['name'])
    
    # Set mass properties
    mass_props = body_data.get('mass_properties', {})
    if mass_props:
        mass = mass_props.get('mass', 1.0)
        body.SetMass(mass)
        
        # Set center of mass
        com = mass_props.get('center_of_mass', {})
        if com:
            # Convert from mm to m (Fusion uses mm, Chrono typically uses m)
            body.SetPos(chrono.ChVectorD(
                com.get('x', 0) / 1000.0,
                com.get('y', 0) / 1000.0,
                com.get('z', 0) / 1000.0
            ))
        
        # Set inertia tensor
        inertia = mass_props.get('moments_of_inertia', {})
        if inertia:
            body.SetInertiaXX(chrono.ChVectorD(
                inertia.get('xx', 1.0),
                inertia.get('yy', 1.0),
                inertia.get('zz', 1.0)
            ))
    
    # Apply transformation if present
    transform = body_data.get('transform', {})
    if transform:
        translation = transform.get('translation', {})
        if translation:
            pos = chrono.ChVectorD(
                translation.get('x', 0) / 1000.0,
                translation.get('y', 0) / 1000.0,
                translation.get('z', 0) / 1000.0
            )
            body.SetPos(pos)
    
    # Load collision geometry from STL if available
    geom_file = body_data.get('geometry_file')
    if geom_file:
        stl_path = os.path.join(geometry_dir, geom_file)
        if os.path.exists(stl_path):
            # Enable collision
            body.SetCollide(True)
            
            # Create collision model
            body.GetCollisionModel().ClearModel()
            
            # Load mesh for collision
            mesh = chrono.ChTriangleMeshConnected()
            # Use appropriate method based on file extension
            if stl_path.lower().endswith('.stl'):
                # Note: PyChrono API may vary by version
                # Try STL-specific loading if available
                try:
                    mesh.LoadSTLMesh(stl_path)
                except AttributeError:
                    # Fallback for older PyChrono versions or if STL method not available
                    mesh.LoadWavefrontMesh(stl_path, True, True)
            else:
                mesh.LoadWavefrontMesh(stl_path, True, True)
            
            # Add mesh to collision model
            body.GetCollisionModel().AddTriangleMesh(
                chrono.ChMaterialSurfaceNSC(),
                mesh,
                False,  # is_static
                False,  # is_convex
                chrono.ChVectorD(0, 0, 0),
                chrono.ChMatrix33D(1)
            )
            
            body.GetCollisionModel().BuildModel()
            
            # Also add visual shape
            mesh_shape = chrono.ChTriangleMeshShape()
            mesh_shape.SetMesh(mesh)
            # Use newer API if available, fallback to older
            try:
                body.AddVisualShape(mesh_shape)
            except AttributeError:
                body.AddAsset(mesh_shape)
    
    # Set body as fixed if needed (ground bodies)
    if body_data.get('is_fixed', False):
        body.SetBodyFixed(True)
    
    # Add body to system
    system.Add(body)
    
    return body


def create_joint_from_data(joint_data, body_map, system):
    """
    Create a PyChrono constraint from exported joint data.
    
    Args:
        joint_data: Dictionary with joint data
        body_map: Dictionary mapping body names to ChBody objects
        system: PyChrono system to add constraint to
    
    Returns:
        chrono.ChLink: Created joint/constraint
    """
    joint_type = joint_data.get('type', '')
    
    # Get connected bodies
    body_one_name = joint_data.get('body_one')
    body_two_name = joint_data.get('body_two')
    
    if not body_one_name or not body_two_name:
        return None
    
    body_one = body_map.get(body_one_name)
    body_two = body_map.get(body_two_name)
    
    if not body_one or not body_two:
        return None
    
    # Get joint origin
    origin = joint_data.get('origin', {})
    origin_pos = chrono.ChVectorD(
        origin.get('x', 0) / 1000.0,
        origin.get('y', 0) / 1000.0,
        origin.get('z', 0) / 1000.0
    )
    
    # Create appropriate joint type
    joint = None
    
    if 'Revolute' in joint_type or 'RevoluteJointType' in joint_type:
        joint = chrono.ChLinkLockRevolute()
        joint.Initialize(body_one, body_two, 
                        chrono.ChCoordsysD(origin_pos))
    
    elif 'Rigid' in joint_type or 'RigidJointType' in joint_type:
        joint = chrono.ChLinkLockLock()
        joint.Initialize(body_one, body_two,
                        chrono.ChCoordsysD(origin_pos))
    
    elif 'Slider' in joint_type or 'SliderJointType' in joint_type:
        joint = chrono.ChLinkLockPrismatic()
        joint.Initialize(body_one, body_two,
                        chrono.ChCoordsysD(origin_pos))
    
    if joint:
        joint.SetName(joint_data.get('name', ''))
        system.Add(joint)
    
    return joint


def create_visualization(system, window_title="PyChrono Simulation"):
    """
    Create Irrlicht visualization for the system.
    
    Args:
        system: PyChrono system to visualize
        window_title: Title for the visualization window
    
    Returns:
        chronoirr.ChIrrApp: Irrlicht application
    """
    if not PYCHRONO_AVAILABLE:
        raise ImportError("PyChrono is not installed.")
    
    # Create Irrlicht application
    app = chronoirr.ChIrrApp(
        system,
        window_title,
        chronoirr.dimension2du(1024, 768)
    )
    
    app.AddTypicalSky()
    app.AddTypicalLights()
    app.AddTypicalCamera(chronoirr.vector3df(2, 2, 2))
    
    return app


# Example usage
if __name__ == "__main__":
    print("PyChrono Loader Module")
    print("=" * 50)
    print("\nThis module provides functions to load Fusion 360")
    print("exported models into PyChrono simulations.")
    print("\nExample usage:")
    print("  from pychrono_loader import load_model_from_json")
    print("  system = load_model_from_json('model.json')")
    print("\nPyChrono available:", PYCHRONO_AVAILABLE)
