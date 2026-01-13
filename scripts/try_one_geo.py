import urllib.request
u='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/geojson/states/India.geojson'
print('Trying', u)
try:
    resp=urllib.request.urlopen(u, timeout=15)
    data=resp.read()
    if data and len(data)>100:
        with open('processed_data/india_states.geojson','wb') as f:
            f.write(data)
        print('Saved from', u)
    else:
        print('No data')
except Exception as e:
    print('Failed:', e)
