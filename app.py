from flask import *
import pymongo
from flask_sqlalchemy import SQLAlchemy
import json
#連線mongodb資料庫
client = pymongo.MongoClient("mongodb+srv://root:<password>@user.b7egcyy.mongodb.net/?retryWrites=true&w=majority")
modb = client.website


app = Flask( __name__)
app.secret_key="i know"

#連線mysql資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://be1119c102f23e:7d6dcb05@us-cdbr-east-06.cleardb.net/heroku_07d2de6f7393559"
mydb = SQLAlchemy(app)

class bb_products(mydb.Model):
    __tablename__= "bb_products"
    bb_id = mydb.Column(mydb.Integer, primary_key=True)
    bb_size= mydb.Column(mydb.Integer)
    bb_name = mydb.Column(mydb.String(30), unique=True, nullable=False)
    bb_price = mydb.Column(mydb.Integer)
    bb_img = mydb.Column(mydb.String(100))
    bb_link = mydb.Column(mydb.String(100))

    bb_prosucts_all_products = mydb.relationship("all_products", backref="bb_products") #外鍵的設定
    bb_prosucts_AddToCar = mydb.relationship("AddToCar", backref="bb_products") #外鍵的設定

    def __init__(self, bb_id, bb_size, bb_name, bb_price, bb_img, bb_link):
        self.bb_id = bb_id
        self.bb_size = bb_size 
        self.bb_name = bb_name
        self.bb_price = bb_price
        self.bb_img = bb_img
        self.bb_link = bb_link
    

        

class sc_products(mydb.Model):
    __tablename__= "sc_products"
    sc_id = mydb.Column(mydb.Integer, primary_key=True)
    sc_size= mydb.Column(mydb.Integer)
    sc_name = mydb.Column(mydb.String(30), unique=True, nullable=False)
    sc_price = mydb.Column(mydb.Integer)
    sc_img = mydb.Column(mydb.String(100))
    sc_link = mydb.Column(mydb.String(100))

    sc_prosucts_all_products = mydb.relationship("all_products", backref="sc_products") #外鍵的設定
    sc_prosucts_AddToCar = mydb.relationship("AddToCar", backref="sc_products") #外鍵的設定

    def __init__(self, sc_id, sc_size, sc_name, sc_price, sc_img, sc_link):
        self.sc_id = sc_id
        self.sc_size = sc_size
        self.sc_name = sc_name
        self.sc_price = sc_price
        self.sc_img = sc_img
        self.sc_link = sc_link


class vb_products(mydb.Model):
    __tablename__= "vb_products"
    vb_id = mydb.Column(mydb.Integer, primary_key=True)
    vb_size= mydb.Column(mydb.Integer)
    vb_name = mydb.Column(mydb.String(30), unique=True, nullable=False)
    vb_price = mydb.Column(mydb.Integer)
    vb_img = mydb.Column(mydb.String(100))
    vb_link = mydb.Column(mydb.String(100))

    vb_prosucts_all_products = mydb.relationship("all_products", backref="vb_products") #外鍵的設定
    vb_prosucts_AddToCar = mydb.relationship("AddToCar", backref="vb_products") #外鍵的設定

    def __init__(self, vb_id, vb_size, vb_name, vb_price, vb_img, vb_link):
        self.vb_id = vb_id
        self.vb_size = vb_size
        self.vb_name = vb_name
        self.vb_price = vb_price
        self.vb_img = vb_img
        self.vb_link = vb_link



class all_products(mydb.Model):
    __tablename__ = "all_commoditys"
    p_id = mydb.Column(mydb.Integer, primary_key=True)
    name = mydb.Column(mydb.String(30), unique=True, nullable=False)

    bb_id = mydb.Column(mydb.Integer, mydb.ForeignKey('bb_products.bb_id'), nullable=True) #外鍵的設定
    sc_id = mydb.Column(mydb.Integer, mydb.ForeignKey('sc_products.sc_id'), nullable=True) #外鍵的設定
    vb_id = mydb.Column(mydb.Integer, mydb.ForeignKey('vb_products.vb_id'), nullable=True) #外鍵的設定

    def __init__(self, p_id, name, bb_id, sc_id, vb_id):
        self.p_id = p_id
        self.name = name
        self.bb_id = bb_id
        self.sc_id = sc_id
        self.vb_id = vb_id


