from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customers.models import Customer
from .models import Loan
from .services.eligibility import calculate_credit_score


# ---------------------------------------
#      CHECK ELIGIBILITY
# ---------------------------------------
class CheckEligibility(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = request.data.get("loan_amount")
        interest_rate = request.data.get("interest_rate")
        tenure = request.data.get("tenure")

        # Required fields
        if customer_id is None or loan_amount is None or tenure is None:
            return Response({"error": "customer_id, loan_amount and tenure are required"},
                            status=400)

        # Default interest rate
        if interest_rate is None:
            interest_rate = 10  

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        score = calculate_credit_score(customer)
        approval = False
        corrected_interest_rate = float(interest_rate)

        # Scoring Logic
        if score > 50:
            approval = True

        elif score > 30:
            approval = True
            corrected_interest_rate = max(corrected_interest_rate, 12)

        elif score > 10:
            approval = True
            corrected_interest_rate = max(corrected_interest_rate, 16)

        else:
            return Response({
                "approval": False,
                "message": "Loan rejected due to low credit score.",
                "credit_score": score
            }, status=400)

        # EMI Formula
        r = corrected_interest_rate / (12 * 100)

        if r == 0:
            return Response({"error": "Invalid interest rate"}, status=400)

        emi = loan_amount * r * (1 + r) ** tenure / ((1 + r) ** tenure - 1)

        return Response({
            "customer_id": customer_id,
            "approval": approval,
            "credit_score": score,
            "interest_rate_sent": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": round(emi, 2)
        }, status=200)



# ---------------------------------------
#      CREATE LOAN
# ---------------------------------------
class CreateLoan(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = request.data.get("loan_amount")
        interest_rate = request.data.get("interest_rate")
        tenure = request.data.get("tenure")

        if customer_id is None or loan_amount is None or tenure is None:
            return Response({"error": "customer_id, loan_amount and tenure are required"},
                            status=400)

        if interest_rate is None:
            interest_rate = 10  # default

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        score = calculate_credit_score(customer)

        # Reject logic
        if score <= 10 or customer.current_debt > customer.approved_limit:
            return Response({
                "loan_approved": False,
                "message": "Loan cannot be approved due to low credit score or high debt."
            }, status=400)

        corrected_interest_rate = float(interest_rate)

        if score > 50:
            pass
        elif score > 30:
            corrected_interest_rate = max(corrected_interest_rate, 12)
        elif score > 10:
            corrected_interest_rate = max(corrected_interest_rate, 16)

        r = corrected_interest_rate / (12 * 100)
        emi = loan_amount * r * (1 + r) ** tenure / ((1 + r) ** tenure - 1)

        # Create Loan
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=corrected_interest_rate,
            monthly_installment=round(emi, 2)
        )

        customer.current_debt += loan_amount
        customer.save()

        return Response({
            "loan_id": loan.id,
            "loan_approved": True,
            "monthly_installment": round(emi, 2),
            "corrected_interest_rate": corrected_interest_rate
        }, status=201)



# ---------------------------------------
#      VIEW SINGLE LOAN
# ---------------------------------------
class ViewLoan(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=404)

        customer = loan.customer

        return Response({
            "loan_id": loan.id,
            "customer": {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "tenure": loan.tenure
        }, status=200)



# ---------------------------------------
#      VIEW LOANS BY CUSTOMER
# ---------------------------------------
class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        loans = Loan.objects.filter(customer_id=customer_id)

        if not loans.exists():
            return Response({"message": "No loans found for this customer"}, status=404)

        loan_list = []
        for loan in loans:
            loan_list.append({
                "loan_id": loan.id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": loan.tenure
            })

        return Response(loan_list, status=200)
