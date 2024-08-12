import requests
from datetime import datetime

# Input the key dates
repo_creation_date = datetime.strptime("2015-06-20", "%Y-%m-%d")
last_update_date = datetime.strptime("2021-04-12", "%Y-%m-%d")

# Path to your generated requirements.txt file
requirements_path = (
    "C:/Users/sakib51/Documents/requirement_generation/exampleProject/requirements.txt"
)
new_requirements_path = "C:/Users/sakib51/Documents/requirement_generation/exampleProject/new_requirements.txt"


def read_requirements(file_path):
    with open(file_path, "r") as file:
        packages = [line.split("==")[0].strip() for line in file.readlines()]
    return packages


def get_pypi_versions(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for package: {package_name}")
        return []

    data = response.json()
    versions = []

    for version, release_info in data["releases"].items():
        if release_info:  # Check if there is release information available
            release_date = release_info[0]["upload_time"]
            release_date = datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%S")
            versions.append((version, release_date))

    return versions


def get_closest_versions(package_name, repo_creation_date, last_update_date):
    versions = get_pypi_versions(package_name)
    closest_creation_version = None
    closest_update_version = None
    min_creation_diff = float("inf")
    min_update_diff = float("inf")

    for version, release_date in versions:
        creation_diff = abs((release_date - repo_creation_date).days)
        update_diff = abs((release_date - last_update_date).days)

        if creation_diff < min_creation_diff:
            min_creation_diff = creation_diff
            closest_creation_version = version

        if update_diff < min_update_diff:
            min_update_diff = update_diff
            closest_update_version = version

    return closest_creation_version, closest_update_version


def write_new_requirements(packages, repo_creation_date, last_update_date, output_path):
    with open(output_path, "w") as file:
        for package in packages:
            creation_version, update_version = get_closest_versions(
                package, repo_creation_date, last_update_date
            )

            if creation_version and update_version:
                file.write(f"{package} >= {creation_version}, <= {update_version}\n")
            else:
                file.write(f"{package}\n")
        print(f"New requirements file created at {output_path}")


# Step 1: Read the package names from requirements.txt
packages = read_requirements(requirements_path)

# Step 2: Write the new requirements.txt with version constraints
write_new_requirements(
    packages, repo_creation_date, last_update_date, new_requirements_path
)
