import os
import json

import gspread
import geocoder
from slugify import slugify
from flask import Flask, render_template, jsonify
from oauth2client.service_account import ServiceAccountCredentials


app = Flask('sample')

app.config['JSON_AS_ASCII'] = False
app.config['SHEET_URL'] = os.environ.get('SHEET_URL')
app.config['SHEETS_API_KEY'] = json.loads(os.environ.get('SHEETS_API_KEY'))
app.config['GEOCODING_API_KEY'] = os.environ.get('GEOCODING_API_KEY')


data = {
    'type': 'FeatureCollection',
    'features': [],
}


@app.before_first_request
def before_first_request():
    for row in get_sheet(app.config['SHEETS_API_KEY'], app.config['SHEET_URL']):
        location = row['Location'] + ', Czech Republic'
        g = geocoder.google(location, key=app.config['GEOCODING_API_KEY'])
        coords = g.latlng

        properties = dict((slugify(item[0]), item[1]) for item in row.items())
        data['features'].append({
            'type': 'Feature',
            'properties': properties,
            'geometry': {
                'type': 'Point',
                'coordinates': [coords[1], coords[0]]
            }
        })


@app.route('/')
def index():
    return render_template('index.html')


# See https://github.com/pyvec/elsa/issues/58 to see why this route is crippled
@app.route('/api.json')
def api():
    response = jsonify(data)
    # response.mimetype = 'application/geo+json'
    return response


def get_sheet(api_key, sheet_url):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(api_key, scope)

    sheets = gspread.authorize(credentials)
    worksheet = sheets.open_by_url(sheet_url).get_worksheet(0)
    cells = worksheet.get_all_values()

    header = cells[0]
    rows = cells[1:]

    return (dict(zip(header, row)) for row in rows)
