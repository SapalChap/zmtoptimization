import pandas as pd
import pulp
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, LpStatus
from config import DB_PATH

def optimize_malatang(p_max_cost_main, p_macro_priority_main, p_meat_req_main, p_starch_req_main, p_vegetables_req_main, p_seafood_req_main):
	# Load and prepare data
	data = pd.read_csv(DB_PATH)
	data = data.dropna()
	df = pd.DataFrame(data)

	df['Total_MicroNutrients'] = df['Vitamin B6 (mg)'] + df['Vitamin C (mg)']+ df['Vitamin E (mg)']+ df['Magnesium (mg)']
	df['Pounds(lbs)'] = df['Weight (g)'] * 0.00220462
	df['Cost($)'] = df['Pounds(lbs)']* 14.99

	# Create the problem
	prob = LpProblem("Maximize_Nutrition", LpMaximize)

	# Define decision variables
	food_vars = {row['Food']: LpVariable(row['Food'], lowBound=0, cat="Integer") for index, row in df.iterrows()}

	# Set macro priority objective function
	if p_macro_priority_main == "Protein":
		prob += (
		1000 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		100 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		10 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Protein_Priority"
		)
	elif p_macro_priority_main == "Carbs":
		prob += (
		100 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		1000 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		10 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Carbs_Priority"
		)
	elif p_macro_priority_main == "Fats":
		prob += (
		100 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		10 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		1000 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Fats_Priority"
		)
	elif p_macro_priority_main == "Micronutrients":
		prob += (
		100 * lpSum(row['Protein (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +  
		10 * lpSum(row['Carbs (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +     
		1 * lpSum(row['Fats (g)'] * food_vars[row['Food']] for index, row in df.iterrows()) +       
		1000 * lpSum(row['Total_MicroNutrients'] * food_vars[row['Food']] for index, row in df.iterrows()), 
		"Micronutrients_Priority"
		)
	else:
		print("Error, choose between protein, carbs, fats or micronutrients")
		return None

	# Set cost constraint
	prob += lpSum(row['Cost($)'] * food_vars[row['Food']] for index, row in df.iterrows()) <= p_max_cost_main, "Cost_Constraint"

	# Max 1 of each food constraint
	for food in food_vars:
		prob += food_vars[food] <= 1, f"Max_{food}"

	# Category variation constraints
	prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Meats'].iterrows()) == p_meat_req_main, "Meat_Requirement"
	prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Starch'].iterrows()) == p_starch_req_main, "Starch_Requirement"
	prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Vegetables'].iterrows()) == p_vegetables_req_main, "Vegetables_Requirement"
	prob += lpSum(food_vars[row['Food']] for index, row in df[df['Category'] == 'Seafood'].iterrows()) == p_seafood_req_main, "Seafood_Requirement"

	# Solve the problem
	prob.solve()

	# Get results
	status = LpStatus[prob.status]
	results = {
		"status": status,
		"total_cost": sum(row['Cost($)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()),
		"total_protein": sum(row['Protein (g)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()),
		"total_carbs": sum(row['Carbs (g)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()),
		"total_fats": sum(row['Fats (g)'] * food_vars[row['Food']].varValue for index, row in df.iterrows()),
		"total_micronutrients": sum(row['Total_MicroNutrients'] * food_vars[row['Food']].varValue for index, row in df.iterrows()),
		"selected_foods": []
	}

	# Get selected foods and their serving sizes
	for food in food_vars:
		if food_vars[food].varValue != 0:
			serving_size = df.loc[df['Food'] == food, 'Serving Size'].values[0]
			results["selected_foods"].append({
				"food": food,
				"quantity": food_vars[food].varValue,
				"serving_size": serving_size
			})

	return results

# Example usage
if __name__ == "__main__":
	results = optimize_malatang(20, "Protein", 1, 1, 2, 1)
	
	# Print results
	print("Status:", results["status"])
	print("Total Cost:", results["total_cost"])
	print("Total Protein:", results["total_protein"])
	print("Total Carbs:", results["total_carbs"])
	print("Total Fats:", results["total_fats"])
	print("Total Micronutrients:", results["total_micronutrients"])
	
	print("\nFood Quantities:")
	for food in results["selected_foods"]:
		print(f"{food['food']}: {food['quantity']} ({food['serving_size']})")
