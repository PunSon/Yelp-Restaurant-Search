from flask import Flask, render_template, request
from yelpapi import YelpAPI

app = Flask(__name__)
api_key = 'MUxXiF4fqu7TVYOLicZL1ntIozfY2msDtf5lEEUNo3FxWIALOr3c0du2N9tfv-w5qEwS0SDNDgLHk-HX3VA-q8YGapZy2-JSYKXbCnAe1mzEIW4USVWAcXC0nAJpZXYx'
yelp_api = YelpAPI(api_key)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        term = request.form['term']
        limit = int(request.form['limit'])

        # Call Yelp API with user inputs
        params = {
            'term': term,
            'sort_by': 'rating',
            'attributes': 'liked_by_vegetarians',
            'limit': limit
        }
        response = yelp_api.search_query(location=location, **params)
        businesses = response.get('businesses',[])
        for business in businesses:
            latitude = business.get('coordinates',{}).get('latitude')
            longitude = business.get('coordinates',{}).get('longitude')
            business['google_maps_link'] = f'https://www.google.com/maps?q={latitude},{longitude}'

        return render_template('results.html', businesses=businesses)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
