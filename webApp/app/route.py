from flask import Flask, render_template, flash, request,jsonify
import pandas as pd
import json
import test as parent
#data csv file path

a="C:/Users/sajith/PycharmProjects/fyp/datacsv/UI/Final_FeatureSet.csv"
b="C:/Users/sajith/PycharmProjects/fyp/datacsv/UI/normalize.csv"
c='C:/Users/sajith/PycharmProjects/fyp/datacsv/UI/Final_result_withRank.csv'

def Recommend(uid):
    Movies = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\Movies.csv')
    results = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\result0.csv')
    results.columns = ['MID', 'rating', 'UID']
    # uid = 1108136359517809
    user = str(uid)
    foo = user[:-2]
    user  = foo+"x"
    uid = user.replace(" ", "")
    results.info()
    result = results.query('UID=="'+uid+'"').head(15)
    final = pd.merge( result, Movies, left_on='MID', right_on='movieId')
    movies = final["title"]

    dataFrame = pd.DataFrame(movies)
    # dataFrame1=dataFrame.sort_values(by=['Predicted Rank'])
    UserRank = dataFrame['title']
    movies = UserRank.tolist()
    print(movies)
    dataset = {}
    index = 0
    name1 = []
    No_of_post1 = []
    for i in movies:
        No_of_post1.append(str(i))

    dataset["id"] = No_of_post1

    return dataset


app = Flask(__name__)
@app.route('/')
def home():
    dataset=createDataInRanking()
    json_dump = json.dumps(dataset)
    return render_template('ranking.html',dataset=json_dump)

@app.route('/ranking', methods=['GET','POST'])
def addProduct():
    dataset=createDataInRanking()
    json_dump = json.dumps(dataset)
    return render_template('ranking.html',dataset=json_dump)

@app.route('/addProdcutValue', methods=['GET','POST'])
def addProdcutValue():
    print(request)
    print(request.form)
    fl = request.form['reco']
    strmovies = str(fl)
    strMovie = strmovies.replace("[", "")
    strid = strMovie.replace("]", "")
    print(strid)
    result = Recommend(float(strid))
    json_dump = json.dumps(result)
    return render_template('recommendation.html', dataset=json_dump)

@app.route('/expert', methods=['GET','POST'])
def getExpert():
    dataset1=get_users_Wice_Category('intermediate Users', 'Novice Users')
    dataset1["erro"] = False

    json_dump1 = json.dumps(dataset1)
    return render_template('expertUsers.html',dataset1=json_dump1)


@app.route('/novice', methods=['GET','POST'])
def getNovice():
    dataset1=get_users_Wice_Category('intermediate Users', 'Expert Users')
    dataset1["erro"] = False

    json_dump1 = json.dumps(dataset1)
    return render_template('NoviceUsers.html',dataset1=json_dump1)


@app.route('/intermediate', methods=['GET','POST'])
def getIntermediate():
    dataset1=get_users_Wice_Category('Novice Users', 'Expert Users')
    dataset1["erro"] = False

    json_dump1 = json.dumps(dataset1)
    return render_template('intermediate.html',dataset1=json_dump1)




@app.route('/search', methods=['GET','POST'])
def search():
    print(request)
    print(request.form)
    fl = request.form['search']
    completeDataset = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\IdAndMoviesv6.csv')
    match = parent.IsUserExists(fl)

    if match:
        result = completeDataset.query('id==' + str(fl)).head()
        uid = result['id'].values
        movies = result["movie_list"].values
        O_Predicted = result["O_Predicted"].values
        C_Predicted = result["C_Predicted"].values
        E_Predicted = result["E_Predicted"].values
        A_Predicted = result["A_Predicted"].values
        N_Predicted =result["N_Predicted"].values
        strmovies = str(movies)
        strMovie = strmovies.replace("[","")
        strMovi = strMovie.replace("]","")
        strMov = strMovi.replace('"',"")
        strMo = strMov.replace('/',"")
        strM = strMo.replace("'","")



        dataset={}

        dataset["uid"] = str(uid)
        dataset["movies"]=str(strM)
        dataset["O_Predicted"] = str(O_Predicted)
        dataset["C_Predicted"] = str(C_Predicted)
        dataset["E_Predicted"] = str(E_Predicted)
        dataset["A_Predicted"] = str(A_Predicted)
        dataset["N_Predicted"] = str(N_Predicted)

        json_dump1 = json.dumps(dataset)
        print(json_dump1)

        return render_template('addProduct.html', datset=json_dump1)
    else:
        dataset = createDataInRanking()
        dataset["erro"] = True
        json_dump = json.dumps(dataset)

        return render_template('ranking.html',dataset=json_dump)




@app.route('/test', methods=['GET', 'POST'])
def test():
    # selectedProduct = request.get_json()
    return {
        "username" : "milanda",
        "telephoneNo" : "0715864650",
        "age":"15",
        "height" :  "10",
        "weight" : "10"
    }

def createDataInRanking():
    data = pd.read_csv(r'C:\Users\HP ITFAC\Desktop\FYP\Datasets\inputs\IdAndMoviesv6.csv')
    dataFrame=pd.DataFrame(data)
    # dataFrame1=dataFrame.sort_values(by=['Predicted Rank'])
    UserRank=dataFrame.get('id')
    dataset = {}
    index = 0
    name1 = []
    No_of_post1 = []
    for i in UserRank:
        No_of_post1.append(str(i))

    dataset["id"] = No_of_post1
    return dataset

def get_users_Wice_Category(name1,name2):
    data1 = pd.read_csv(c)

    dataframe = pd.DataFrame(data1)

    data = dataframe.sort_values(by=['Predicted_MLR'], ascending=False)

    data2 = data[data.User_category != name1]

    data3 = data2[data2.User_category != name2]

    User_type_name = 'Expert Users'
    name = data3.get('Username')
    Score = data3.get('Predicted_MLR')
    type = data3.get('User_category')
    dataset1 = {}
    name1 = []
    Score1 = []
    for i in name:
        name1.append(i)
    for x in Score:
        Score1.append(str(format(x,'.2f')))

    dataset1["name"] = name1
    dataset1["post"] = Score1
    return dataset1

if __name__ == '__main__':
    app.run(debug=True)
