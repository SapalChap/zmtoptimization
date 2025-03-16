from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/constraints', methods=['GET', 'POST'])
def constraints():
    if request.method == 'POST':
        # Collect form data
        max_price = request.form.get('max_price')
        priority = request.form.get('priority')
        meat_variation = request.form.get('meat_variation')
        starch_variation = request.form.get('starch_variation')
        vegetable_variation = request.form.get('vegetable_variation')
        seafood_variation = request.form.get('seafood_variation')
        
        return redirect(url_for('results'))
    
    return render_template('constraints.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True) 