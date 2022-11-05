# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chrisjen', 'chrisjen.core', 'chrisjen.options']

package_data = \
{'': ['*']}

install_requires = \
['amos>=0.1.10,<0.2.0',
 'bobbie==0.1.1',
 'holden>=0.1.4,<0.2.0',
 'miller>=0.1.3,<0.2.0',
 'more_itertools>=9.0.0,<10.0.0',
 'nagata>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'chrisjen',
    'version': '0.1.2',
    'description': 'Python project workflows made easy',
    'long_description': '[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Documentation Status](https://readthedocs.org/projects/chrisjen/badge/?version=latest)](http://chrisjen.readthedocs.io/?badge=latest)\n\n<p align="center">\n<img src="https://media.giphy.com/media/EUdtBgPPKP3F7U6yBh/giphy.gif" />\n</p>\nNamed after the biggest badass in The Expanse, who knew how to get things done, chrisjen provides a solid foundation for designing internal project workflows with simple configuration files or scripting. chrisjen understands that you want to start designing your project and not spend countless hours designing the framework for your project. The primary goal of chrisjen is provide a simple, intuitive, powerful, extensible framework for constructing and implementing Python project workflows.\n\n## Intuitive \n\nchrisjen locates all of the essential parts of a python workflow under one roof, using consistent naming conventions and structures. You start with an "idea" (typically in the form of a(n) ini, toml, json, or python file, but you can use a python dict as well) and the rest of the project is created for you. If you want to manually change, iterate, or otherwise advance through the stages of your project, that is done entirely through the Project class using intuitive attributes like "outline", "workflow", and "summary". All the file management is performed through the consistent interface of the filing "clerk".\n\n<p align="center">\n<img src="https://media.giphy.com/media/69qwCZtG4arIgMuL6b/giphy.gif" width="250" height="250"/>\n</p>\n\nchrisjen strives to get out of your way and has an easy learning curve. Importantly, unlike most other workflow packages, chrisjen does not require learning a new scripting language. Even the initial idea is created with a file or dictionary that is easy to read. For example, this is part of an .ini. configuration file for a data science project used in chrisjen\'s unit tests:\n\n```\n[general]\nseed = 43\nconserve_memory = True\nparallelize = False\ngpu = False\n\n[files]\nsource_format = csv\ninterim_format = csv\nfinal_format = csv\nanalysis_format = csv\ntest_data = True\ntest_chunk = 500\nexport_results = True\n\n[wisconsin_cancer_project]\nwisconsin_cancer_workers = analyst, critic\nwisconsin_cancer_design = waterfall\n\n[analyst]\ndesign = contest\nanalyst_steps = scale, split, encode, sample, model\nfill_techniques = none\ncategorize_techniques = none\nscale_techniques = minmax, robust, normalize\nsplit_techniques = stratified_kfold, train_test\nencode_techniques = target, weight_of_evidence, one_hot, james_stein\nmix_techniques = none\ncleave_techniques = none\nsample_techniques = none\nreduce_techniques = none\nmodel_techniques = xgboost, logit, random_forest\nsearch_method = random\nmodel_type = classify\nlabel = target\ndefault_package = sklearn\n\n[critic]\ndesign = waterfall\ncritic_steps = shap, sklearn\ncritic_techniques = explain, predict, report\ndata_to_review = test\njoin_predictions = True\n```\n\nYou do not even half to select all of the options and specifications because chrisjen includes intellgent defaults. For example, if one of your project workers did not have a "design" setting, chrisjen would use the [waterfall design](https://www.lucidchart.com/blog/waterfall-project-management-methodology), the basic sequential design pattern in project management.\n\n## Flexible\n<p align="center">\n<img src="https://media.giphy.com/media/GnepwAlt5FG3ASUvRB/giphy.gif"/>\n</p>\nchrisjen emphasizes letting users design their projects from a range of options. These choices can be provided in another package or added on the fly.\n\n## Powerful \n\nTo faciliate workflow construction, chrisjen comes with several common workflow designs. While straightforward, these workflows are otherwise tedious and sometimes difficult to implement. chrisjen does all of that work for you. chrisjen is particularly powerful for comparative and conditional projectrs where you want to identify the best strategy or average results among multiple iterations. Among the structures provided out-of-the-box are:\n* Contest: evaluates and selects the best workflow among several based on one or more criteria\n* Waterfall: the most basic workflow in project management which follows a pre-planned rigid workflow structure\n* Kanban: a sequential workflow with isolated stages that produces deliverables for the following stage\n* Scrum: flexible workflow structure that requires greater user control and intervention\n* Pert: workflow that focuses on efficient use of parallel resources, including identifying the critical path\n* Agile: a dynamic workflow structure that changes direction based on one or more criteria\n* Lean: an iterative workflow that maximizes efficiency based on one or more criteria\n* Survey: averages multiple workflows based on one or more criteria\n\n## Extensible\n\nchrisjen\'s framework supports a wide range of coding styles. You can create complex multiple inheritance structures with mixins galore or simpler, compositional objects. Even though the data structures are necessarily object-oriented, all of the tools to modify them are also available as functions, for those who prefer a more functional approaching to programming.\n\n## Contributing \n\nThe project is also highly documented so that users and developers and make chrisjen work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.\n',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WithPrecedent/chrisjen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
