#################################################
# Libraries
#################################################

import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect
    )

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################

# Create connection to sqlite database
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
otu = Base.classes.otu
samples = Base.classes.samples
metadata = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Home Route
#################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

#################################################
# Sample Names Route
#################################################

@app.route('/names')
def get_names():
# Returns a list of sample names

    # Create an empty list to store names
    name_list = []
    
    # Query samples_metadata table for SAMPLEID
    results = session.query(metadata.SAMPLEID).all()
    
    # Loop through the results
    for name in results:

        # Append each name to the list
        name_list.append("BB_" + str(name[0]))
    
    # Return list of names
    return (jsonify(name_list))

#################################################
# OTU Description Route
#################################################

@app.route('/otu')
def get_otu_description():
    # Return a list of OTU descriptions
    
    # Create an empty list to store descriptions
    otu_description_list = []

    # Query otu table for description
    results = session.query(otu.lowest_taxonomic_unit_found).all()

    # Loop through the results
    for item in results:

        # Append each description to the list
        otu_description_list.append(item[0])
        
    # Return list of descriptions
    return (jsonify(otu_description_list))

#################################################
# Metadata Route
#################################################

@app.route('/metadata/<sample>')
def get_metadata(sample):
    # Returns a JSON dictionary containing age, bbtype, ethnicity, gender, location and sample id
    # Sample must in the following format: `BB_940`
    
    # Get just the number from the sample
    sample_num = sample[3:]

    # Create an empty dictionary to store metadata
    metadata_dict = {}

    # Query samples_metadata table where the sample id equals the sample num
    results = session.query(metadata.AGE, metadata.BBTYPE, metadata.ETHNICITY, metadata.GENDER, metadata.LOCATION, metadata.SAMPLEID)\
                .filter(metadata.SAMPLEID == sample_num).all()

    # Add items to dictionary
    metadata_dict["AGE"] = results[0][0]
    metadata_dict["BBTYPE"] = results[0][1]
    metadata_dict["ETHNICITY"] = results[0][2]
    metadata_dict["GENDER"] = results[0][3]
    metadata_dict["LOCATION"] = results[0][4]
    metadata_dict["SAMPLEID"] = sample_num

    # Return JSON dictionary of metadata items
    return (jsonify(metadata_dict))

#################################################
# Weekly Washing Route
#################################################

@app.route('/wfreq/<sample>')
def get_weekly(sample):
    # Returns the weekly washing frequency as a number
    # Sample must in the following format: `BB_940`

    # Get just the number from the sample
    sample_num = sample[3:]

    # Query samples_metadata table where the sample id equals the sample num
    results = session.query(metadata.WFREQ).filter(metadata.SAMPLEID == sample_num).all()

    # Assign the washing frequency based on the results
    wfreq = results[0][0]
    
    # Return the washing frequency as an integer
    return (wfreq)

#################################################
# Sample Values Route
#################################################

@app.route('/samples/<sample>')
def get_samples(sample):
    # Returns the OTU IDs and sample values for a given sample
    
    # Create a connection to the database
    conn = engine.connect()

    # Query samples table and put results in dataframe
    data = pd.read_sql(f"SELECT otu_id, {sample} FROM samples", conn)

    # Sort dataframe by sample value in descending order
    sorted_data = data.sort_values([sample], ascending = False)

    # Create a list of the sorted OTU IDs and a list of sample values
    otu_list = sorted_data['otu_id'].values.tolist()
    sample_list = sorted_data[sample].values.tolist()

    # Convert lists in a dictionary
    sample_dict = {'otu_ids' : otu_list, 'sample_values' : sample_list}

    # Return a list of dictionaries containing sorted lists for OTU IDs and Sample Values
    return (jsonify(sample_dict))

#################################################

if __name__ == "__main__":
    app.run(debug=True)