# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unhidden']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.0,<2.0.0', 'requests>=2.28.1,<3.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['unhidden = unhidden.main:app']}

setup_kwargs = {
    'name': 'unhidden',
    'version': '0.3.0',
    'description': '',
    'long_description': 'This CLI app is made for saved palettes analysis. There are various commands to get weekly/monthly/daily saved palette results and compare them. To get the full potential of the app, please read this guide.\n\nNotes\n1. Throughout this note, commands to be run will be written inside double quotes. You should run the commands without the double quotes.\n2. The API key will be denoted as "XYXYXY". You should always replace it with your actual API key for Unhidden Beauty.\n3. Every command starts with "unhidden", as it\'s the name of the app.\n4. Before using the app for the first time, you need to download the API data to your local machine. To do that, simply run "unhidden api XYXYXY --update".\n4. Every time you want to do a new analysis (e.g., weekly metrics update), you need to first update your local data so that it stores the latest saved palettes as well. So, make a habbit to run "unhidden api XYXYXY --update" everytime you want to use the app. It will take only a couple of seconds.\n\n\nAll Commands\n\n1. api\napi command is for accessing general info about saved palettes API. Run "unhidden api XYXYXY" to simply run it and learn when you updated your local data last time.\n\n2. palette\npalette command is for analyzing saved palettes metrics for different time periods. You can give any starting and ending date of format "dd.mm.yy" and it will return the results. \n\nExample usages of "palette" command:\n> unhidden palette 5.10.22 12.10.22 (returns saved palette metrics for the given period including October 12th)\n> unhidden palette 2.6.22 now (returns metrics from February 2th up to now)\n> unhidden palette today (returns today\'s metrics)\n> unhidden palette yesterday (returns yesterday\'s metrics)\n> unhidden palette lastweek (returns metrics of last full week)\n\nAdd the argument "--compare" to compare the metrics to the previous time interval of same length. Examples:\n> unhidden palette 1.10.22 31.10.22 --compare (returns october\'s metrics and also compares it with september)\n> unhidden palette lastweek --compare (returns last full week\'s metrics and also compares it with previous week)\n\nAdd the argument "--count" to get the list of people that saved specific amount of palettes. Examples:\n> unhidden palette lastweek --count \'3\' (returns list of users who saved exactly 3 palettes last week. Make sure to include single quotes)\n> unhidden palette 1.1.21 31.1.21 --count \'>5\' (returns list of users who saved more than 5 palettes in January 2021)\n\n3. customer-wc\ncustomer-wc command is for getting the users of interest and also getting "Customer WC" sheets for engagement data of any week. Since this command modifies the Shopify report, make sure to download it from Shopify first. In order to download the report, log in to Shopify, go to "Analytics > Reports". Open the report named "\nFirst time and return customers _ excluding tests _KS_updated_250722". Set the dates you want to be analyzed and make sure data is displayed "Daily". Then click "Export" and export data as CSV file. It will be on your downloads folder. Now you\'re ready to run this command.\n\nExamples:\n> unhidden customer-wc 7.11.22 (returns users of interest for week commencing November 7th, and also updates Shopify report of same date range)\n\nAdd the argument "--month" to get monthly data instead of weekly. Examples:\n> unhidden customer-wc 1.11.22 --month\n\n4. palette-wc\npalette-wc command is for getting palettes information for the sheet "Saved palettes WC" for engagement sheets. Simplly run this command and then the data will be copied to your keyboard. Then paste it to the sheet.\n\nExample usage:\n> unhidden palette-wc 7.11.22\n\nAdd "--save" argument to save the data as csv file instead.\nExample:\n> unhidden palette-wc 7.11.22 --save\n',
    'author': 'Burak Akkaya',
    'author_email': 'akkaya.burak@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