class AddToCar(mydb.Model):
    __tablename__ = "Car"
    c_id = mydb.Column(mydb.Integer, primary_key=True)
    u_name = mydb.Column(mydb.String(30))
    amount = mydb.Column(mydb.Integer)

    bb_id = mydb.Column(mydb.Integer, mydb.ForeignKey('bb_products.bb_id'), nullable=True) #外鍵的設定
    sc_id = mydb.Column(mydb.Integer, mydb.ForeignKey('sc_products.sc_id'), nullable=True) #外鍵的設定
    vb_id = mydb.Column(mydb.Integer, mydb.ForeignKey('vb_products.vb_id'), nullable=True) #外鍵的設定

    def __init__(self, u_name, amount, bb_id, sc_id, vb_id):
        self.u_name = u_name
        self.amount = amount
        self.bb_id = bb_id
        self.sc_id = sc_id
        self.vb_id = vb_id

#首頁
@app.route("/")
def index():
    if "username" in session:
        a=session["username"]
        return render_template("index.html", data=a)
    else:
        return render_template("index.html")
    
#會員登入
@app.route("/signin")
def signin():
    if "username" in session:
        return render_template("member.html")
    else:
        return render_template("signin.html")
    
#會員註冊
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/signup_form", methods=["POST"])
def signup_form():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["password2"]

    collection= modb.users #指定users集合
    result = collection.find_one({
        "email":email
    })

    if result != None:
        return redirect('/error?msg=電子郵件已被註冊!')
    elif password != password2:
        return redirect("/error?msg=密碼輸入不一致!")
    else:
        collection.insert_one({
            "username":username,
            "email":email,
            "password":password
        })
        return redirect("/signup_ok")

#會員登入功能
@app.route("/signin_form", methods=["POST"])
def signin_form():
    email = request.form["email"]
    password = request.form["password"]
    collection =modb.users
    result = collection.find_one({
        "$and":[
        {"email":email},
        {"password":password}
        ]
    })
    if result != None:
        session["username"]=result["username"]
        session["email"]=result["email"]
        return redirect("/member")
    else:
        return redirect("/error?msg=登入失敗!")

#會員介面
@app.route("/member")
def member():
    if "username" in session:
        username = session["username"]
        email = session["email"]
        return render_template("member.html",name=username,email=email)
        
    else:
        return redirect("/signin")
#登出功能
@app.route("/signout", methods=["GET"])
def signout():
    del session["username"]
    del session["email"]
    return redirect("/")


#錯誤頁面
@app.route("/error")
def error():
    message = request.args.get("msg","出現錯誤!")
    return render_template("error.html",msg=message)

#註冊成功頁面
@app.route('/signup_ok')
def ok():
    return render_template("signup_ok.html")



#取得商品資料並加入購物車資料庫
@app.route("/car_form", methods=["POST"])
def car_form():
    if "username" in session:
        bt_a = request.values.get("quick_buy")
        bt_b= request.values.get("send_car")
        if bt_a =="立即購買": #判斷點擊哪個按鈕
            username = session["username"]
            id = request.form["id"]
            amount = request.form["p_amount"]
            if int(id) <= 6:
                p =all_products.query.filter_by(p_id=int(id)).first()
                p_id = p.bb_products.bb_id
                p1 = AddToCar(username, amount, p_id, None,None)
                mydb.session.add(p1)
                mydb.session.commit()
                return redirect("car")
            elif 7 <= int(id) <= 12:
                p =all_products.query.filter_by(p_id=int(id)).first()
                p_id = p.sc_products.sc_id
                p1 = AddToCar(username, amount, None, p_id,None)
                mydb.session.add(p1)
                mydb.session.commit()
                return redirect("car")
            elif int(id) > 12 :
                p =all_products.query.filter_by(p_id=int(id)).first()
                p_id = p.vb_products.vb_id
                p1 = AddToCar(username, amount, None, None, p_id)
                mydb.session.add(p1)
                mydb.session.commit()
                return redirect("car")
        elif bt_b =="放入購物車":
            username = session["username"]
            id = request.form["id"]
            amount = request.form["p_amount"]
            if int(id) <= 6:
                p =all_products.query.filter_by(p_id=int(id)).first()
                p_id = p.bb_products.bb_id
                p1 = AddToCar(username, amount, p_id, None,None)
                mydb.session.add(p1)
                mydb.session.commit()
                return redirect("add_car")
            elif 7 <= int(id) <= 12:
                p =all_products.query.filter_by(p_id=int(id)).first()
                p_id = p.sc_products.sc_id
                p1 = AddToCar(username, amount, None, p_id,None)
                mydb.session.add(p1)
                mydb.session.commit()
                return redirect("add_car")
            elif int(id) > 12 :
                p =all_products.query.filter_by(p_id=int(id)).first()
                p_id = p.vb_products.vb_id
                p1 = AddToCar(username, amount, None, None, p_id)
                mydb.session.add(p1)
                mydb.session.commit()
                return redirect("add_car")
    else:
        return redirect("/signin")
    
