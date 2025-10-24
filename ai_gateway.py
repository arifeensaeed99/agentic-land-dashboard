from __future__ import annotations
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

class DeereAIGatewayOpenAI(OpenAI):


    def __init__(
        self,
        access_token: str,
        base_url: str,
        deere_ai_gateway_registration_id: Optional[str] = None
    ):
        base_url = (
            base_url + "openai/" if base_url.endswith("/") else base_url + "/openai/"
        )

        headers = {"Authorization": f"Bearer {access_token}"}
        if deere_ai_gateway_registration_id is not None:
            headers["deere-ai-gateway-registration-id"] = deere_ai_gateway_registration_id

        super(DeereAIGatewayOpenAI, self).__init__(
            # This is required to pass validations in the parent class
            api_key="sk-000000000000000000000000000000000000000000000000",
            base_url=base_url,
            default_headers=headers,
        )