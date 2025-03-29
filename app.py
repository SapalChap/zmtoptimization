from flask import Flask, render_template, request, redirect, url_for, session
from optimizer import optimize_malatang
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/constraints', methods=['GET', 'POST'])
def constraints():
    if request.method == 'POST':
        try:
            # Store form data in session
            session['max_price'] = float(request.form.get('max_price'))
            session['priority'] = request.form.get('priority').capitalize()  # Match case in optimizer
            session['meat_variation'] = int(request.form.get('meat_variation'))
            session['starch_variation'] = int(request.form.get('starch_variation'))
            session['vegetable_variation'] = int(request.form.get('vegetable_variation'))
            session['seafood_variation'] = int(request.form.get('seafood_variation'))
            
            return redirect(url_for('results'))
        except Exception as e:
            print(f"Error in form processing: {str(e)}")
            return redirect(url_for('constraints'))
    
    return render_template('constraints.html')

@app.route('/results')
def results():
    if 'max_price' not in session:
        return redirect(url_for('constraints'))
    
    try:
        results = optimize_malatang(
            p_max_cost_main=session['max_price'],
            p_macro_priority_main=session['priority'],
            p_meat_req_main=session['meat_variation'],
            p_starch_req_main=session['starch_variation'],
            p_vegetables_req_main=session['vegetable_variation'],
            p_seafood_req_main=session['seafood_variation']
        )
        
        if results is None:
            print("Optimization returned None")
            return redirect(url_for('constraints'))
            
        return render_template('results.html', results=results)
    except Exception as e:
        print(f"Error in optimization: {str(e)}")
        return redirect(url_for('constraints'))

if __name__ == '__main__':
    app.run(debug=True) 