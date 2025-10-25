from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customers.models import Customer
from .services.eligibility import calculate_credit_score
import math

class CheckEligibility(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = request.data.get("loan_amount")
        interest_rate = request.data.get("interest_rate")
        tenure = request.data.get("tenure")

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        score = calculate_credit_score(customer)
        approval = False
        corrected_interest_rate = interest_rate

        # Scoring logic
        if score > 50:
            approval = True
        elif score > 30:
            approval = True
            corrected_interest_rate = max(interest_rate, 12)
        elif score > 10:
            approval = True
            corrected_interest_rate = max(interest_rate, 16)

        # EMI formula
        r = corrected_interest_rate / (12 * 100)
        emi = loan_amount * r * (1 + r) ** tenure / ((1 + r) ** tenure - 1)

        return Response({
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": round(emi, 2)
        }, status=status.HTTP_200_OK)
    
from .models import Loan

class CreateLoan(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = request.data.get("loan_amount")
        interest_rate = request.data.get("interest_rate")
        tenure = request.data.get("tenure")

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=404)

        # ✅ Step 1: Credit score check (using your existing function)
        from .services.eligibility import calculate_credit_score
        score = calculate_credit_score(customer)

        # Eligibility logic same as check-eligibility
        if score <= 10 or customer.current_debt > customer.approved_limit:
            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Loan cannot be approved due to low credit score or high debt."
            }, status=status.HTTP_400_BAD_REQUEST)

        corrected_interest_rate = interest_rate
        if score > 50:
            corrected_interest_rate = interest_rate
        elif score > 30:
            corrected_interest_rate = max(interest_rate, 12)
        elif score > 10:
            corrected_interest_rate = max(interest_rate, 16)

        # ✅ Step 2: Calculate EMI (compound interest)
        r = corrected_interest_rate / (12 * 100)
        emi = loan_amount * r * (1 + r) ** tenure / ((1 + r) ** tenure - 1)

        # ✅ Step 3: Save loan in DB
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=corrected_interest_rate,
            monthly_installment=round(emi, 2)
        )

        # ✅ Step 4: Update customer’s debt
        customer.current_debt += loan_amount
        customer.save()

        # ✅ Step 5: Return response
        return Response({
            "loan_id": loan.id,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan approved successfully.",
            "monthly_installment": round(emi, 2)
        }, status=status.HTTP_201_CREATED)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from customers.models import Customer

class ViewLoan(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id)
            customer = Customer.objects.get(id=loan.customer_id)

            loan_data = {
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
            }

            return Response(loan_data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ViewLoansByCustomer(APIView):
    def get(self, request, customer_id):
        loans = Loan.objects.filter(customer_id=customer_id)
        if not loans.exists():
            return Response({"message": "No loans found for this customer"}, status=status.HTTP_404_NOT_FOUND)

        loan_list = []
        for loan in loans:
            repayments_left = loan.tenure  # for now assume tenure = total months left (you can update later)
            loan_list.append({
                "loan_id": loan.id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": repayments_left
            })

        return Response(loan_list, status=status.HTTP_200_OK)



