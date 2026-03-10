import jwt
from datetime import datetime, timedelta
from app.settings import settings
import structlog

logger = structlog.get_logger()


class MkPlaceJWT:
    """Gerador de JWT para autenticação SSO MkPlace"""
    
    @staticmethod
    def generate_token(customer_id: str, expires_in_days: int = 365) -> str:
        """
        Gera um JWT para autenticação do cliente na MkPlace
        
        Args:
            customer_id: ID externo do cliente
            expires_in_days: Dias até expiração do token (padrão: 365)
        
        Returns:
            Token JWT assinado
        """
        now = datetime.utcnow()
        exp = now + timedelta(days=expires_in_days)
        
        # Roles conforme documentação MkPlace
        roles = [
            "oauth/user/read",
            "oauth/user/token",
            "oauth/user/recover",
            "oauth/user/getAll",
            "oauth/user/delete",
            "oauth/user/update",
            "shopping/offer/read",
            "customer/customer/get",
            "customer/customer/update",
            "customer/customer/delete",
            "customer/shoppingCart/create",
            "customer/shoppingCart/get",
            "customer/shoppingCart/delete",
            "customer/newsletter/create",
            "customer/wishlist/get",
            "customer/wishlist/create",
            "customer/wishlist/delete",
            "sales/order/checkout",
            "sales/order/read",
            "sales/order/write",
            "payment/creditcard/read",
            "payment/creditcard/create",
            "payment/creditcard/delete",
            "payment/creditcard/update",
            "payment/creditcard/get",
            "payment/transaction/read",
            "payment/transaction/create",
            "payment/transaction/timeline",
            "payment/transaction/addPayment",
            "catalog/review/create",
            "catalog/questionanswer/createQuestion",
            "loyalty/campaign/simulate",
            "loyalty/member/read",
            "loyalty/points/read",
            "loyalty/wallet/read",
            "freight/shipping/create",
            "freight/worksheet/read",
            "promotion/promotion/read",
            "subscription/subscription/cancel",
            "subscription/charge/retry",
            "subscription/charge/update",
            f"profile:storeId={settings.mkplace_store_id}",
            f"profile:accountId={settings.mkplace_account_id}",
            f"profile:clientId=client",
            f"profile:customerId={customer_id}"
        ]
        
        payload = {
            "exp": int(exp.timestamp()),
            "iat": int(now.timestamp()),
            "sub": customer_id,
            "typ": "Bearer",
            "azp": settings.mkplace_client_id,
            "realm_access": {
                "roles": roles
            },
            "scope": "email openid profile",
            "email_verified": True,
            "clientId": settings.mkplace_client_id,
            "customerId": customer_id,
            "storeId": settings.mkplace_store_id
        }
        
        headers = {
            "alg": "RS256",
            "typ": "JWT",
            "kid": settings.mkplace_kid
        }
        
        token = jwt.encode(
            payload,
            settings.mkplace_private_key,
            algorithm="RS256",
            headers=headers
        )
        
        logger.info("mkplace_jwt_generated", customer_id=customer_id)
        return token
