import sys
import os

def calculate_emi(principal, annual_rate, tenure_months):
    if annual_rate == 0:
        return principal / tenure_months
    monthly_rate = (annual_rate / 12) / 100
    return principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)

def process_loan():
    print("--- Loan Processing System ---")
    
    # Auto-detect Jenkins or command-line arguments
    if "JENKINS_HOME" in os.environ or len(sys.argv) > 1:
        print("[Automation Detected] Bypassing interactive inputs...")
        customer_id = sys.argv[1] if len(sys.argv) > 1 else "JENKINS-TEST"
        age = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monthly_salary = float(sys.argv[3]) if len(sys.argv) > 3 else 5000.0
        existing_loan_emi = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
        credit_score = int(sys.argv[5]) if len(sys.argv) > 5 else 720
        employment_type = (sys.argv[6] if len(sys.argv) > 6 else "salaried").strip().lower()
        requested_amount = float(sys.argv[7]) if len(sys.argv) > 7 else 15000.0
        loan_tenure_months = int(sys.argv[8]) if len(sys.argv) > 8 else 24
    else:
        # Standard interactive questions for manual testing
        customer_id = input("Enter Customer ID: ")
        age = int(input("Enter Age: "))
        monthly_salary = float(input("Enter Monthly Salary: "))
        existing_loan_emi = float(input("Enter Total Existing Loan EMI/Payments: "))
        credit_score = int(input("Enter Credit Score: "))
        employment_type = input("Enter Employment Type (Salaried/Self-Employed): ").strip().lower()
        requested_amount = float(input("Enter Requested Loan Amount: "))
        loan_tenure_months = int(input("Enter Loan Tenure (in months): "))

    rejection_reasons = []
    
    if age < 21 or age > 60:
        rejection_reasons.append(f"Age {age} is outside the eligible bracket (21-60).")
    
    if credit_score < 650:
        rejection_reasons.append(f"Credit score {credit_score} is below the minimum required (650).")

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
        rejection_reasons.append(f"Debt-to-Income ratio ({dti_ratio:.2f}%) exceeds the 50% limit.")

    max_eligible_amount = (monthly_salary * 12) * 4
    
    if requested_amount > max_eligible_amount:
        rejection_reasons.append(f"Requested amount exceeds max eligibility limit of {max_eligible_amount:,.2f}.")

    if len(rejection_reasons) == 0:
        status = "APPROVED"
        final_approved_amount = requested_amount
        final_emi = projected_emi
    else:
        status = "REJECTED"
        final_approved_amount = 0.0
        final_emi = 0.0

    print("\n====================================")
    print("         LOAN PROCESS REPORT        ")
    print("====================================")
    print(f"Customer ID:          {customer_id}")
    print(f"Employment Type:      {employment_type.capitalize()}")
    print(f"Credit Score:         {credit_score}")
    print(f"Debt-to-Income Ratio: {dti_ratio:.2f}%")
    print(f"Assessed Interest Rate:{interest_rate:.2f}%")
    print(f"Max Eligible Amount:  {max_eligible_amount:,.2f}")
    print(f"Status:               {status}")
    
    if status == "APPROVED":
        print(f"Approved Amount:      {final_approved_amount:,.2f}")
        print(f"Monthly EMI:          {final_emi:,.2f}")
    else:
        print("\nReasons for Rejection:")
        for reason in rejection_reasons:
            print(f" - {reason}")
    print("====================================")

if __name__ == "__main__":
    process_loan()
