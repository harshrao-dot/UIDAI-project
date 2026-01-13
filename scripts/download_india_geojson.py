import urllib.request
import ssl

# Create SSL context to ignore certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson',
    'https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States',
    'https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson',
    'https://raw.githubusercontent.com/HindustanTimesLabs/shapefiles/master/india/india_states.geojson'
]

for u in urls:
    try:
        print('Trying', u)
        # Use the SSL context
        resp = urllib.request.urlopen(u, context=ctx, timeout=15)
        data = resp.read()
        if data and len(data) > 100:
            with open('processed_data/india_states.geojson', 'wb') as f:
                f.write(data)
            print('Saved from', u)
            break
    except Exception as e:
        print(f'Failed {u}: {e}')
else:
    print('No candidate worked')
