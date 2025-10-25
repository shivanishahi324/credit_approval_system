def calculate_credit_score(customer):
    score = 50  # base score

    # 1️⃣ if customer's debt approved is under limit 
    if customer.current_debt <= customer.approved_limit:
        score += 20
    else:
        score -= 20

    # 2️⃣ if monthly income is more than 30,000 
    if customer.monthly_income > 30000:
        score += 10

    # 3️⃣ Ensure score always between 0 and 100
    if score > 100:
        score = 100
    elif score < 0:
        score = 0

    return score
