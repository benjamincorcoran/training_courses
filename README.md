# Data Science Seminars 

This repository contains all the Data Science presentations that have been created by me. 

## Contents

### Programming 

#### Python 

- [Introduction to Python - Part 1](<./Introduction to Python/Introduction to Python Part 1.ipynb>)
    - Introduction to Python and Python Objects
    - Introduction to the Pandas Library
    - Selecting, filtering and creating new variables in Pandas
- [Introduction to Python - Part 2](<./Introduction to Python/Introduction to Python Part 2.ipynb>)
    - Descriptive Statistics in Pandas
    - Updating values in Pandas
    - Aggregation in Pandas
    - Cross-tabulation in Pandas
    - Merging in Pandas
- [Introduction to Web Scraping](<./Introduction to Web Scraping/Introduction to Web Scraping.ipynb>)
    - HTML and CSS 
    - Using Pandas `read_html()`
    - Using requests to get HTML and JSON data
    - Using BeauitifulSoup to parse HTML data
    - Using Selenium to interact with live websites
- [Introduction to Data Linking](<./Introduction to Data Linking/Introduction to Data Linking.ipynb>)
    - M and U Values
    - String Comparison
    - Expectation Maximisation


### Data Engineering 

- [Introduction to Data Engineering](<./Introduction to Data Engineering/Introduction to Data Engineering.ipynb>)

### Data Visualisation 

- [Introduction to Data Visualisation](<./Introduction to Data Visualisation/Introduction to Data Visualisation.ipynb>)
- [Introduction to Tableau](<./Introduction to Tableau/Introduction to Tableau.ipynb>)
- [Introduction to Plotly](<./Introduction to Plotly/Introduction to Plotly.ipynb>)
- [Introduction to Dash](<./Introduction to Dash/Introduction to Dash.ipynb>)

### Ways of Working 

- [Introduction to Git](<./Introduction to Git/Introduction to Git.ipynb>)
- [Introduction to Report Templating](<./Introduction to Plotly/Introduction to Report Templating.ipynb>)

## How to use a presentation 

All presentations are written as jupyter notebooks. They have also been converted into stand alone slide sets using reveal.js. Opening the slide set will start a presentation. Press `s` to open up speaker mode and get access to the speaker notes.  

## How to build presentations 

All the presentations in this repository can be built to be stand alone `.slides.html` files. Use 

```cmd
python build_presentations.py
```

It is possible to use the argument `--find` to specify a specific presentation to build based on a keyword present in the presentation's filepath. This is **case-sensitive**. For example, to build only the Introduction to Git presentation the following code should be used. 

```cmd
python build_presentations.py --find Git
```

All presentation notebooks present should now be built into standalone `.slides.html` files. 

## How to write presentations 

Presentations can be written like any jupyter notebook, using markdown cells to include text. Make sure to use the property inspector tool (cogs on the right hand side in JupyterLab) to set the slide type.
