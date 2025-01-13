import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess

# Extract the components of the orientation tensor
subprocess.run("cat log.simulation | grep -w 'Time =' | cut -d' ' -f3 | tr -d '(' > time", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $2}' | tr -d '()' | awk -F' ' '{print $1}' > r11", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $3}' | tr -d '()' | awk -F' ' '{print $1}' > r12", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $4}' | tr -d '()' | awk -F' ' '{print $1}' > r13", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $5}' | tr -d '()' | awk -F' ' '{print $1}' > r21", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $6}' | tr -d '()' | awk -F' ' '{print $1}' > r22", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $7}' | tr -d '()' | awk -F' ' '{print $1}' > r23", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $8}' | tr -d '()' | awk -F' ' '{print $1}' > r31", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $9}' | tr -d '()' | awk -F' ' '{print $1}' > r32", shell=True)
subprocess.run("cat log.simulation | grep 'Orientation' | awk '{print $10}' | tr -d '()' | awk -F' ' '{print $1}' > r33", shell=True)

# Combine orientation components with other extracted data
subprocess.run("paste time r11 r12 r13 r21 r22 r23 r31 r32 r33 > plotfile2", shell=True)


# Function to load the generated data from the plotfile
def load_data():
    plotfile_path = "/home/lollilol/Desktop/fsi_6dof/background_zone/plotfile2"
    
    # Attempt to load the data with error handling for inconsistent rows
    try:
        # Use np.genfromtxt with 'invalid_raise=False' to skip rows with inconsistent column count
        data = np.genfromtxt(plotfile_path, delimiter=None, invalid_raise=False)  # Skip problematic rows
        
        # Check if data has the correct number of columns (10 columns expected)
        if data.ndim == 1:
            print("Data appears to be one-dimensional. Checking file format...")
            with open(plotfile_path, 'r') as f:
                for i, line in enumerate(f.readlines()[:5]):
                    print(f"Line {i}: {line.strip()}")
            raise ValueError("Data is not in the expected multi-column format.")
        
        # Verify that each row has exactly 10 columns, otherwise skip
        expected_columns = 10
        data = [row for row in data if len(row) == expected_columns]
        
        if len(data) == 0:
            raise ValueError("No valid data found with the correct number of columns.")
        
        data = np.array(data)  # Convert to numpy array for further processing
        
        # Extract columns for time, center of mass coordinates, linear velocities, and angular velocities
        time = data[:, 0]
        r11 = data[:, 1]
        r12 = data[:, 2]
        r13 = data[:, 3]
        r21 = data[:, 4]
        r22 = data[:, 5]
        r23 = data[:, 6]
        r31 = data[:, 7]
        r32 = data[:, 8]
        r33 = data[:, 9]

		    
        return time, r11, r12, r13, r21, r22, r23, r31, r32, r33 
    
    except Exception as e:
        print(f"Error loading data from {plotfile_path}: {e}")
        return None



