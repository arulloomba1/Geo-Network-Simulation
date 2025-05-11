import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from datetime import datetime, timedelta
import config
from visualization import NetworkVisualizer

class CommunicationNode:
    def __init__(self, node_id, position):
        self.node_id = node_id
        self.position = position
        self.data_buffer = []
        self.last_transmission = None
        self.slot_number = node_id  
        self.power_state = 'standby' 
        self.transmission_count = 0
        self.total_bytes_sent = 0

    def collect_data(self, timestamp):
        """Simulate data collection from sensors"""
        data = {
            'timestamp': timestamp,
            'value': np.random.normal(0, 1),  
            'accuracy': config.SENSOR_ACCURACY
        }
        self.data_buffer.append(data)

    def can_transmit(self, current_time):
        """Check if it's this node's turn to transmit"""
        cycle_time = current_time % config.TDMA_CYCLE_DURATION
        slot_start = self.slot_number * config.TDMA_SLOT_DURATION
        return slot_start <= cycle_time < slot_start + config.TDMA_SLOT_DURATION
    
    def update_power_state(self, current_time):
        """Update the node's power state based on current time"""
        if self.can_transmit(current_time):
            self.power_state = 'tx'
        elif current_time % 3600 < 60: 
            self.power_state = 'gps'
        else:
            self.power_state = 'standby'
            
    def transmit_data(self, current_time):
        """Transmit data if it's the node's turn"""
        if self.can_transmit(current_time) and self.data_buffer:
            # Simulate transmission
            packet = self.data_buffer.pop(0)
            self.transmission_count += 1
            self.total_bytes_sent += config.RAW_PACKET_SIZE
            return packet
        return None

class Satellite:
    def __init__(self, position):
        self.position = position
        self.received_packets = []
        self.total_bytes_received = 0

    def receive_packet(self, packet, timestamp):
        """Simulate packet reception with propagation delay"""
        self.received_packets.append({
            'packet': packet,
            'timestamp': timestamp + config.SATELLITE_PROPAGATION_DELAY
        })
        self.total_bytes_received += config.RAW_PACKET_SIZE

class NetworkSimulation:
    def __init__(self):
        self.nodes = []
        self.satellite = Satellite((0, 0)) 
        self.setup_network()
        self.current_time = 0
        self.visualizer = NetworkVisualizer(self)
        
    def setup_network(self):
        """Initialize network nodes in a circular pattern"""
        for i in range(config.NUM_NODES):
            angle = 2 * np.pi * i / config.NUM_NODES
            radius = 5
            position = (radius * np.cos(angle), radius * np.sin(angle))
            self.nodes.append(CommunicationNode(i, position))
            
    def update(self, frame):
        """Update the simulation state"""
        self.current_time = frame
        
        for node in self.nodes:
            node.update_power_state(self.current_time)
            
            if self.current_time % (config.SENSING_INTERVAL * 60) == 0:
                node.collect_data(self.current_time)
                
            packet = node.transmit_data(self.current_time)
            if packet:
                self.satellite.receive_packet(packet, self.current_time)
                
        self.visualizer.update(frame)
        
    def run_simulation(self):
        """Run the network simulation"""
        frames = np.arange(0, 2*3600, 1)  
        
        ani = FuncAnimation(self.visualizer.fig, self.update,
                          frames=frames,
                          interval=50,  
                          blit=False)
        
        ani.save('network_simulation.mp4', writer='ffmpeg', fps=20, 
                extra_args=['-vcodec', 'libx264'], 
                savefig_kwargs={'facecolor': 'white'})
        
        plt.show()
        
    def get_network_statistics(self):
        """Get current network statistics"""
        stats = {
            'total_transmissions': sum(node.transmission_count for node in self.nodes),
            'total_bytes_sent': sum(node.total_bytes_sent for node in self.nodes),
            'total_bytes_received': self.satellite.total_bytes_received,
            'buffer_sizes': [len(node.data_buffer) for node in self.nodes],
            'channel_utilization': config.CHANNEL_UTILIZATION,
            'energy_per_node': config.TOTAL_ENERGY_PER_DAY
        }
        return stats

if __name__ == "__main__":
    simulation = NetworkSimulation()
    simulation.run_simulation() 