from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_unique_crime_types():
    conn = sqlite3.connect('crimes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT "Primary Type" FROM filtered_crimes')
    crime_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sorted(crime_types)

def convert_two_digit_year(year):
    """Convert four-digit year to two-digit year"""
    if len(year) == 4:
        return year[2:]
    return year

def get_crime_data(crime_type=None, year=None):
    conn = sqlite3.connect('crimes.db')
    cursor = conn.cursor()
    query = """
    SELECT
        Latitude,
        Longitude,
        "Primary Type",
        Date,
        Block,
        Description,
        Arrest
    FROM filtered_crimes
    WHERE Latitude IS NOT NULL
    AND Longitude IS NOT NULL
    """
    params = []
    
    if crime_type:
        query += ' AND "Primary Type" = ?'
        params.append(crime_type)
    
    if year:
        two_digit_year = convert_two_digit_year(year)
        query += """ AND substr(Date, -14, 2) = ? """
        params.append(two_digit_year)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    result = [{
        "lat": row[0],
        "lng": row[1],
        "type": row[2],
        "date": row[3],
        "block": row[4],
        "description": row[5],
        "arrest": "Yes" if row[6] else "No"
    } for row in rows if row[0] and row[1]]
    
    conn.close()
    return result

@app.route('/api/getTrendData')
def get_trend_data():
    crime_types = request.args.getlist('types[]')
    conn = sqlite3.connect('crimes.db')
    cursor = conn.cursor()
    
    trend_data = {
        "crimeTypes": []
    }
    
    for crime_type in crime_types:
        query = """
        SELECT 
            COUNT(CASE WHEN Arrest = 1 THEN 1 END) as arrests,
            COUNT(CASE WHEN Arrest = 0 THEN 1 END) as no_arrests
        FROM filtered_crimes
        WHERE "Primary Type" = ?
        """
        
        cursor.execute(query, (crime_type,))
        results = cursor.fetchone()
        
        trend_data["crimeTypes"].append({
            "type": crime_type,
            "arrestCount": results[0],
            "noArrestCount": results[1]
        })
    
    conn.close()
    return jsonify(trend_data)

@app.route('/')
def index():
    years = ['2020', '2021', '2022', '2023', '2024']
    crime_types = get_unique_crime_types()
    return render_template('index.html', crime_types=crime_types, years=years)

@app.route('/trends')
def trends():
    print("Trends route accessed!")  # Debug print
    years = ['2020', '2021', '2022', '2023', '2024']
    crime_types = get_unique_crime_types()
    return render_template('trends.html', crime_types=crime_types, years=years)

@app.route('/api/getCrimeData')
def crime_data():
    crime_type = request.args.get('type')
    year = request.args.get('year')
    crimes = get_crime_data(crime_type, year)
    return jsonify(crimes)

@app.route('/api/getTrendData')
def get_trend_data_api():
    crime_types = request.args.getlist('types[]')
    if not crime_types:
        return jsonify({"error": "No crime types specified"}), 400
    
    trend_data = get_trend_data(crime_types)
    return jsonify(trend_data)

if __name__ == '__main__':
    app.run(debug=True)