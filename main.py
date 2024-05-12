from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Function to fetch COVID-19 data from the API
def fetch_covid_data(api_key):
    url = f"https://api.covidactnow.org/v2/states.json?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to extract necessary data for plotting
def extract_data_for_plotting(data):
    states = []
    cases = []
    deaths = []
    
    for state_data in data:
        states.append(state_data['state'])
        cases.append(state_data['actuals']['cases'])
        deaths.append(state_data['actuals']['deaths'])
    
    return states, cases, deaths

# Route for the dashboard
@app.route('/')
def dashboard():
    api_key = "54bc1b70bc5e4188bf29e23d8cf1128b"  # Replace this with your API key
    data = fetch_covid_data(api_key)
    
    tabular_data = []
    for i in data:
        state = i['state']
        cases = i['actuals']['cases']
        new_cases = i['actuals']['newCases']
        deaths = i['actuals']['deaths']
        vaccination_completed=i['actuals']['vaccinationsCompleted']
        caseDensity=i['metrics']['caseDensity']
        infectionRate=i['metrics']['infectionRate']
        tabular_data.append({'state': state, 'cases': cases, 'deaths': deaths,
                           'new_cases':new_cases,'vaccination_completed':vaccination_completed, 'caseDensity':caseDensity, 'infectionRate':infectionRate})
        states, cases, deaths = extract_data_for_plotting(data)
    states, cases, deaths = extract_data_for_plotting(data)

    # Create plots
    case_plot = go.Bar(x=states, y=cases, name='Cases',marker=dict(color='orange'))
    death_plot = go.Bar(x=states, y=deaths, name='Deaths',marker=dict(color="red"))

    # Layout
    layout = go.Layout(title='COVID-19 Cases and Deaths by State',
                       xaxis=dict(title='States'),
                       yaxis=dict(title='Count'))

    # Plot configuration
    case_fig = go.Figure(data=[case_plot], layout=layout)
    death_fig = go.Figure(data=[death_plot], layout=layout)

    case_graph = case_fig.to_html(full_html=False)
    death_graph = death_fig.to_html(full_html=False)

    return render_template('dashboard.html', case_graph=case_graph, death_graph=death_graph,tabular_data=tabular_data
                           )

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
