from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['fbprophet','dask[complete]']

setup(
  name='prophet_gcp',
  version='0.1',
  author = 'Matias Aravena',
  author_email = 'matias@spikelab.xyz',
  install_requires=REQUIRED_PACKAGES,
  packages=find_packages(),
  include_package_data=True,
  description='Running prophet for products')