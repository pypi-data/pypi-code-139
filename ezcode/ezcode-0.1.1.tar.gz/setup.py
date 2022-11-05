import json
from pathlib import Path
from setuptools import setup, find_packages


#     python -c "\
# import json, pathlib, requests;\
# base_dir = pathlib.Path('${BASE_DIRECTORY}');\
# payload = {'text': (base_dir/'${file_path}').read_text(encoding='utf-8'), 'mode': 'markdown'};\
# html_str = requests.post('https://api.github.com/markdown', data=json.dumps(payload), headers={'Accept':'application/vnd.github+jso'}).text;\
# open((base_dir/'html/${file_name}.html'), 'w').write(html_str);\
# "
#     python -m "http.server" --directory "${BASE_DIRECTORY}/html" "9999" &
#     open "http://localhost:9999/${file_name}.html"
# }

def build_long_description():
    long_description=""
    docs = Path(__file__).parent / "docs"
    for md in docs.glob("*.md"):
        with open(md, mode="r", encoding="utf-8") as f:
            long_description += f.read()
    return long_description


setup(
    name="ezcode",
    version="0.1.1",
    author="Zheng Gao",
    author_email="mail.zheng.gao@gmail.com",
    description="Easy Algorithm & Data Structure",
    url="https://github.com/zheng-gao/ez_code",
    project_urls={"Bug Tracker": "https://github.com/zheng-gao/ez_code/issues"},
    long_description=build_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                            # Information to filter the project on PyPi website
    python_requires=">=3.7",                      # Minimum version requirement of the package
    py_modules=["ezcode"],                        # Name of the python package
    package_dir={"": "src"},                      # Directory of the source code of the package
    packages=find_packages(where="src"),          # List of all python modules to be installed
    install_requires=[]                           # Install other dependencies if any
)
