create venv in folder


-install packages:

keras
tf-nightly-cpu
flask
Flask-Json


gemmer

@app.route('/api/modelOne', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        print("hi")
        data = request.get_json()
        key_list = [k for k, v in data[0].items()]
        print(key_list)
        df = pd.DataFrame(data)
        print(len(df))
        #df.to_csv(r'/Users/niklashjort/Desktop/Projects/DeepLearnApi/DeepLearnApi/training/data/apple_data.csv', index=False, header=True)
        return jsonify(data)
    else:
            error = 'Invalid username/password'
            return print(error)
    # the code below is executed if the request method
    # was GET or the credentials were invalid