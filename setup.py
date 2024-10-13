import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

  setuptools.setup(
  name='spp_core',
  version='0.0.1',
  author='F_i Ye',
  author_em_il='feiye@vims.edu',
  description='Core scripts from Python tools for pre/post-processing SCHISM models',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',
  project_urls = {
    "Issues": ""
  },
  license='MIT',
  packages=[
    'spp_core',
    'spp_core.Grid',
    'spp_core.Download',
    'spp_core.Utilities',
  ],
  package_data={'spp_core': ['Datafiles/*']},
  install_requires=[
    'numpy',
    'pandas',
    'xarray',
    'pyshp>=2.0.0',
    'geopandas'
  ],
)
