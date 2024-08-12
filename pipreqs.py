import os
import subprocess


def generate_requirements(project_path):
    # Generate requirements.txt using pipreqs
    try:
        subprocess.run(["pipreqs", project_path, "--force"], check=True)
        print("requirements.txt generated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    # Read the generated requirements.txt to extract package names
    requirements_file = os.path.join(project_path, "requirements.txt")

    if os.path.exists(requirements_file):
        with open(requirements_file, "r") as file:
            packages = [line.split("==")[0] for line in file.readlines()]

        print("Extracted Packages:")
        for package in packages:
            print(package)

        return packages
    else:
        print("requirements.txt not found.")
        return []


# Provide the path to your project directory
project_path = "C:/Users/sakib51/Documents/requirement_generation/exampleProject"

# Generate the requirements and extract package names
packages = generate_requirements(project_path)
