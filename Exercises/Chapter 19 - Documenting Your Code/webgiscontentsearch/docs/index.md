# Web GIS Content Search

Tools to assist in searching for and filtering your Portal for ArcGIS or ArcGIS Online organizations's web GIS!

:::{note}
This Python Package is a lot of fun to use.

:::

## Getting Started

To get started, install this package into your Python environment.

### Creating an Environment

You may wish to use ArcGIS Pro's Conda environment as a template. Please note, we never recommend modifying the default ArcGIS Pro Conda environment, always create a new one instead.

``` shell
conda create --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3" --prefix <path to your new environment>

conda activate <path to your new environment>
```

### Installation

In a terminal, activate your Python environment, and run the following

``` python
pip install -e <path to webgiscontentsearch folder>
```

### Import the Package

``` python
import webgiscontentsearch