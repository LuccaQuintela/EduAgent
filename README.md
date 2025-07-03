# EduAgent: A Multi-Agent Collaborative Learning Tutor

An A.I. powered tutoring system designed to help anyone learn any subject efficiently and for free. 

## Features

- Builds flexible and evolving curriculums.
- Creates individual lessons per module within the curriculum.
- Finds additional learning material online for the student to pull from.
- Creates quizes for the modules and tests them on the student.
- Uses the results from the quizes to adjust the curriculum and individual lessons.
- Builds a learning schedule with built-in practice for applicable subjects.

## Tech Stack
- [Google Agent Development Kit](https://google.github.io/adk-docs/)
- Python
- Conda (for environment management)

### Usage Instructions

In order to run this code yourself, you will need to first set up your virtual environment properly. 
First, install anaconda and then once in the root diretory of the project, run these commands.

##### On first time.
``` conda env create -f environment.yml ```

##### Once the environment is created, run this everytime you wish to enter environment. 
``` conda activate eduagent ```

##### When you wish to exit the environment, run this.
``` conda deactivate ```

If you wish to run each of the agent's individually and take a look at their event logs with visualizations, 
run the following terminal command, take the link it provides and paste it into your web browser. 
Make sure your pwd is `EduAgent/agents/` before doing so.
``` adk web ```