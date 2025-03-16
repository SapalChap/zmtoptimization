import pandas as pd
import pulp
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, LpStatus

data = pd.read_csv("C:/Users/sapal/Documents/ZMT Project/ZMTFoodDB.csv")

#Clean and turn to dataframe
data = data.dropna()
df = pd.DataFrame(data)

df['Total_MicroNutrients'] = df['Vitamin B6 (mg)'] + df['Vitamin C (mg)']+ df['Vitamin E (mg)']+ df['Magnesium (mg)']

df['Pounds(lbs)'] = df['Weight (g)'] * 0.00220462
df['Cost($)'] = df['Pounds(lbs)']* 14.99

# Step 1: Create the problem
prob = LpProblem("Maximize_Nutrition", LpMaximize)

# Step 2: Define decision variables
food_vars = {row['Food']: LpVariable(row['Food'], lowBound=0, cat="Integer") for index, row in df.iterrows()}


def set_macro_priority(macro):
	
	global prob
	
	if macro == "Protein":
		prob += (
		1000 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		100 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		10 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Protein_Priority"
	)
	elif macro == "Carbs":
		prob += (
		100 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		1000 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		10 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Carbs_Priority"
	)
	elif macro == "Fats":
		prob += (
		100 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		10 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		1000 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Fats_Priority"
	)
	elif macro == "Micronutrients":
		prob += (
		100 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		10 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		1 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1000 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Micronutrients_Priority"
	)
	else:
		print("Error, choose between protein, carbs, fats or micronutrients")
		

set_macro_priority("Protein")
		
#Constraints

max_cost = 20

prob += lpSum(row['Cost($)'] * food_vars[row['Food']] for index, row in df.iterrows()) <= max_cost, "Cost_Constraint"

#Max 1 of ecah food
for food in food_vars:
    prob += food_vars[food] <= 1, f"Max_{food}"

#Constrant 3: Category Variation

Meat_Req = 2
Starch_Req = 2
Vegetables_Req = 4
Seafood_Req = 2

# Meats
prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Meats'].iterrows()) == Meat_Req, "Meat_Requirement"

# Starch
prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Starch'].iterrows()) == Starch_Req, "Starch_Requirement"

# Vegetables
prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Vegetables'].iterrows()) == Vegetables_Req, "Vegetables_Requirement"

# Seafood
prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Seafood'].iterrows()) == Seafood_Req, "Seafood_Requirement"

# Step 5: Solve the problem
prob.solve()

# Step 6: Check the status
status = LpStatus[prob.status]
print("Status:", status)


print("Total Cost:", sum(row['Cost($)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()))
print("Total Protein:", sum(row['Protein (g)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()))
print("Total Carbs:", sum(row['Carbs (g)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()))
print("Total Fats:", sum(row['Fats (g)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()))
print("Total Micronutrients:", sum(row['Total_MicroNutrients'] * food_vars[row['Food']].varValue for index, row in df.iterrows()))

print("\nFood Quantities:")
    
for food in food_vars:
    if food_vars[food].varValue != 0:  # Check if the food quantity is non-zero
        # Find the serving size for the current food
        serving_size = df.loc[df['Food'] == food, 'Serving Size'].values[0]
        print(f"{food}: {food_vars[food].varValue} ({serving_size})")
        

