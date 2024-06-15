import numpy as np
import matplotlib.pyplot as plt
import math
import os
from quiz_agent import quiz
import datetime


path = "/Users/gleb/Desktop/Obsedian/My Obsidian Brain/Learning & Development/Monthly Review/monthly_review.md"
image_path = "/Users/gleb/Desktop/Obsedian/My Obsidian Brain/pics/"

def read_topics(path):
    with open(path, 'r') as file:
        topics = file.read().splitlines()
        return topics
    
def calculate_elapsed_months(date_str):
    date_format = "%d/%m/%Y"
    given_date = datetime.datetime.strptime(date_str, date_format)
    today = datetime.datetime.now()
    diff = abs((today.year - given_date.year) * 12 + (today.month - given_date.month))
    return diff

def headings_and_subheadings(topics):
    headings = {}
    current_heading = None

    for line in topics:
        if line.startswith('# Monthly'):
            current_heading = 'Monthly'
            headings[current_heading] = {}
        elif line.startswith('\t- ') and current_heading == 'Monthly':
            parts = line[3:].strip().split('{')
            if len(parts) == 2:
                subheading = parts[0].strip()
                data = parts[1].rstrip('}')
                data_dict = {}
                for item in data.split(','):
                    key_value = item.strip().split(':')
                    if len(key_value) == 2:
                        key = key_value[0].strip()
                        value = key_value[1].strip()
                        data_dict[key] = value
                elapsed_months = calculate_elapsed_months(data_dict['t'])
                if 1 <= elapsed_months <= 2:
                    data_dict['t'] = elapsed_months
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
            't': int(data.get('t', 0.1)),
            'Q': str(data.get('Q', 'N'))
        }
        subjects.append(topic)

t = np.linspace(0, 12, 400)

plt.ion()

with open(path, 'a') as md_file:
    image_index = 1

    for heading in headings_dict.keys():
        fig, ax = plt.subplots(figsize=(10, 6))
        print(heading)

        for subject in subjects:
            if subject['heading'] == heading:
                if 'Y' in subject['Q']:
                    IU = subject['IU']
                    D = subject['D']
                    N = subject['N']
                    C = subject['C']
                    I = subject['I']
                    elapsed_time = subject['t']
                    print(f'elapsed time is:{elapsed_time}')

                    IU_prime = (IU * 0.25) / 10
                    D_prime = (1 / (D * 0.4)) / 40
                    N_prime = 1 / (N * 0.25)
                    C_prime = (C * 0.25) / 10
                    I_prime = I
                    c = 10

                    initial_understanding = (IU / 10) * 100

                    Understanding = initial_understanding * np.exp((-t / (IU_prime * D_prime * C_prime * 2)) * (1 / (N_prime * 30)) * (1 / c))

                    idx = np.abs(t - elapsed_time).argmin()
                    current_understanding = Understanding[idx]

                    importance_index = current_understanding * I
                    print(f"Importance index for {subject['subheading']}: {importance_index}")

                    ax.plot(t, Understanding, label=subject['subheading'], linewidth=1.5)
                    ax.scatter(elapsed_time, current_understanding, s=100, label=f'{subject["subheading"]} CU', zorder=5)

                    quiz_response = quiz(heading, subject['subheading'], importance_index)
                    md_file.write(f"\n\n## {subject['subheading']}\n")
                    md_file.write(quiz_response)
                else: pass
            else:pass

        ax.set_xlabel('Time (months)')
        ax.set_ylabel('Understanding (%)')
        ax.set_title(f'Retention Curve For {heading}')
        ax.legend()
        ax.grid(True)

        figure_filename = f"{heading.replace(' ', '_')}_{image_index}.png"
        figure_path = os.path.join(image_path, figure_filename)
        plt.savefig(figure_path, dpi=300, bbox_inches='tight')

        md_file.write(f'\n\n![[{figure_filename}]]\n')

        image_index += 1

        plt.pause(0.001)

plt.show(block=True)