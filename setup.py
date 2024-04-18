from setuptools import find_packages,setup

#with open("README.md", "r", encoding="utf-8") as f:
    #long_description = f.read()
    
def get_libraries_from_requirements_file(file_path):
    with open(file_path, 'r') as rf:
        requirements_list = []
        for lib in rf:
            requirements_list.append(lib.strip())
    return requirements_list

__version__ = "0.0.0"

REPO_NAME = "Sensor-Abnormality-Classification"
AUTHOR_USER_NAME = "Dharmateja033"
SRC_REPO = "Sensor-Abnormality-Classification"
AUTHOR_EMAIL = "dharmateja.2660@gmail.com"

setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Classification project on APS system(IOT) of heavy_load vehicles",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "bugTracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    packages=find_packages(),
)