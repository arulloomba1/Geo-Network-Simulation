import matplotlib.pyplot as plt
import numpy as np
from src import config
from matplotlib.patches import Circle, Arrow
from matplotlib.animation import FuncAnimation

class NetworkVisualizer:
    def __init__(self, simulation):
        self.simulation = simulation
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111)
        self.setup_visualization()
        self.packet_positions = {} 
        
    def setup_visualization(self):
        """Setup the network topology visualization"""
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.grid(True)
        self.ax.set_title('Network Communication', pad=20, fontsize=14)
        
        self.ground_station = (0, -7)
        self.ax.scatter(self.ground_station[0], self.ground_station[1], 
                       color='purple', s=200, label='Ground Station')
        
        self.ax.scatter(0, 0, color='red', s=200, label='Satellite')

        # Legend
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
    def update(self, frame):
        """Update the visualization"""
        self.ax.clear()
        self.setup_visualization()
        
        # Packet positions
        current_time = frame
        for node in self.simulation.nodes:
            if node.can_transmit(current_time):
                # Packet position between node and satellite
                progress = (current_time % config.TDMA_SLOT_DURATION) / config.TDMA_SLOT_DURATION
                
                # Transmit line from node to satellite
                self.ax.plot([node.position[0], 0], [node.position[1], 0], 
                           'g--', alpha=0.5, linewidth=2)
                
                # Animated packet
                packet_x = node.position[0] + (0 - node.position[0]) * progress
                packet_y = node.position[1] + (0 - node.position[1]) * progress
                self.ax.scatter(packet_x, packet_y, color='yellow', s=50, 
                              label='Data Packet' if progress == 0 else '')
                
                if progress > 0.5:
                    # Transmit line from satellite to ground station
                    self.ax.plot([0, self.ground_station[0]], [0, self.ground_station[1]], 
                               'r--', alpha=0.5, linewidth=2)
                    
                    # Animated packet to ground station
                    ground_progress = (progress - 0.5) * 2
                    ground_x = 0 + (self.ground_station[0] - 0) * ground_progress
                    ground_y = 0 + (self.ground_station[1] - 0) * ground_progress
                    self.ax.scatter(ground_x, ground_y, color='orange', s=50)
            
            # Transmission timing info
            cycle_time = current_time % config.TDMA_CYCLE_DURATION
            slot_start = node.slot_number * config.TDMA_SLOT_DURATION
            if slot_start <= cycle_time < slot_start + config.TDMA_SLOT_DURATION:
                self.ax.text(node.position[0], node.position[1] + 0.5,
                           f'Transmitting\n{config.BAUD_RATE} baud',
                           ha='center', va='bottom', fontsize=10)
            else:
                time_until_transmit = (slot_start - cycle_time) % config.TDMA_CYCLE_DURATION
                self.ax.text(node.position[0], node.position[1] + 0.5,
                           f'Next TX in\n{time_until_transmit//60}m {time_until_transmit%60}s',
                           ha='center', va='bottom', fontsize=10)
        
        # Time display
        hours = current_time // 3600
        minutes = (current_time % 3600) // 60
        seconds = current_time % 60
        self.ax.text(-7, 7, f'Time: {hours:02d}:{minutes:02d}:{seconds:02d}',
                    fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        
        self.fig.tight_layout() 