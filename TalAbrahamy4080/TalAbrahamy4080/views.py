"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from TalAbrahamy4080 import app
from TalAbrahamy4080.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from TalAbrahamy4080.Models.QueryFormStructure import QueryFormStructure 
from TalAbrahamy4080.Models.QueryFormStructure import LoginFormStructure 
from TalAbrahamy4080.Models.QueryFormStructure import UserRegistrationFormStructure
from TalAbrahamy4080.Models.QueryFormStructure import GasStationFormStructure
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Tal Abrahamy contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About the Project',
        year=datetime.now().year,
        
    )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )



@app.route('/DataModel')
def DataModel():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou gas stasion',
        year=datetime.now().year,
        message=""
    )
@app.route('/DataModel')
def DataModel1():
    """Renders the contact page."""
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou gas stasion',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer who have most gas stasion in israel'
        )
@app.route('/DataSet1')
def DataSet1():
    df = pd.read_excel(path.join(path.dirname(__file__), 'static/Data/gass.xlsx'))
    raw_data_table_head = df.head().to_html(classes='table table-hover')
    df = df.drop(index=0)
    df = df.drop(index=1)
    df = df.drop(index=2)
    df = df.drop(index=3)
    df = df.drop(index=4)

    raw_data_table = df.to_html(classes='table table-hover')

    return render_template(
        'DataSet1.html',
        raw_data_table=raw_data_table,
        raw_data_table_head=raw_data_table_head,
        title='Gas Station',
        year=datetime.now().year,
        message='Links to the data',

    )
@app.route('/DataSet2')
def DataSet2():
    df = pd.read_excel(path.join(path.dirname(__file__), 'static/Data/gass.xlsx'))
    raw_data_table_head = df.head().to_html(classes='table table-hover')
    df = df.drop(index=0)
    df = df.drop(index=1)
    df = df.drop(index=2)
    df = df.drop(index=3)
    df = df.drop(index=4)

    raw_data_table = df.to_html(classes='table table-hover')

    return render_template(
        'DataSet2.html',
        raw_data_table=raw_data_table,
        raw_data_table_head=raw_data_table_head,
        title='Dataset',
        year=datetime.now().year,
        message='Links to the data',
    )

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = GasStationFormStructure(request.form)
    df_gass= pd.read_excel(path.join(path.dirname(__file__), "static\\Data\\gass.xlsx"))
    chart1=""
    chart2=""
    
    #Set the list of states from the data set of all US states
    cities_choices = df_gass['city'].astype(str).to_list()
    cities_choices = list(dict.fromkeys(cities_choices))
    cities_choices = sorted(cities_choices)
    cities_choices = list(zip(cities_choices, cities_choices)) 
    form.City.choices = cities_choices

    #plot 
    if (request.method == 'POST' ):
        try:
            df_g = df_gass.drop(['station_number', 'station_name', 'address', 'authorty', 'telephone', 'fax', 'X', 'Y'], 1)
            companies = form.GasStations.data
            city = form.City.data
            df_g = df_g.loc[df_g["company"].isin(companies)]
            df_g = df_g.loc[df_g["city"] == city]
            df_g = df_g.groupby('company').size()

            fig1 = plt.figure()
            ax1 = fig1.add_subplot(111)
 
            df_g.plot(ax=ax1, kind='bar', rot=0, width=0.3, ) 
            plt.title('Gas stations in %s' % city)
            plt.style.use('ggplot')
            chart1 = plot_to_img(fig1)
        except IndexError:
            chart = 'https://freeiconshop.com/wp-content/uploads/edd/error-flat.png'

     
    return render_template('query.html', 
            form = form, 
            chart1=chart1,
            chart2=chart2,
            title='User Data Query',
            year=datetime.now().year,
            message='Please enter the parameters you choose, to analyze the database'
        )

#פעולה שמעבירה את הגרף לתמונה
def plot_to_img(fig):
    pngImage= io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64, "
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String



