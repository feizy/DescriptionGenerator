from flask import Flask, request, render_template, redirect, url_for
import requests
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("API_KEY")
print(openai.api_key)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/code", methods=["POST","GET"])
def generate_code():
    if request.method == "POST":
        model_engine = "code-davinci-002"
        prompt = request.form['question']
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.3,
        )
        answer = completions.choices[0].text
        return render_template("code.html", answer=answer)
    return render_template("code.html")


@app.route("/generate", methods=["POST","GET"])
def generate_description():
    if request.method == "POST":
        model_engine = "text-davinci-003"
        product_category = request.form["product_category"]
        brand = request.form["brand"]
        color = request.form["color"]
        material = request.form["material"]
        additional_info = request.form["additional_info"]
        prompt = generate_prompt(product_category, brand, color, material, additional_info)
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        product_description = completions.choices[0].text
        return render_template("description.html", product_description=product_description)
    return render_template("description.html")

@app.route('/goto_code')
def goto_code():
    return redirect(url_for('generate_code'))

@app.route('/goto_description')
def goto_description():
    return redirect(url_for('generate_description'))

def generate_prompt(product_category, brand, color, material, additional_info):
    return """生成一个商品描述，语言要生动准确;
    第一段描述基本属性，第二段描述一下使用场景;
    第三段描述一下适用人群;
    不要平铺直叙，口语化一些，增加细节描述
商品类别: {}
品牌: {}
颜色: {}
材质: {}
补充特点: {}
""".format(
        product_category, brand, color, material, additional_info
    )
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)