import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from src import config
from src.visualization import NetworkVisualizer
import random

class EmergencyCommunicationNode:
    def __init__(self, node_id, position, emergency=False):
        self.node_id = node_id
        self.position = position
        self.data_buffer = []
        self.last_transmission = None
        self.slot_number = node_id  
        self.power_state = 'standby'
        self.transmission_count = 0
        self.total_bytes_sent = 0
        self.emergency = emergency
        self.battery_voltage = 12.0
        self.solar_voltage = 14.0
        self.gps_fix = (0.0, 0.0)
        self.sensor_diagnostics = 0b00000000
        self.emergency_flag = 0b00000000
        self.last_values = []

    def collect_data(self, timestamp):
        value = np.random.normal(0, 1)
        self.last_values.append(value)
        if len(self.last_values) > 12:
            self.last_values.pop(0)
        data = {
            'timestamp': timestamp,
            'value': value,
            'accuracy': config.SENSOR_ACCURACY,
            'battery_voltage': self.battery_voltage,
            'solar_voltage': self.solar_voltage,
            'gps_fix': self.gps_fix,
            'diagnostics': self.sensor_diagnostics,
            'emergency_flag': self.emergency_flag
        }
        self.data_buffer.append(data)

    def can_transmit(self, current_time):
        if self.emergency:
            scheduled = (current_time % 300 == 0)
            goes_random = random.random() < 0.02  
            return scheduled or goes_random
        else:
            cycle_time = current_time % config.TDMA_CYCLE_DURATION
            slot_start = self.slot_number * config.TDMA_SLOT_DURATION
            return slot_start <= cycle_time < slot_start + config.TDMA_SLOT_DURATION

    def update_power_state(self, current_time):
        if self.can_transmit(current_time):
            self.power_state = 'tx'
        elif current_time % 3600 < 60:
            self.power_state = 'gps'
        else:
            self.power_state = 'standby'

    def transmit_data(self, current_time):
        if self.can_transmit(current_time) and self.data_buffer:
            if self.emergency:
                num_readings = random.randint(5, 12)
                readings = self.last_values[-num_readings:]
                timestamps = [current_time - 60 * i for i in range(num_readings)][::-1]
                trend = np.diff(readings).tolist() if len(readings) > 1 else [0]
                packet_size = random.randint(400, 750)
                packet = {
                    'timestamps': timestamps,
                    'readings': readings,
                    'trend': trend,
                    'battery_voltage': self.battery_voltage,
                    'solar_voltage': self.solar_voltage,
                    'gps_fix': self.gps_fix,
                    'diagnostics': self.sensor_diagnostics,
                    'emergency_flag': 0b10000010, 
                    'packet_size': packet_size
                }
                self.transmission_count += 1
                self.total_bytes_sent += packet_size
                return packet
            else:
                packet = self.data_buffer.pop(0)
                self.transmission_count += 1
                self.total_bytes_sent += config.RAW_PACKET_SIZE
                return packet
        return None

class EmergencySatellite:
    def __init__(self, position):
        self.position = position
        self.received_packets = []
        self.total_bytes_received = 0

    def receive_packet(self, packet, timestamp):
        size = packet.get('packet_size', config.RAW_PACKET_SIZE)
        self.received_packets.append({
            'packet': packet,
            'timestamp': timestamp + config.SATELLITE_PROPAGATION_DELAY
        })
        self.total_bytes_received += size

class EmergencyNetworkSimulation:
    def __init__(self):
        self.nodes = []
        self.satellite = EmergencySatellite((0, 0))
        self.setup_network()
        self.current_time = 0
        self.visualizer = EmergencyNetworkVisualizer(self)

    def setup_network(self):
        for i in range(config.NUM_NODES):
            angle = 2 * np.pi * i / config.NUM_NODES
            radius = 5
            position = (radius * np.cos(angle), radius * np.sin(angle))
            emergency = (i == 0 or i == 1)
            self.nodes.append(EmergencyCommunicationNode(i, position, emergency=emergency))

    def update(self, frame):
        self.current_time = frame
        for node in self.nodes:
            node.update_power_state(self.current_time)
            if node.emergency:
                if self.current_time % (5 * 60) == 0:
                    node.collect_data(self.current_time)
            else:
                if self.current_time % (config.SENSING_INTERVAL * 60) == 0:
                    node.collect_data(self.current_time)
            packet = node.transmit_data(self.current_time)
            if packet:
                self.satellite.receive_packet(packet, self.current_time)
        self.visualizer.update(frame)

    def run_simulation(self):
        frames = np.arange(0, 1800, 1)  
        ani = FuncAnimation(self.visualizer.fig, self.update,
                            frames=frames,
                            interval=50,
                            blit=False)
        ani.save('output/emergency_mode_simulation.mp4', writer='ffmpeg', fps=20,
                 extra_args=['-vcodec', 'libx264'],
                 savefig_kwargs={'facecolor': 'white'})
        plt.show()

