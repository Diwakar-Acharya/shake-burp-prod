import json
import logging
import boto3
from django.conf import settings

logger = logging.getLogger(__name__)

def send_verification_email_via_lambda(user_email: str, verification_token: str) -> bool:
    """
    Invokes AWS Lambda function to trigger email verification via AWS SES asynchronously.
    """
    try:
        lambda_client = boto3.client('lambda', region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'eu-north-1'))
        payload = {
            "email": user_email,
            "verification_token": verification_token,
            "sender_email": getattr(settings, 'AWS_SES_SENDER_EMAIL', 'noreply@shakeandburp.com'),
        }
        response = lambda_client.invoke(
            FunctionName=getattr(settings, 'AWS_LAMBDA_EMAIL_FUNCTION', 'SendVerificationEmail'),
            InvocationType='Event',  # Asynchronous execution
            Payload=json.dumps(payload)
        )
        logger.info(f"Triggered AWS Lambda email verification for {user_email}, status: {response.get('StatusCode')}")
        return True
    except Exception as e:
        logger.error(f"Failed to invoke AWS Lambda for email verification: {str(e)}")
        return False
