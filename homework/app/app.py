from flask import Flask, request, session, render_template

import kandinskiy

from dotenv import dotenv_values

app = Flask(__name__)

print(app.instance_path)

# для использования переменной app.session
app.config["SECRET_KEY"] = dotenv_values(".flask_env")["SECRET_KEY"]


@app.route("/")
def index():
    # сохраняем pipeline_id в переменной сессии, чтобы каждый раз не пришлось его получать

    if "pipeline_id" not in session.keys():
        print("requesting pipeline_id")
        session["pipeline_id"] = kandinskiy.setup()

    availability_status = kandinskiy.is_available(session["pipeline_id"])

    generation_styles = kandinskiy.get_styles()
       
    template_params = {
        "pipeline_id" : session["pipeline_id"],
        "status" : availability_status,
        "styles" : generation_styles,
    }

    return render_template('index.html', **template_params)
 
@app.route("/generate", methods=["POST"])
def generate_image():

    prompt = dict(request.form)
    # после проверки правильности запроса к сервису,
    # отправляем запрос к нейросетил

    if not hasattr(prompt, "style"):
        prompt["style"] = "DEFAULT"
    
    image_name = kandinskiy.generate_image(prompt, session["pipeline_id"])
    
    return render_template('show_image.html', image_name=image_name)



@app.route("/availability")
def is_available():
    return kandinskiy.is_available(session["pipeline_id"])

@app.route("/styles")
def get_styles():
    return kandinskiy.get_styles(session["pipeline_id"])

if __name__ == "__main__":
    app.run()
