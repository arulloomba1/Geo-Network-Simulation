# Geo-Network Simulation

This project simulates a geostationary satellite communication network with multiple data collection points (DCPs). The simulation models the TDMA-based communication protocol and visualizes the network topology and data flow.

## Features

- Real-time visualization of network topology
- TDMA-based communication scheduling
- Configurable network parameters
- Simulated data collection and transmission
- Satellite propagation delay modeling
- Emergency mode simulation with rich packet content and visual highlighting

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the simulation:
```bash
python run_simulation.py
```

3. Run the emergency mode demo:
```bash
python -m src.emergency_mode_animation
```

## Configuration

All network parameters can be modified in `src/config.py`, including:
- Time parameters (sensing interval, TDMA slot duration)
- Communication parameters (packet size, baud rate)
- Network parameters (number of nodes, propagation delay)
- Data collection parameters
- Visualization settings

## Project Structure

- `src/` — All source code
  - `network_simulation.py`: Main simulation logic and visualization
  - `emergency_mode_animation.py`: Emergency mode demo with rich packet content
  - `config.py`: Network parameters and configuration
  - `visualization.py`: Visualization utilities
- `output/`: Simulation outputs (mp4, gif, etc.)
- `tests/`: Unit tests (empty for now)
- `requirements.txt`: Project dependencies
- `run_simulation.py`: Entry point for the main simulation
- `README.md`: Project documentation

## Future Improvements

- Add data analysis and statistics
- Implement more sophisticated TDMA scheduling
- Add error modeling and packet loss simulation
- Include power consumption modeling
- Add optimization algorithms for network efficiency 