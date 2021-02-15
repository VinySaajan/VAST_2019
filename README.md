# VisAn2019_2

VisAnProject 2019
from Victor, Kinger
working on Mini Challenge 2

![alt text](https://gitlab.rhrk.uni-kl.de/visanproject2019/visan2019_2/raw/init_version/data/Tool_Screenshots/Visual_Analysis_Tab.png "Visual Analysis")
![alt text](https://gitlab.rhrk.uni-kl.de/visanproject2019/visan2019_2/raw/init_version/data/Tool_Screenshots/Data_Analysis_Tab.png "Data Analysis")

Prerequistes to run the project:
1. Anaconda Distribution
2. Bokeh server
3. Geopandas (Use "conda install --channel conda-forge geopandas".)
How to run:
1. Download the repository and extract the contents in your system.
2. From Anaconda Prompt, go to the extracted directory.
3. Run bokeh server: bokeh serve --show visan2019_2

Note: We have noticed an issue with geopandas installed using pip package installer.
Therefore in case of error with GDAL, it is recommended to uninstall existing gdal and geopandas
and reinstall from the conda channel.

