from django.core.management.base import BaseCommand
import pandas as pd
from customers.models import Customer
from loans.models import Loan


class Command(BaseCommand):
    help = "Import customer and loan data from Excel files"

    def handle(self, *args, **kwargs):
        try:
            customer_df = pd.read_excel("customer_data.xlsx")
            loan_df = pd.read_excel("loan_data.xlsx")

            for _, row in customer_df.iterrows():
                Customer.objects.update_or_create(
                    id=row["Customer ID"],
                    defaults={
                        "first_name": row["First Name"],
                        "last_name": row["Last Name"],
                        "age": row["    Age"],
                        "phone_number": row["Phone Number"],
                        "monthly_income": row["Monthly Salary"],
                        "approved_limit": row["Approved Limit"],
                        "current_debt": row["Current Debt"],
                    },
                )

            for _, row in loan_df.iterrows():
                Loan.objects.update_or_create(
                    id=row["Loan ID"],
                    defaults={
                        "customer_id_id": row["Customer ID"],
                        "loan_amount": row["Loan Amount"],
                        "tenure": row["Tenure"],
                        "interest_rate": row["Interest Rate"],
                        "monthly_repayment": row["Monthly payment"],
                        "emis_paid_on_time": row["EMIs paid on Time"],
                        "start_date": row["Date of Approval"],
                        "end_date": row["End Date"],
                    },
                )

            self.stdout.write(self.style.SUCCESS(" Data imported successfully!"))

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.stdout.write(self.style.ERROR(f" Import failed: {e}"))
