"""
Configuration parameters for the communication network simulation.
All parameters can be modified to match real-world scenarios.
"""

# Time parameters
SENSING_INTERVAL = 15  # minutes
TDMA_SLOT_DURATION = 10  # seconds
TDMA_CYCLE_DURATION = 3600  # seconds (1 hour)

# Communication parameters
BAUD_RATE = 300  # bits per second
FREQUENCY_BAND = (401, 402)  # MHz

# Data parameters
RAW_PACKET_SIZE = 375  # bytes (300 bits/sec × 10 sec = 3000 bits = 375 bytes)
USABLE_PAYLOAD = 250  # bytes (after protocol overhead)
PROTOCOL_OVERHEAD = RAW_PACKET_SIZE - USABLE_PAYLOAD  # bytes

# Network parameters
NUM_NODES = 5  # number of communication nodes (can be set to 2527 for full network)
SATELLITE_PROPAGATION_DELAY = 0.25  # seconds (typical GEO satellite delay)

# Data collection parameters
DATA_POINTS_PER_PACKET = 10  # number of sensor readings per transmission
SENSOR_ACCURACY = 0.95  # sensor measurement accuracy (95%)

# Power consumption parameters
TX_VOLTAGE = 12.0  # V DC
TX_CURRENT = 1.8  # A during transmission
STANDBY_VOLTAGE = 12.0  # V DC
STANDBY_CURRENT = 0.0028  # A during standby (2.8 mA)
GPS_VOLTAGE = 12.0  # V DC
GPS_CURRENT = 0.025  # A during GPS fix (25 mA)
GPS_FIX_DURATION = 60  # seconds for GPS fix

# Energy calculations
TX_ENERGY_PER_TRANSMISSION = TX_VOLTAGE * TX_CURRENT * TDMA_SLOT_DURATION  # Joules
TX_ENERGY_PER_TRANSMISSION_WH = TX_ENERGY_PER_TRANSMISSION / 3600  # Wh
TX_ENERGY_PER_DAY = TX_ENERGY_PER_TRANSMISSION_WH * 24  # Wh/day
STANDBY_ENERGY_PER_DAY = STANDBY_VOLTAGE * STANDBY_CURRENT * 24  # Wh/day
GPS_ENERGY_PER_DAY = GPS_VOLTAGE * GPS_CURRENT * GPS_FIX_DURATION * 24 / 3600  # Wh/day
TOTAL_ENERGY_PER_DAY = TX_ENERGY_PER_DAY + STANDBY_ENERGY_PER_DAY + GPS_ENERGY_PER_DAY  # Wh/day
TOTAL_NETWORK_ENERGY_PER_DAY = TOTAL_ENERGY_PER_DAY * NUM_NODES  # Wh/day

# Data throughput calculations
DATA_PER_TRANSMISSION = USABLE_PAYLOAD  # bytes
DATA_PER_DAY = DATA_PER_TRANSMISSION * 24  # bytes/day
TOTAL_NETWORK_DATA_PER_DAY = DATA_PER_DAY * NUM_NODES  # bytes/day
RAW_NETWORK_DATA_PER_DAY = RAW_PACKET_SIZE * 24 * NUM_NODES  # bytes/day

# Time efficiency parameters
ACTIVE_TIME_PER_DAY = TDMA_SLOT_DURATION * 24  # seconds
TOTAL_TIME_PER_DAY = 24 * 3600  # seconds
CHANNEL_UTILIZATION = ACTIVE_TIME_PER_DAY / TOTAL_TIME_PER_DAY * 100  # percentage

# Visualization parameters
PLOT_REFRESH_RATE = 1  # seconds
ANIMATION_SPEED = 1  # multiplier for animation speed 