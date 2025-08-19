# Zhang Liang Malatang Optimizer (ZMT Optimization)

**ZMT Optimization** is a web app that helps users build the most optimal **DIY hotpot bowl** from *Zhang Liang Malatang*—balancing nutritional goals like protein, carbs, fats, or micronutrients, while staying within a budget and ingredient preferences.

---

##  Demo & Context

Built by SapalChap, this was inspired by a visit to Zhang Liang Malatang in Mountain View and combines interests in mathematics, fitness, and data science. It uses linear programming to maximize nutritional value per dollar spent. The Flask-powered web app is hosted on PythonAnywhere and sees around ~200 monthly visits.

---

## Features

- **Macronutrient Prioritization**: Choose to prioritize protein, carbs, fats, or micronutrients. :contentReference[oaicite:1]{index=1}  
- **Budget Constraint**: Set your maximum spend per bowl (minimum $5). :contentReference[oaicite:2]{index=2}  
- **Ingredient Variety**: Specify how many items to include from each category (meats, starches, vegetables, seafood). :contentReference[oaicite:3]{index=3}  
- **Optimization via Linear Programming**: Utilizes PuLP in Python to solve the optimization problem. :contentReference[oaicite:4]{index=4}  
- **Food Data Compilation**: Combines USDA database with additional sources for missing ingredients fetched from DoorDash data. :contentReference[oaicite:5]{index=5}  
- **Lightweight Web UI**: Built with Flask and deployed on PythonAnywhere for easy adjustments and interaction. :contentReference[oaicite:6]{index=6}  
