import csv, json

potentialCustomers = { "Potential Customers": [] }
output = []

def openInput():
    with open('data/input.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        lineNo = 0

        for row in spamreader:

            lineNo += 1
            if lineNo == 1: continue

            potentialCustomers["Potential Customers"].append({
                "name": row[0],
                "age": int(row[1]),
                "gender": row[2],
                "smoker": row[3],
                "email": row[4],
                "height": row[5],
                "weight": row[6],
                "bmi": bmiCalculator(row[6], row[5]),
                "health": row[7],
                "alcohol": float(row[8]),
                "postalcode": row[9],
                "policyRequested": float(row[10])
                })

def calculatePremiums():
    for customer in potentialCustomers["Potential Customers"]:
        calculateScore(customer)
        calculatePremium(customer)

        output.append({
            "name": customer["name"],
            "bmi": customer["bmi"],
            "score": customer["score"],
            "monthly premium": customer["monthlyPremium"]
        })
        
def bmiCalculator(weight, height):
    f_weight = float(weight)
    f_height = float(height)
    return (f_weight / f_height / f_height) * 10000

def calculatePremium(customer):
    premiumMultiplier = 0
    if customer["age"] > 18 and customer["age"] <= 40:
        if customer["smoker"] == "S":
            premiumMultiplier = 0.25
        else:
            premiumMultiplier = 0.1

    
    if customer["age"] > 40 and customer["age"] <= 60:
        if customer["smoker"] == "S":
            premiumMultiplier = 0.55
        else:
            premiumMultiplier = 0.3

    monthlyPremium = (customer["policyRequested"] / 1000) * customer["premiumMultiplier"] * premiumMultiplier / 12
    customer["monthlyPremium"] = round(monthlyPremium, 2)

def calculateScore(customer):
    score = 0
    multiplier = 1

    # 15 points
    if customer["bmi"] < 18.5:              score = score + 15
    if "ANXIETY" in customer["health"]:     score = score + 15
    if "DEPRESSION" in customer["health"]:  score = score + 15

    # 25 points
    if "SURGERY" in customer["health"]: score = score + 25
    if customer["smoker"] == "S":       score = score + 25
    if customer["bmi"] > 25:            score = score + 25
    if customer["alcohol"] > 10:        score = score + 25

    # 30 points
    if "HEART" in customer["health"]:   score = score + 30
    if customer["bmi"] > 30:            score = score + 30
    if customer["alcohol"] > 25:        score = score + 30

    if score > 100:
        multiplier = 1.25
    elif score > 75 and score <= 100:
        multiplier = 1.15
    
    customer["score"] = score
    customer["premiumMultiplier"] = multiplier
    
def writeJsonOutput():
    with open('data/output.json', 'w') as fp:
        json.dump(output, fp, indent=4)

    with open('data/total_output.json', 'w') as fp:
        json.dump(potentialCustomers, fp, indent=4)

def main():
    openInput()
    calculatePremiums()
    writeJsonOutput()


if __name__ == '__main__':
    main()