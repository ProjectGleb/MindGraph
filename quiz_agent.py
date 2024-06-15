#Getting user input, and making a plan
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import requests
load_dotenv()


def quiz(heading, subheading, importance_index):
    # activate chatGPT agent
    import os

    api_key = os.getenv("OPENAI_API_KEY")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"""You are a {heading} tutor of a university student.\n
                The student wants to reherse the topic {subheading}. Your job is to provide him 3 test questions at once, on that topic in the incresing order of difficulty. First question should be about his understanding of the overall topic. When mathematical notation is needed for the quesiton you must use the LaTeX notation. Since it will be printed in Obsedian, put the latex formulas inside dounble $$ like in the example. Else it wont be formatted properly. Try not to be overly wordy and leave no enter spaces between questions. Lastly, paste the importance index:{importance_index} before the questions.\n
                Example:
                Importance Index: {importance_index}
                Questions:
                1. Essence of Linear Transformation: What is linear transformation and why is it important?
                2. Transformation Proof: 2. Show that the transformation $T: \mathbb{{R}}^3 \rightarrow \mathbb{{R}}^3$ defined by $T(x, y, z) = (x + y, y + z, x - z)$ is a linear transformation.
                3. Applying linear transformation: Given the linear transformation $T: \mathbb{{R}}^3 \rightarrow \mathbb{{R}}^3$ defined by the matrix $$ A = \begin{{pmatrix}} 1 & 2 & 3 \\ 0 & -1 & 1 \\ 2 & 0 & 1 \end{{pmatrix}} $$ compute $T(1, 0, 1)$ and $T(2, -1, 0)$.
                """
            },
            {
                "role": "user",
                "content": f"The student wants to reherse the topic {subheading}."
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json()['choices'][0]['message']['content'])
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)



