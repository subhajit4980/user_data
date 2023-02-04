from flask import Flask, jsonify, request,json
from config import db, SECRET_KEY
from os import environ
from user import USER
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=environ.get('DB_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.secret_key = SECRET_KEY
db.init_app(app)
def create_app():
    with app.app_context():
        @app.route('/add_user', methods=['POST'])
        def add_user():
            data = request.form.to_dict(flat=True)
            new_customer = USER(
                username=data["username"],
                password=data['password'],
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address']
            )
            try:
                users=USER.query.all()
                usernamelist=[user.username for user in users]
                if new_customer.username  not in usernamelist:
                    db.session.add(new_customer)
                    db.session.commit()
                else:
                    return jsonify("username already in used")
            except:
                return jsonify("some thing went wrong")
            return jsonify(msg="Signup Successfully")
        # db.drop_all()
        @app.route('/get_user', methods=['GET'])
        def get_user():
            users=USER.query.all()
            user_data={}
            user_data["users"]=[]
            for us in users:
                us_data={}
                us_data["id"]=us.id
                us_data["username"]=us.username
                us_data["password"]=us.password
                us_data["name"]=us.name
                us_data["email"]=us.email
                us_data["phone"]=us.phone
                us_data["address"]=us.address
                user_data["users"].append(us_data)
            return json.dumps(user_data)
        db.create_all()
        db.session.commit()
        return app
if __name__ == "__main__":
    app=create_app()
    app.run(host="0.0.0.0", port='4545', debug='True')