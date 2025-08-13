# harman2 폴더 내
# project 폴더 내
# server 폴더 내
# exam01.py

# request : clinet -> server
# response : server -> client

# python server
# 1) flask : 마이크로 웹 프레임워크(12000 line)
# 2) Django : 모든 기능 포함 (flask보다 10 ~ 20배 무거움)

from flask import Flask # route 경로 설정, run 서버 실행
from flask import render_template # html load
from flask import request # 사용자가 보낸 정보
from flask import redirect # 페이지 이동
from flask import make_response # 페이지 이동시 정보 유지

# aws.py 안에 detect 관련 함수만 쓰고 싶음
from aws import detect_labels_local_file
from aws import compare_faces as cf

# 파일 이름 보안처리 라이브러리
from werkzeug.utils import secure_filename

import os
# static 폴더가 없으면 만들어라
if not os.path.exists("static"):
    os.mkdir("static")
    
# get -> args[key]
# post -> form[key]

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare_faces():

    # /detect 통해서 한 내용과 거의 동일
    # file이 2개일 뿐
    # 1. compare로 오는 file1, file2를 받아서
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        file1_filename = secure_filename(file1.filename)
        file2_filename = secure_filename(file2.filename)

        file1.save("static/" + file1_filename)
        file2.save("static/" + file2_filename)

    # static폴더에 save
    # 이때, secure_filename 사용해서
    # 2. aws.py 얼굴 비교 aws 코드
    # 이 결과를 통해 웹 페이지에
    # "동일 인물 확률 ??.??%입니다."
    # 3. aws.py 안에 함수를 불러와서
    # exam01.py 사용

        r = cf("static/" + file1_filename, "static/" + file2_filename)

    return r

@app.route("/detect", methods=["POST"])
def detect_label():

    # flask 보안 규칙상 file 이름은 secure 처리 해야함
    if request.method == "POST":
        file = request.files["file"]

        # file을 static 폴더에 저장하고
        file_name = secure_filename(file.filename)
        file.save("static/" + file_name)
        # 해당 경로를 detect_lo ~ 함수에 전달
        r = detect_labels_local_file("static/" + file_name)

    return r

@app.route("/secret", methods=["POST"])
def box():
    try:
        if request.method == "POST":
            hidden = request.form["hidden"]
            return f"비밀정보 : {hidden}"
    except:
        return "데이터 전송 실패"

@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":

        # 페이지 이동 : redirect
        # 페이지가 이동하더라도 정보를 남겨서 사용
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        if login_id == "leejaewon" and login_pw == "0626":
            # 로그인 성공
            response = make_response(redirect("/login/success"))
            response.set_cookie("user", login_id)
            return response
        else:
            return redirect("/")

    return "로그인 성공"

@app.route("/login/success", methods=["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__ == "__main__":
    app.run(host="0.0.0.0" )