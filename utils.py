"""
Utility Functions for Fusion 360 to PyChrono Export
====================================================

This module provides utility functions for data conversion and validation.

Author: gabboraron
License: MIT
"""

import json
import os


def validate_json_export(json_path):
    """
    Validate that an exported JSON file has the correct structure.
    
    Args:
        json_path: Path to JSON file to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Check required fields
        required_fields = ['model_name', 'bodies', 'joints', 'metadata']
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
        
        # Validate bodies
        if not isinstance(data['bodies'], list):
            return False, "bodies must be a list"
        
        for i, body in enumerate(data['bodies']):
            if 'name' not in body:
                return False, f"Body {i} missing 'name' field"
            if 'mass_properties' not in body:
                return False, f"Body {body['name']} missing 'mass_properties'"
        
        # Validate joints
        if not isinstance(data['joints'], list):
            return False, "joints must be a list"
        
        for i, joint in enumerate(data['joints']):
            if 'name' not in joint:
                return False, f"Joint {i} missing 'name' field"
            if 'type' not in joint:
                return False, f"Joint {joint.get('name', i)} missing 'type' field"
        
        return True, "Valid"
        
    except json.JSONDecodeError as e:
        return False, f"JSON parsing error: {str(e)}"
    except FileNotFoundError:
        return False, f"File not found: {json_path}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def convert_units(value, from_unit, to_unit):
    """
    Convert between different units.
    
    Args:
        value: Numeric value to convert
        from_unit: Source unit ('mm', 'cm', 'm', 'in')
        to_unit: Target unit ('mm', 'cm', 'm', 'in')
    
    Returns:
        float: Converted value
    """
    # Define conversion factors to meters
    to_meters = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'in': 0.0254,
        'ft': 0.3048
    }
    
    if from_unit not in to_meters or to_unit not in to_meters:
        raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")
    
    # Convert to meters first, then to target unit
    value_in_meters = value * to_meters[from_unit]
    result = value_in_meters / to_meters[to_unit]
    
    return result


def get_model_summary(json_path):
    """
    Get a summary of the exported model.
    
    Args:
        json_path: Path to JSON file
    
    Returns:
        dict: Summary information
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        summary = {
            'model_name': data.get('model_name', 'Unknown'),
            'num_bodies': len(data.get('bodies', [])),
            'num_joints': len(data.get('joints', [])),
            'units': data.get('metadata', {}).get('units', 'unknown'),
            'bodies': [body['name'] for body in data.get('bodies', [])],
            'joints': [joint['name'] for joint in data.get('joints', [])]
        }
        
        # Calculate total mass
        total_mass = sum(
            body.get('mass_properties', {}).get('mass', 0)
            for body in data.get('bodies', [])
        )
        summary['total_mass'] = total_mass
        
        return summary
        
    except Exception as e:
        return {'error': str(e)}


def print_model_summary(json_path):
    """
    Print a formatted summary of the exported model.
    
    Args:
        json_path: Path to JSON file
    """
    summary = get_model_summary(json_path)
    
    if 'error' in summary:
        print(f"Error reading model: {summary['error']}")
        return
    
    print("=" * 60)
    print("Model Summary")
    print("=" * 60)
    print(f"Model Name: {summary['model_name']}")
    print(f"Units: {summary['units']}")
    print(f"Total Mass: {summary['total_mass']:.2f} kg")
    print(f"\nBodies ({summary['num_bodies']}):")
    for body_name in summary['bodies']:
        print(f"  - {body_name}")
    print(f"\nJoints ({summary['num_joints']}):")
    for joint_name in summary['joints']:
        print(f"  - {joint_name}")
    print("=" * 60)


def create_export_config(output_path='export_config.json'):
    """
    Create a default export configuration file.
    
    Args:
        output_path: Path to save configuration file
    """
    config = {
        'export_settings': {
            'export_stl': True,
            'stl_quality': 'medium',  # low, medium, high
            'export_mass_properties': True,
            'export_joints': True,
            'export_materials': True,
            'unit_conversion': {
                'from': 'mm',
                'to': 'm'
            }
        },
        'simulation_settings': {
            'gravity': [0, -9.81, 0],
            'time_step': 0.01,
            'solver_type': 'NSC',  # NSC or SMC
            'default_material': {
                'friction': 0.5,
                'restitution': 0.1
            }
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuration file created: {output_path}")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Fusion 360 to PyChrono - Utility Functions")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python utils.py <command> [arguments]")
        print("\nCommands:")
        print("  validate <json_file>  - Validate exported JSON file")
        print("  summary <json_file>   - Print model summary")
        print("  config [output_path]  - Create default config file")
        print("\nExamples:")
        print("  python utils.py validate model_pychrono.json")
        print("  python utils.py summary model_pychrono.json")
        print("  python utils.py config export_config.json")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'validate':
        if len(sys.argv) < 3:
            print("Error: Please provide JSON file path")
            sys.exit(1)
        
        json_path = sys.argv[2]
        is_valid, message = validate_json_export(json_path)
        
        if is_valid:
            print(f"✓ Valid export file: {json_path}")
        else:
            print(f"✗ Invalid export file: {message}")
            sys.exit(1)
    
    elif command == 'summary':
        if len(sys.argv) < 3:
            print("Error: Please provide JSON file path")
            sys.exit(1)
        
        json_path = sys.argv[2]
        print_model_summary(json_path)
    
    elif command == 'config':
        output_path = sys.argv[2] if len(sys.argv) > 2 else 'export_config.json'
        create_export_config(output_path)
    
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)