#商品增加到購物車成功的頁面
@app.route("/add_car")
def car_ok():
    if "username" in session:
            return render_template("addcar_ok.html")
    else:
        return redirect("/signin")
    
#購物車頁面
@app.route("/car")
def car():
    if "username" in session:
        username= session["username"]
        a=session["username"]
        items=[]
        j=1
        total=0
        p =AddToCar.query.filter_by(u_name=username).all()
        for i in p:
            if i.bb_id:
                car_item={
                "p_id":j,
                "img":i.bb_products.bb_img,
                "name":i.bb_products.bb_name,
                "price":i.bb_products.bb_price,
                "amount":i.amount,
                "total":int(i.bb_products.bb_price) * int(i.amount),
                "c_id":i.c_id
                }
                items.append(car_item)
                j+=1
            elif i.sc_id:
                car_item={
                "p_id":j,
                "img":i.sc_products.sc_img,
                "name":i.sc_products.sc_name,
                "price":i.sc_products.sc_price,
                "amount":i.amount,
                "total":int(i.sc_products.sc_price) * int(i.amount),
                "c_id":i.c_id
                }
                items.append(car_item)
                j+=1
            elif i.vb_id:
                car_item={
                "p_id":j,
                "img":i.vb_products.vb_img,
                "name":i.vb_products.vb_name,
                "price":i.vb_products.vb_price,
                "amount":i.amount,
                "total":int(i.vb_products.vb_price) * int(i.amount),
                "c_id":i.c_id
                }
                items.append(car_item)
                j+=1
        for k in items:
            total += int(k["total"])
        return render_template("car.html", items=items, data=a, total_price=total)
    else:
        return redirect("/signin")
    
#刪除購物車項商品功能
@app.route("/del_car", methods=["POST"])
def del_car():
    if "username" in session:
        id = request.form["id"]
        p = AddToCar.query.filter_by(c_id = int(id)).first()
        mydb.session.delete(p)
        mydb.session.commit()
        return redirect("/car")
    else:
        return redirect("/signin")

#送出全部購物車訂單
@app.route("/send_car", methods=["POST"])
def send_car():
    if "username" in session:
        username = session["username"]
        p = AddToCar.query.filter_by(u_name = username).first()
        if p != None:
            mydb.session.query(AddToCar).filter_by(u_name = username).delete()
            mydb.session.commit()
            return redirect("/send_car_ok")
        else:
            return redirect('/error?msg=購物車為空!')
    else:
        return redirect("/signin")
    
#送出訂單成功頁面路由
@app.route("/send_car_ok")
def send_car_ok():
    if "username" in session:
        return render_template("send_car_ok.html")
    else:
        return redirect("/signin")
    
#籃球商品路由
@app.route("/ball6")
def ball6():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball6.html", data=a)
    else:
        return render_template("bb_product/ball6.html")
    
@app.route("/ball6-1")
def ball6_1():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball6-1.html", data=a)
    else:
        return render_template("bb_product/ball6-1.html")
    
@app.route("/ball6-2")
def ball6_2():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball6-2.html", data=a)
    else:
        return render_template("bb_product/ball6-2.html")
    
@app.route("/ball6-3")
def ball6_3():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball6-3.html", data=a)
    else:
        return render_template("bb_product/ball6-3.html")
    
@app.route("/ball7")
def ball7():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball7.html", data=a)
    else:
        return render_template("bb_product/ball7.html")
    
@app.route("/ball7-1")
def ball7_1():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball7-1.html", data=a)
    else:
        return render_template("bb_product/ball7-1.html")
    
