#Activate Iranian National Bank

import requests
from django.contrib import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import NFT, Transaction
import json
from datetime import datetime



class BankMeliPaymentGateway:
    """
    Handles NFT purchases using Bank Melli payment gateway
    """

    def __init__(self):
        self.merchant_id = settings.BANK_MELLI_MERCHANT_ID
        self.terminal_id = settings.BANK_MELLI_TERMINAL_ID
        self.redirect_url = settings.BASE_URL + reverse('payment_verify')
        self.api_url = "https://bankmelli.com/pg/services/rest/"
    

    def generate_payment_request(self, nft_id, user_id, amount):

        """
        Generate payment request to Bank Melli gateway
        """

        nft = NFT.objects.get(pk = nft_id)

        # Create Transaction form

        transaction = Transaction.objects.create(
            nft = nft,
            user_id = user_id,
            amount = amount,
            status = "Pending",
            payment_gateway = 'bank_melli',
        )

        payload = {

            "MerchantID": self.merchant_id,
            "TerminalID": self.terminal_id,
            "Amount": int(amount * 10) # Convert to IRR
            "Amount": int(amount * 10000),  # Convert to IRT
            "OrderID": transaction.id,
            "LocalDateTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "ReturnURL": self.redirect_url,
            "AdditionalData": json.dumps({
            "nft_id": nft_id,
            "user_id": user_id,
        #    "admin_id": admin_id,

            })

        }


        try:
            response = requests.post(f"{self.api_url}request",
            json = payload,
            headers = {'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            data = response.json()
            if data.get('Status')
 

                




def verify_payment(self, authority, amount):

    """
    Verify payment with Bank Melli after user returns from gateway
    """

    try:
        transaction = Transaction.objects.get(bank_reference=authority)

    payload= {
        "MerchantID": self.merchant_id,
        "TerminalID": self.terminal_id,
        "Authority": authority,
        "Amount": int(amount * 10)
    }

    response = requests.post(
        f"{self.api_url}verify",
        json = payload,
        headers = {'Content-Type': 'application/json'}
    )

    response.raise_for_status()

    data = response.json()
    if data.get('Status') == 1:
        #Success 
        transaction.status = 'completed'
        transaction.bank_trace_number = data.get('TraceNumber')
        transaction.save()

        nft = transaction.nft
        nft.owner = transaction.user
        nft.save()

        return{
            'success': True,
            'transaction': transaction,
            'nft': nft,

        }
    raise Exception(data.get('Message', 'Payment verification failed'))

except Exception as e:
    if 'transaction' in locals():
        transaction.status = 'failed'
        transaction.error_message = str(e)
        transaction.save()
    return {'success': False, 'message': str(e)}
