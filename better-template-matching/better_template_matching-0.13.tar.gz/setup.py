from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.13'
DESCRIPTION = "Fast template matching with multiprocessing, supports different sizes, and filters overlapping results"

# Setting up
setup(
    name="better_template_matching",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/better_template_matching',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_cv2_imshow_thread', 'a_pandas_ex_intersection_difference', 'a_pandas_ex_less_memory_more_speed', 'a_pandas_ex_plode_tool', 'flatten_everything', 'keyboard', 'kthread', 'numpy', 'opencv_python', 'pandas', 'regex', 'requests', 'scikit_image', 'skimage', 'ujson', 'windows_adb_screen_capture'],
    keywords=['template', 'matching', 'windows', 'bot', 'opencv'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules' ],
    install_requires=['a_cv2_imshow_thread', 'a_pandas_ex_intersection_difference', 'a_pandas_ex_less_memory_more_speed', 'a_pandas_ex_plode_tool', 'flatten_everything', 'keyboard', 'kthread', 'numpy', 'opencv_python', 'pandas', 'regex', 'requests', 'ujson', 'windows_adb_screen_capture'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*