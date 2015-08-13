# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from myCPI.public.myCPIForms import BudgetShareForm

import json

blueprint = Blueprint('mycpi', __name__, static_folder="../static")


@blueprint.route("/mycpi", methods=["GET", "POST"])
def enterBudgetShare():
    form = BudgetShareForm(request.form)
    share_data = {'None': None}
    if request.method == "POST":
        if form.validate_on_submit():
            my_cpi = compute_cpi(form)
            share_data = plot_shares(form)
        else:
            my_cpi = None
    elif request.method == "GET":
        my_cpi = None
    return render_template("public/mycpi.html", form=form, my_cpi=my_cpi, share_data=share_data)

def get_budget_sum(form):
    budget_sum = (form.food_share.data+form.housing_share.data+form.apparel_share.data+form.edu_share.data+ \
        form.transportation_share.data+form.medical_share.data+form.recreation_share.data+form.other_share.data)    
    return budget_sum
    
def compute_cpi(form):
    component_indexes = {'food':246.245,\
        'housing':238.568,\
        'apparel': 124.954,\
        'edu': 137.425,\
        'transport': 208.012,\
        'medical_care': 446.271,\
        'recreation': 116.395,\
        'other': 415.022}
    
    ref_indexes = {'food':100,\
        'housing':100,\
        'apparel': 100,\
        'edu': 100,\
        'transport': 100,\
        'medical_care': 100,\
        'recreation': 100,\
        'other': 100}
    
    budget_sum = get_budget_sum(form)

    wgted_sum = (form.food_share.data/budget_sum) * (component_indexes['food']/ref_indexes['food']) + \
        (form.housing_share.data/budget_sum) * (component_indexes['housing']/ref_indexes['housing']) + \
        (form.apparel_share.data/budget_sum) * (component_indexes['apparel']/ref_indexes['apparel']) + \
        (form.edu_share.data/budget_sum) * (component_indexes['edu']/ref_indexes['edu']) + \
        (form.transportation_share.data/budget_sum) * (component_indexes['transport']/ref_indexes['transport']) + \
        (form.medical_share.data/budget_sum) * (component_indexes['medical_care']/ref_indexes['medical_care']) + \
        (form.recreation_share.data/budget_sum) * (component_indexes['recreation']/ref_indexes['recreation']) + \
        (form.other_share.data/budget_sum) * (component_indexes['other']/ref_indexes['other'])
    
    inflation = wgted_sum * 100
    return round(inflation,3)

def plot_shares(form, chartID='chartID', chart_type='pie', chart_height=500):
    budget_shares = {}
    budget_shares['title'] = {"text": "Visualization of budget shares"}
    budget_sum = float(get_budget_sum(form))
    budget_shares['series'] = json.dumps([{'name': "Budget Share",\
            'colorByPoint': True,\
            'data':[\
                {"name":"Food/Beverage", "y": round(100* form.food_share.data/budget_sum, 2)},\
                {"name":"Housing", "y": round(100*form.housing_share.data/budget_sum, 2)},\
                {"name":"Apparel", "y": round(100*form.apparel_share.data/budget_sum, 2)},\
                {"name":"Transportation", "y": round(100*form.transportation_share.data/budget_sum, 2)},\
                {"name":"Medical Care", "y": round(100*form.medical_share.data/budget_sum, 2)},\
                {"name":"Recreation", "y": round(100*form.recreation_share.data/budget_sum, 2)},\
                {"name":"Education", "y": round(100*form.edu_share.data/budget_sum, 2)},\
                {"name":"Other Services", "y": round(100* form.other_share.data/budget_sum, 2)}]}])
    budget_shares['page_type'] = "graph"
    budget_shares['chart'] = {"renderTo": chartID, "type": chart_type, "height": chart_height}

    return budget_shares
    
    
    
@blueprint.route("/about/")
def about():
    form = BudgetShareForm(request.form)
    return render_template("public/about.html", form=form)
