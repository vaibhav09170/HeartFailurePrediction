from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirements_lst:List[str] = []
    try:
        with open("requirements.txt","r") as file:
            requirements_lines = file.readlines()
            for line in requirements_lines:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirements_lst.append(requirement)
    
    except FileNotFoundError:
        print("requirements.txt not found")
    
    return requirements_lst    
#test
print(get_requirements())

setup(
    name="HeartFailurePrediction",
    version="0.0.1",
    author="vaibhav",
    author_email="vaibhav09170@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)