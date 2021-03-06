from setuptools import setup, find_packages

setup(
      name='GraphEditor',
      version='0.0.1',
      description='Tool to work with graphs',
      author='Eldar Paplauski',
      author_email='eldarpoplauski111@gmail.com',
      packages=find_packages('src', exclude=['GraphEditor']),  # same as name
      install_requires=['pygame'],  # external packages as dependencies
)