class EmergencyNetworkVisualizer(NetworkVisualizer):
    def setup_visualization(self):
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.grid(True)
        self.ax.set_title('Network Communication (Emergency Mode Demo)', pad=20, fontsize=14)
        self.ground_station = (0, -7)
        self.ax.scatter(self.ground_station[0], self.ground_station[1],
                        color='purple', s=200, label='Ground Station')
        self.ax.scatter(0, 0, color='red', s=200, label='Satellite')
        for node in self.simulation.nodes:
            color = 'orange' if getattr(node, 'emergency', False) else 'blue'
            edgecolor = 'red' if getattr(node, 'emergency', False) else 'black'
            self.ax.scatter(node.position[0], node.position[1],
                            color=color, edgecolors=edgecolor, s=120, label=f'Node {node.node_id}')
        self.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    def update(self, frame):
        self.ax.clear()
        self.setup_visualization()
        current_time = frame
        for node in self.simulation.nodes:
            if node.can_transmit(current_time):
                progress = (current_time % (300 if node.emergency else config.TDMA_SLOT_DURATION)) / (300 if node.emergency else config.TDMA_SLOT_DURATION)
                self.ax.plot([node.position[0], 0], [node.position[1], 0],
                             'g--', alpha=0.7 if node.emergency else 0.5, linewidth=2)
                packet_x = node.position[0] + (0 - node.position[0]) * progress
                packet_y = node.position[1] + (0 - node.position[1]) * progress
                pkt_color = 'red' if node.emergency else 'yellow'
                self.ax.scatter(packet_x, packet_y, color=pkt_color, s=70 if node.emergency else 50,
                                label='Emergency Packet' if node.emergency and progress == 0 else ('Data Packet' if progress == 0 else ''))
                if progress > 0.5:
                    self.ax.plot([0, self.ground_station[0]], [0, self.ground_station[1]],
                                 'r--', alpha=0.7 if node.emergency else 0.5, linewidth=2)
                    ground_progress = (progress - 0.5) * 2
                    ground_x = 0 + (self.ground_station[0] - 0) * ground_progress
                    ground_y = 0 + (self.ground_station[1] - 0) * ground_progress
                    self.ax.scatter(ground_x, ground_y, color='red' if node.emergency else 'orange', s=70 if node.emergency else 50)
            # Add info
            if node.emergency:
                self.ax.text(node.position[0], node.position[1] + 0.7,
                             f'EMERGENCY\nTX every 5min\n{node.transmission_count} pkts',
                             ha='center', va='bottom', fontsize=11, color='red', fontweight='bold')
            else:
                cycle_time = current_time % config.TDMA_CYCLE_DURATION
                slot_start = node.slot_number * config.TDMA_SLOT_DURATION
                if slot_start <= cycle_time < slot_start + config.TDMA_SLOT_DURATION:
                    self.ax.text(node.position[0], node.position[1] + 0.5,
                                 f'Transmitting\n{config.BAUD_RATE} baud',
                                 ha='center', va='bottom', fontsize=10)
                else:
                    time_until_transmit = (slot_start - cycle_time) % config.TDMA_CYCLE_DURATION
                    self.ax.text(node.position[0], node.position[1] + 0.5,
                                 f'Next TX in\n{int(time_until_transmit//60)}m {int(time_until_transmit%60)}s',
                                 ha='center', va='bottom', fontsize=10)
        hours = current_time // 3600
        minutes = (current_time % 3600) // 60
        seconds = current_time % 60
        self.ax.text(-7, 7, f'Time: {hours:02d}:{minutes:02d}:{seconds:02d}',
                     fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        self.fig.tight_layout()

if __name__ == "__main__":
    sim = EmergencyNetworkSimulation()
    sim.run_simulation() 