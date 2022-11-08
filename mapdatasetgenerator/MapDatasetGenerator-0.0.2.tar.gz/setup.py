# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mapdataset', 'mapdataset.lib']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'dill>=0.3.5.1,<0.4.0.0',
 'mbutil>=0.3.0,<0.4.0',
 'torch>=1.12.1,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'mapdatasetgenerator',
    'version': '0.0.2',
    'description': 'Map dataset generator for learning map representations and generation',
    'long_description': '# MapDatasetGenerator\nGenerate and load dataset of road network maps.\n\n<!-- # Quick start\n* Use pip to install necessary python packages `pip install -r requirements.txt`.\n* Run `python run.py` script. It will store .dill files in the data/output/ directory. \n* These dill files can be read using the `ImgGroupReader` object in `read.py`. Run `read.py` to run a small test for the same.  \n -->\n\n# Installation from pip\n\n```\npip install mapdatasetgenerator\n```\n\n# Creating patches\n```\n# Run this script to generate data in /output directory.\nimport logging\nimport sys\n\nroot = logging.getLogger()\nroot.setLevel(logging.INFO)\n\nhandler = logging.StreamHandler(sys.stdout)\nhandler.setLevel(logging.INFO)\nformatter = logging.Formatter(\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\')\nhandler.setFormatter(formatter)\nroot.addHandler(handler)\n\nfrom mapdataset import ImageGroupReader, single_layer_converter, MapsDataset, MapReader\n\n\nsfMap = MapReader(\'./data/input/sf_layered.txt\', "SF_Layered")\nmapsDataset = MapsDataset(\n    patch_size=(32, 32), \n    stride=10, \n    sample_group_size=1280, \n    converter=single_layer_converter,\n    outputDir="./data/output"\n    ) \n    \nmapsDataset.generate_patches(sfMap) #This will generate dill files which contain the saved sample lists.\n\n```\n\n# Reading patches\n\n```\n# Script to read dill data objects as numpy arrays.\nfrom PIL import Image\nimport os\nimport sys\nimport logging\n\nroot = logging.getLogger()\nroot.setLevel(logging.INFO)\n\nhandler = logging.StreamHandler(sys.stdout)\nhandler.setLevel(logging.INFO)\nformatter = logging.Formatter(\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\')\nhandler.setFormatter(formatter)\nroot.addHandler(handler)\n\n\nfrom mapdataset import ImageGroupReader, single_layer_converter, MapsDataset, MapReader, ImageUtils\n\ndillFolder = "./data/output/SF_Layered/32x32/group-1280-stride-10"\n\nmapsDataset = MapsDataset(\n    patch_size=(32, 32), \n    stride=10, \n    sample_group_size=1280, \n    converter=single_layer_converter,\n    outputDir="./data/output"\n    ) \n\nmapsDataset.loadPatches("./data/output/SF_Layered/32x32/group-1280-stride-10")\npatchNo = randint(0, len(mapsDataset))\nlogging.info(f"reading patch {patchNo}")\npatch = mapsDataset[patchNo]\n\n\nim = ImageUtils.TorchNpPatchToPILImgGray(patch)\npath = os.path.join(dillFolder, f"{patchNo}.png")\nim.save(path)\n\n```\n\n# Using for training\n\n1. Create patches if you already do not have them\n2. Create a MapsDataset object and load patches. Now you can use the dataset object as a regular Pytorch dataset or use it with a Dataloader.\n',
    'author': 'Ishaan',
    'author_email': 'iparanja@ucsc.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AugmentedDesignLab/MapDatasetGenerator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
