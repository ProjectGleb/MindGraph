import numpy as np
import matplotlib.pyplot as plt
import math
import os

# --- A SIMILAR CHART WITH A DIFFERENT CONSTANT IS ALSO NEEDED FOR WEEKLY REVIEW. ---

# Upload a list of topics √
# Use MCTS algorithm (Importance Index is incorrect!!!)
# Plot the topics forgetfulness curve
# Develop a quiz for each topic. Append it to the end of the file.
# Develop interconnection quiz. To force me to RECALL OLD TOPICS I'VE COVERED THAT MIGHT BE RELATED. (TAG THEM ON OBSEDIAN)?

path = "/Users/gleb/Desktop/Obsedian/My Obsidian Brain/Learning & Development/Monthly Review/monthly_review.md"
image_path = "/Users/gleb/Desktop/Obsedian/My Obsidian Brain/pics/"

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

topics = read_topics(path)
headings_dict = headings_and_subheadings(topics)

subjects = []

for heading, subheadings in headings_dict.items():
    for subheading, data in subheadings.items():
        topic = {
            'heading': heading,
            'subheading': subheading,
            'I': int(data.get('I', 1)),
            'IU': int(data.get('IU', 1)),
            'D': int(data.get('D', 1)),
            'N': int(data.get('N', 1)),
            'C': int(data.get('C', 1)),
            't': int(data.get('t', 1))
        }
        subjects.append(topic)

# Time range (e.g., 0 to 12 months)
t = np.linspace(0, 12, 400)

# Turn on interactive mode
plt.ion()

# Open the .md file for appending
with open(path, 'a') as md_file:
    image_index = 1  # Initialize image index

    # Create a figure for each header
    for heading in headings_dict.keys():
        fig, ax = plt.subplots(figsize=(10, 6))

        for subject in subjects:
            if subject['heading'] == heading:
                IU = subject['IU']
                D = subject['D']
                N = subject['N']
                C = subject['C']
                I = subject['I']
                elapsed_time = subject['t']

                # Normalize the values
                IU_prime = (IU * 0.25) / 10
                D_prime = (1 / (D * 0.4)) / 40
                N_prime = 1 / (N * 0.25)
                C_prime = (C * 0.25) / 10
                I_prime = I
                c = 10

                # Initial understanding as a percentage
                initial_understanding = (IU / 10) * 100

                # Calculate retention using the modified formula
                Understanding = initial_understanding * np.exp((-t / (IU_prime * D_prime * C_prime * 2)) * (1 / (N_prime * 30)) * (1 / c))

                # Find the index corresponding to the elapsed time
                idx = np.abs(t - elapsed_time).argmin()
                current_understanding = Understanding[idx]

                importance_index = current_understanding * I
                print(f"Importance index for {subject['subheading']}: {importance_index}")

                # Plotting each subject's understanding curve
                ax.plot(t, Understanding, label=subject['subheading'], linewidth=1.5)

                # Plotting Current Understanding (CU) as a point on the curve
                ax.scatter(elapsed_time, current_understanding, s=100, label=f'{subject["subheading"]} CU', zorder=5)

        # Plot settings
        ax.set_xlabel('Time (months)')
        ax.set_ylabel('Understanding (%)')
        ax.set_title(f'Retention Curve For {heading}')
        ax.legend()
        ax.grid(True)

        # Save the figure to the 'pics' directory with an index
        figure_filename = f"{heading.replace(' ', '_')}_{image_index}.png"
        figure_path = os.path.join(image_path, figure_filename)
        plt.savefig(figure_path, dpi=300, bbox_inches='tight')

        # Append the image path to the .md file using the ![[image_path]] format
        md_file.write(f'\n\n![[{figure_filename}]]\n')

        # Increment the image index
        image_index += 1

        # Display the plot (non-blocking)
        plt.pause(0.001)

# Keep the script running until all plots are displayed
plt.show(block=True)