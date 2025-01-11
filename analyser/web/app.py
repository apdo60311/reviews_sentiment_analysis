import flask
from flask import request
from flask import render_template
import utils.seintmeint as seintmeint
import utils.gen_similar as gen

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        comment = request.form['comment']
        s, level = seintmeint.analyze_sentiment(comment)
        print(comment)

        if s == None:
            return render_template('index.html', sentiment_result = "None", percent=level)          

        return render_template('index.html', sentiment_result = s, percent="{:.2f}".format(level * 100))
    else:
        return render_template('index.html')




@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    if request.method == 'POST':
        url = request.form['url']
        print(url)
        try:
            scraped_data = "Sample scraped data"  
            return render_template('scrapper.html', data=scraped_data)
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            return render_template('scrapper.html', error=error_message)
    else:
        return render_template('scrapper.html')
    

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        text = request.form['prompt']
        try:

            generator = gen.TextGenerator()
            return render_template('generate.html', generated_text=generator.generate_similar_text(text))
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            return render_template('generate.html', error=error_message)
    else:
        default_prompt = request.args.get('message')
        return render_template('generate.html', default_prompt = default_prompt)
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)