import pandas as pd
from celery import shared_task
from customers.models import Customer
from loans.models import Loan

@shared_task
def ingest_initial_data():
    try:
        print(" Reading Excel files...")
        customer_df = pd.read_excel('customer_data.xlsx')
        loan_df = pd.read_excel('loan_data.xlsx')

        print(" Customer columns:", list(customer_df.columns))
        print(" Loan columns:", list(loan_df.columns))

        #  Insert customer data
        for _, row in customer_df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],  # use your new field, NOT id
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row['    Age'],
                    'phone_number': row['Phone Number'],
                    'monthly_income': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                    'current_debt': row['Current Debt']
                }
            )

        #  Insert loan data
        for _, row in loan_df.iterrows():
            customer = Customer.objects.filter(customer_id=row['Customer ID']).first()
            if not customer:
                print(f"  Skipping loan — customer {row['Customer ID']} not found.")
                continue

            Loan.objects.update_or_create(
                id=row['Loan ID'],  # Loan ka apna ID ok hai
                defaults={
                    'customer': customer,
                    'loan_amount': row['Loan Amount'],
                    'tenure': row['Tenure'],
                    'interest_rate': row['Interest Rate'],
                    'monthly_installment': row['Monthly payment'],
                    'emis_paid_on_time': row['EMIs paid on Time'],
                    'start_date': row['Date of Approval'],
                    'end_date': row['End Date']
                }
            )

        print("  Data ingestion completed successfully!")
        return "Success"

    except Exception as e:
        import traceback
        print("  Error during ingestion:")
        traceback.print_exc()
        return "Failed"
