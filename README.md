# cintel-06-custom

## Overview
add summary





## Create Project Virtual Environment

```shell

py -m venv .venv
.venv\Scripts\Activate
py -m pip install -r requirements.txt

```
3. Requirements
- Install packages 
```console
py -m pip install jupyterlab pandas matplotlib 
```
- Freeze your requirements to requirements.txt. 
```console
py -m pip install requests
py -m pip freeze > requirements.txt
```




## Git add and commit 

```shell
git add .
git commit -m "add .gitignore, readme, and requirements"
git push origin main
```


Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```shell
shiny run --reload --launch-browser dashboard/app.py
```

Open a browser to <http://127.0.0.1:8000/> and test the app.

## Run Locally - Subsequent Starts

Open a terminal (VS Code menu "View" / "Terminal") in the root project folder and run these commands.

```shell
.venv\Scripts\Activate
shiny run --reload --launch-browser dashboard/app.py
```

## After Making Changes, Export to Docs Folder

Export to docs folder and test GitHub Pages locally.

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```shell
.venv\Scripts\Activate
shiny static-assets remove
shinylive export dashboard docs
py -m http.server --directory docs --bind localhost 8008
```

Open a browser to <http://[::1]:8008/> and test the Pages app.

## Push Changes back to GitHub

Open a terminal (VS Code menu "Terminal" / "New Terminal") in the root project folder and run these commands.

```shell
git add .
git commit -m "Useful commit message"
git push -u origin main
```

Add new stuff for app:
use dowjones data from csv file 
add new chart from plotly: https://shiny.posit.co/py/components/outputs/plot-plotly/ 

add data grid: https://shiny.posit.co/py/api/express/express.render.DataGrid.html

delete out old chart\ keep other inputs