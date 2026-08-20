import unittest

def calculate_emi(principal, annual_rate, tenure_months):
    if not isinstance(principal, (int, float)) or not isinstance(annual_rate, (int, float)) or not isinstance(tenure_months, int):
        raise TypeError("Invalid data types for EMI calculation")
    if principal < 0 or annual_rate < 0 or tenure_months <= 0:
        raise ValueError("Invalid numeric values for EMI calculation")
    if annual_rate == 0:
        return principal / tenure_months
    monthly_rate = (annual_rate / 12) / 100
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return emi

def evaluate_loan(age, monthly_salary, existing_loan_emi, credit_score, employment_type, requested_amount, loan_tenure_months):
    if not isinstance(age, int) or not isinstance(credit_score, int) or not isinstance(loan_tenure_months, int):
        raise TypeError("Age, credit score, and tenure must be integers")
    if not isinstance(monthly_salary, (int, float)) or not isinstance(existing_loan_emi, (int, float)) or not isinstance(requested_amount, (int, float)):
        raise TypeError("Salary, existing EMI, and requested amount must be numeric")
    
    if monthly_salary <= 0:
        raise ValueError("Monthly salary must be greater than zero")
    if age <= 0 or credit_score < 0 or existing_loan_emi < 0 or requested_amount < 0 or loan_tenure_months <= 0:
        raise ValueError("Input values cannot be negative or zero where applicable")

    employment_type = str(employment_type).strip().lower()
    if employment_type not in ["salaried", "self-employed"]:
        raise ValueError("Invalid employment type")

    rejection_reasons = []
    
    if age < 21 or age > 60:
        rejection_reasons.append("Age outside eligible bracket")
    
    if credit_score < 650:
        rejection_reasons.append("Poor credit score")

    if credit_score >= 750:
        interest_rate = 8.5
    elif credit_score >= 700:
        interest_rate = 10.0
    else:
        interest_rate = 12.5

    if employment_type == "self-employed":
        interest_rate += 1.0

    projected_emi = calculate_emi(requested_amount, interest_rate, loan_tenure_months)
    total_future_debt = existing_loan_emi + projected_emi
    dti_ratio = (total_future_debt / monthly_salary) * 100

    if dti_ratio > 50.0:
        rejection_reasons.append("High debt-to-income ratio")

    max_eligible_amount = (monthly_salary * 12) * 4
    if requested_amount > max_eligible_amount:
        rejection_reasons.append("Exceeds max eligible loan amount")

    if len(rejection_reasons) == 0:
        return {"status": "APPROVED", "rate": interest_rate, "emi": round(projected_emi, 2), "dti": round(dti_ratio, 2)}
    else:
        return {"status": "REJECTED", "reasons": rejection_reasons, "dti": round(dti_ratio, 2)}


class TestLoanProcessingSystem(unittest.TestCase):

    def test_minimum_age_boundary(self):
        res_underage = evaluate_loan(20, 5000, 500, 750, "salaried", 10000, 24)
        self.assertEqual(res_underage["status"], "REJECTED")
        self.assertIn("Age outside eligible bracket", res_underage["reasons"])

        res_exact_min = evaluate_loan(21, 5000, 500, 750, "salaried", 10000, 24)
        self.assertEqual(res_exact_min["status"], "APPROVED")

    def test_maximum_age_boundary(self):
        res_overage = evaluate_loan(61, 5000, 500, 750, "salaried", 10000, 24)
        self.assertEqual(res_overage["status"], "REJECTED")
        self.assertIn("Age outside eligible bracket", res_overage["reasons"])

        res_exact_max = evaluate_loan(60, 5000, 500, 750, "salaried", 10000, 24)
        self.assertEqual(res_exact_max["status"], "APPROVED")

    def test_invalid_salary(self):
        with self.assertRaises(ValueError):
            evaluate_loan(30, 0, 500, 750, "salaried", 10000, 24)
        with self.assertRaises(ValueError):
            evaluate_loan(30, -1000, 500, 750, "salaried", 10000, 24)

    def test_poor_credit_score(self):
        res = evaluate_loan(30, 5000, 0, 649, "salaried", 10000, 24)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Poor credit score", res["reasons"])

    def test_existing_loan_exceeding_threshold(self):
        res = evaluate_loan(30, 5000, 3000, 750, "salaried", 5000, 24)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("High debt-to-income ratio", res["reasons"])

    def test_high_debt_to_income_ratio(self):
        res = evaluate_loan(30, 4000, 1500, 700, "salaried", 20000, 12)
        self.assertTrue(res["dti"] > 50.0)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("High debt-to-income ratio", res["reasons"])

    def test_employment_categories(self):
        res_salaried = evaluate_loan(30, 5000, 0, 750, "salaried", 10000, 24)
        res_self_employed = evaluate_loan(30, 5000, 0, 750, "self-employed", 10000, 24)
        
        self.assertEqual(res_salaried["rate"], 8.5)
        self.assertEqual(res_self_employed["rate"], 9.5)

    def test_boundary_loan_amounts(self):
        max_allowed = (5000 * 12) * 4
        res_exact_max = evaluate_loan(30, 5000, 0, 750, "salaried", max_allowed, 60)
        self.assertEqual(res_exact_max["status"], "APPROVED")

        res_above_max = evaluate_loan(30, 5000, 0, 750, "salaried", max_allowed + 1, 60)
        self.assertEqual(res_above_max["status"], "REJECTED")
        self.assertIn("Exceeds max eligible loan amount", res_above_max["reasons"])

    def test_emi_calculation_accuracy(self):
        emi = calculate_emi(10000, 12.0, 12)
        self.assertAlmostEqual(emi, 888.49, places=2)

    def test_invalid_input_handling(self):
        with self.assertRaises(ValueError):
            evaluate_loan(30, 5000, 0, 750, "unemployed", 10000, 24)

    def test_exception_handling_types(self):
        with self.assertRaises(TypeError):
            evaluate_loan("thirty", 5000, 0, 750, "salaried", 10000, 24)
        with self.assertRaises(TypeError):
            calculate_emi(10000, "twelve", 12)


if __name__ == "__main__":
    unittest.main()
