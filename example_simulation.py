"""
Example PyChrono Simulation
============================

This example demonstrates how to load a Fusion 360 exported model
and run a PyChrono simulation.

Requirements:
    - PyChrono (pip install pychrono)
    - Exported model files from Fusion 360

Author: gabboraron
License: MIT
"""

try:
    import pychrono as chrono
    PYCHRONO_AVAILABLE = True
except ImportError:
    PYCHRONO_AVAILABLE = False

from pychrono_loader import load_model_from_json, create_visualization

def run_simulation(json_path, duration=5.0, time_step=0.01):
    """
    Run a PyChrono simulation from exported Fusion 360 data.
    
    Args:
        json_path: Path to exported JSON file
        duration: Simulation duration in seconds
        time_step: Simulation time step in seconds
    """
    if not PYCHRONO_AVAILABLE:
        raise ImportError("PyChrono is not installed. Please install it first.")
    
    print("Loading model from:", json_path)
    
    # Load the model
    system = load_model_from_json(json_path)
    
    print(f"Loaded {system.Get_bodylist().size()} bodies")
    print(f"Loaded {system.Get_linklist().size()} constraints")
    
    # Create visualization
    app = create_visualization(system, "Fusion 360 Model - PyChrono Simulation")
    
    # Set up rendering
    app.AssetBindAll()
    app.AssetUpdateAll()
    
    # Simulation loop
    app.SetTimestep(time_step)
    app.SetTryRealtime(True)
    
    print("\nStarting simulation...")
    print(f"Duration: {duration}s, Time step: {time_step}s")
    
    simulation_time = 0
    while app.GetDevice().run() and simulation_time < duration:
        app.BeginScene()
        app.DrawAll()
        app.DoStep()
        app.EndScene()
        
        simulation_time = system.GetChTime()
        
        # Print progress every second
        if int(simulation_time) > int(simulation_time - time_step):
            print(f"Simulation time: {simulation_time:.1f}s")
    
    print("Simulation completed!")


def run_headless_simulation(json_path, duration=5.0, time_step=0.01):
    """
    Run a PyChrono simulation without visualization (headless mode).
    
    Args:
        json_path: Path to exported JSON file
        duration: Simulation duration in seconds
        time_step: Simulation time step in seconds
    """
    if not PYCHRONO_AVAILABLE:
        raise ImportError("PyChrono is not installed. Please install it first.")
    
    print("Loading model from:", json_path)
    
    # Load the model
    system = load_model_from_json(json_path)
    
    print(f"Loaded {system.Get_bodylist().size()} bodies")
    print(f"Loaded {system.Get_linklist().size()} constraints")
    
    # Set up time stepper
    system.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_LINEARIZED)
    
    print("\nStarting headless simulation...")
    print(f"Duration: {duration}s, Time step: {time_step}s")
    
    # Simulation loop
    time = 0
    while time < duration:
        system.DoStepDynamics(time_step)
        time = system.GetChTime()
        
        # Print progress every second
        if int(time) > int(time - time_step):
            print(f"Simulation time: {time:.1f}s")
    
    print("Simulation completed!")
    
    # Print final body positions
    print("\nFinal body positions:")
    for body in system.Get_bodylist():
        pos = body.GetPos()
        print(f"  {body.GetName()}: ({pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f})")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("PyChrono Simulation Example")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python example_simulation.py <path_to_json> [duration] [timestep]")
        print("\nExample:")
        print("  python example_simulation.py model_pychrono.json 5.0 0.01")
        print("\nArguments:")
        print("  path_to_json: Path to exported Fusion 360 JSON file")
        print("  duration: Simulation duration in seconds (default: 5.0)")
        print("  time_step: Simulation time step in seconds (default: 0.01)")
        sys.exit(1)
    
    json_path = sys.argv[1]
    duration = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    time_step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
    
    # Check if file exists
    import os
    if not os.path.exists(json_path):
        print(f"\nError: File not found: {json_path}")
        sys.exit(1)
    
    # Run simulation with visualization
    try:
        run_simulation(json_path, duration, time_step)
    except ImportError as e:
        print(f"\nVisualization not available: {e}")
        print("Running headless simulation instead...")
        run_headless_simulation(json_path, duration, time_step)
