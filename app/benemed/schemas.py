from enum import Enum


class BenemedPlan(str, Enum):
    ESSENCIAL = "26d876219db04110881153441ad585d8"
    ESSENCIAL_SAUDE_MENTAL = "720d68006f5f489eb8458d788710b451"


PLAN_DETAILS = {
    BenemedPlan.ESSENCIAL: {
        "description": "Plano Essencial PlugZ",
        "price": "R$ 29,90"
    },
    BenemedPlan.ESSENCIAL_SAUDE_MENTAL: {
        "description": "Plano Essencial PlugZ com saúde mental",
        "price": "R$ 49,90"
    }
}
