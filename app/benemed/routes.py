from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from app.settings import settings
from app.benemed.schemas import BenemedPlan

router = APIRouter(prefix="/benemed", tags=["Benemed"])


@router.get("/checkout")
async def checkout_redirect(plan_id: str = Query(..., description="ID do plano Benemed")):
    """
    Redireciona para o checkout da Benemed com o plano selecionado.
    Ambiente (hml/prod) controlado pela variável BENEMED_ENV.
    """
    # Valida se o plano existe
    try:
        plan = BenemedPlan(plan_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Plano inválido. Planos válidos: {[p.value for p in BenemedPlan]}"
        )

    # Define URL base conforme ambiente
    base_url = (
        "https://hml.benemedsaude.com.br"
        if settings.benemed_env == "hml"
        else "https://benemedsaude.com.br"
    )

    # Monta URL de checkout
    checkout_url = (
        f"{base_url}/checkout"
        f"?id_plan={plan.value}"
        f"&type=Individual"
        f"&id_parceiro={settings.benemed_partner_id}"
    )

    return RedirectResponse(url=checkout_url, status_code=302)