@app.route("/ball7-2")
def ball7_2():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball7-2.html", data=a)
    else:
        return render_template("bb_product/ball7-2.html")
    
@app.route("/ball7-3")
def ball7_3():
    if "username" in session:
        a=session["username"]
        return render_template("bb_product/ball7-3.html", data=a)
    else:
        return render_template("bb_product/ball7-3.html")

#足球商品路由
@app.route("/sc_3")
def sc_3():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc_3.html", data=a)
    else:
        return render_template("sc_product/sc_3.html")
    
@app.route("/sc3-1")
def sc_3_1():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc3-1.html", data=a)
    else:
        return render_template("sc_product/sc3-1.html")
    
@app.route("/sc3-2")
def sc_3_2():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc3-2.html", data=a)
    else:
        return render_template("sc_product/sc3-2.html")
    
@app.route("/sc_4")
def sc_4():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc_4.html", data=a)
    else:
        return render_template("sc_product/sc_4.html")
    
@app.route("/sc4-1")
def sc_4_1():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc4-1.html", data=a)
    else:
        return render_template("sc_product/sc4-1.html")
    
@app.route("/sc4-2")
def sc_4_2():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc4-2.html", data=a)
    else:
        return render_template("sc_product/sc4-2.html")
    
@app.route("/sc_5")
def sc_5():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc_5.html", data=a)
    else:
        return render_template("sc_product/sc_5.html")
    
@app.route("/sc5-1")
def sc_5_1():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc5-1.html", data=a)
    else:
        return render_template("sc_product/sc5-1.html")
    
@app.route("/sc5-2")
def sc_5_2():
    if "username" in session:
        a=session["username"]
        return render_template("sc_product/sc5-2.html", data=a)
    else:
        return render_template("sc_product/sc5-2.html")


#排球商品路由
@app.route("/fivb")
def fivb():
    if "username" in session:
        a=session["username"]
        return render_template("vb_product/fivb.html", data=a)
    else:
        return render_template("vb_product/fivb.html")
    
@app.route("/fivb-1")
def fivb_1():
    if "username" in session:
        a=session["username"]
        return render_template("vb_product/fivb-1.html", data=a)
    else:
        return render_template("vb_product/fivb-1.html")
    
@app.route("/fivb-2")
def fivb_2():
    if "username" in session:
        a=session["username"]
        return render_template("vb_product/fivb-2.html", data=a)
    else:
        return render_template("vb_product/fivb-2.html")
    
@app.route("/vb")
def vb():
    if "username" in session:
        a=session["username"]
        return render_template("vb_product/vb.html", data=a)
    else:
        return render_template("vb_product/vb.html")
    
@app.route("/vb-1")
def vb_1():
    if "username" in session:
        a=session["username"]
        return render_template("vb_product/vb-1.html", data=a)
    else:
        return render_template("vb_product/vb-1.html")
    
@app.route("/vb-2")
def vb_2():
    if "username" in session:
        a=session["username"]
        return render_template("vb_product/vb-2.html", data=a)
    else:
        return render_template("vb_product/vb-2.html")

#搜尋功能
@app.route("/search", methods=["POST"])
def search():
    search_items=[]
    s_item= request.form["search_name"]
    j=1
    p = all_products.query.filter(all_products.name.contains(s_item)).all()
    for i in p:
        if i.bb_id:
            search_item={
                "id":j,
                "name":i.bb_products.bb_name,
                "img":i.bb_products.bb_img,
                "link": i.bb_products.bb_link
                }
            search_items.append(search_item)
            j+=1
        elif i.sc_id:
            search_item={
                "id":j,
                "name":i.sc_products.sc_name,
                "img":i.sc_products.sc_img,
                "link": i.sc_products.sc_link
                }
            search_items.append(search_item)
            j+=1
        elif i.vb_id:
            search_item={
                "id":j,
                "name":i.vb_products.vb_name,
                "img":i.vb_products.vb_img,
                "link": i.vb_products.vb_link
                }
            search_items.append(search_item)
            j+=1
    for k in search_items:
        print(k)
    return render_template("search.html", items= search_items, s_item= s_item)

# app.run(port=3500, debug=True) #部屬在heroku不需要app.run, templates資料夾開頭不能大寫
