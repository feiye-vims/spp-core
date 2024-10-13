import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

  setuptools.setup(
  name='spp-core',
  version='0.0.1',
  author='Fei Ye',
  author_email='feiye@vims.edu',
  description='Core scripts from Python tools for pre/post-processing SCHISM models',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',
  project_urls = {
    "Issues": ""
  },
  license='MIT',
  packages=[
    'spp-core',
    'spp-core.Grid',
    'spp-core.Download',
    'spp-core.Utilities',
  ],
  package_data={'spp-core': ['Datafiles/*']},
  install_requires=[
    'numpy',
    'pandas',
    'xarray',
    'pyshp>=2.0.0',
    'geopandas'
  ],
)
