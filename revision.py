###CONDA ENVIRONMENT: conda activate monthly_revision
import numpy as np
import matplotlib.pyplot as plt
import math


# --- A SIMILAR CHART WITH A DIFFERNT CONSTANT IS ALSO NEEDED FOR WEEKLY REVIEW. ---


# Upload a list of topics √
# Use MCTS algorithm (Importance Index is incorrect!!!)
# Plot the topics forgetfulness curve
# Develop a quiz for each topic. Append it to the end of the file. 
# Develop interconnection quiz. To force me to RECALL OLD TOPICS I'VE COVERED THAT MIGHT BE RELATED. (TAG THEM ON OBSEDIAN)?

path = "/Users/gleb/Desktop/Obsedian/My Obsidian Brain/Learning & Development/monthly_review.md"

### --- READING & WRITING THE FILE LOGIC  --- ### √

def read_topics(path):
    with open(path, 'r') as file:
        topics = file.read().splitlines()
        return topics

def headings_and_subheadings(topics):
    headings = {}
    current_heading = None

    for line in topics:
        if line.startswith('- '):
            current_heading = line[2:].strip()
            headings[current_heading] = {}
        elif line.startswith('\t- ') and current_heading:
            parts = line[3:].strip().split('{')  # Split subheading and data
            if len(parts) == 2:  # Ensure both parts are present
                subheading = parts[0].strip()
                data = parts[1].rstrip('}')  # Remove closing brace
                data_dict = {}
                for item in data.split(','):
                    key_value = item.strip().split(':')  # Split key-value pairs
                    if len(key_value) == 2:  # Ensure key-value pair is valid
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        data_dict[key] = value
                headings[current_heading][subheading] = data_dict

    return headings

# Replace 'path' with the actual path to your file
import math  # Import the math module

topics = read_topics(path)
headings_dict = headings_and_subheadings(topics)

# Print the results
for heading, subheadings in headings_dict.items():
    print(f"{heading}:")
    for subheading, data in subheadings.items():
        print(f"  - {subheading}: {data}")



## --- MCTS  --- ### √
# Importance needs adding to the equation I: out of 10

#{IU': 10, 'D': 1, 'n': 10, 'c': 10, 'C': 10, 't': 2}

# def mcts(headings_dict): ### To be used instead of the parameters bellow


### --- 3. PLOTTING THE FORGETFULNESS CURVE LOGIC  --- ### √
import numpy as np
import matplotlib.pyplot as plt

# List of subjects with their respective parameters
subjects = [
    {'name': 'Subject 1', 'I':10, 'IU': 10, 'D': 1, 'N': 10000000, 'c': 10, 'C': 10, 't': 1},  # Assuming subject 1 was visited 2 months ago
    {'name': 'Subject 2', 'I':10, 'IU': 7, 'D': 2, 'N': 0, 'c': 7, 'C': 10, 't': 1},      
    {'name': 'Subject 3', 'I':2, 'IU': 5, 'D': 3, 'N': 0, 'c': 5, 'C': 10, 't': 1},      
    # Add more subjects as needed
]

# Time range (e.g., 0 to 12 months)
t = np.linspace(0, 12, 400)

plt.figure(figsize=(10, 6))

for subject in subjects:
    IU = subject['IU']
    D = subject['D']
    N = subject['N'] # Number of times the subject was visited should inverse the importance of the revisit!!!
    c = subject['c']
    C = subject['C']
    I = subject['I']
    elapsed_time = subject['t']  # Time elapsed since subject was last visited

    # Normalize the values
    IU_prime = (IU * 0.25) / 10
    D_prime = (1 / (D * 0.4)) / 10
    N_prime = (N * 0.25) / 10
    C_prime = (C * 0.25) / 10
    I_prime = I

    # Initial understanding as a percentage
    initial_understanding = (IU / 10) * 100

    # Calculate retention using the modified formula
    Understanding = initial_understanding * np.exp(-t / (IU_prime * D_prime * C_prime * c * C)) ###

    # Gets the Y value Current Understanding (CU) based on elapsed time x (shown in the plot). i.e: shows where the point is on the plot
    #returns it in %
    idx = np.abs(t - elapsed_time).argmin()
    current_understanding = Understanding[idx]
    importance_index = current_understanding * I
    print(f"Importance index for {subject['name']}: {importance_index}")

    # Plotting each subject's understanding curve
    plt.plot(t, Understanding, label=subject['name'], linewidth=2.5)

    # Plotting Current Understanding (CU) as a point on the curve
    plt.scatter(elapsed_time, current_understanding, s=100, label=f'{subject["name"]} CU', zorder=5)

    # Print Current Understanding (CU) for each subject
    # print(f"Current Understanding for {subject['name']}: {current_understanding}")

    # Importance = I_prime + IU_prime + N_prime + C_prime
    # print(Importance)

# Plot settings
plt.xlabel('Time (months)')
plt.ylabel('Understanding (%)')
plt.title('Forgetfulness Curve for Multiple Subjects')
plt.legend()
plt.grid(True)
plt.show()
