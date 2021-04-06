from flask import Blueprint, request, jsonify, render_template
import pickle

API_EXIST = True
loaded_model = pickle.load(open('API/house_pricing_model', 'rb'))

def price_rtf(x):
    mx = 9100000
    mn = 1750000
    return x*(mx+mn)-mn
def area_tf(x):
    mx = 10360
    mn = 1650
    return (x+mn)/(mx+mn)
def bathrooms_tf(x):
    mx = 3
    mn = 1
    return (x+mn)/(mx+mn)
def stories_tf(x):
    mx = 4
    mn = 1
    return (x+mn)/(mx+mn)
def airconditioning_tf(x):
    mx = 1
    mn = 0
    return (x+mn)/(mx+mn)
def parking_tf(x):
    mx = 3
    mn = 0
    return (x+mn)/(mx+mn)
def prefarea_tf(x):
    mx = 1
    mn = 0
    return (x+mn)/(mx+mn)

api = Blueprint('api', __name__,
                        template_folder='templates')

@api.route('/api/predict', methods=['POST', 'GET'])
def predict():
    if request.method=='POST':
        area = area_tf(float(request.form['area']))
        bathrooms = bathrooms_tf(int(request.form['bathrooms']))
        stories = stories_tf(int(request.form['stories']))
        airconditioning = airconditioning_tf(int(request.form['airconditioning']))
        parking = parking_tf(int(request.form['parking']))
        prefarea = prefarea_tf(int(request.form['prefarea']))

        data = [1, area, bathrooms, stories, airconditioning, parking, prefarea]
        print(data)
        predicted_price = loaded_model.predict([data])

        # edit your code
        return render_template("cal-result.html", price=round(price_rtf(predicted_price[0])))

    if request.method=='GET':
        return "this is house prediction api"

    