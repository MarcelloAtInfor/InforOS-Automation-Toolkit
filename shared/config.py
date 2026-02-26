"""
Centralized configuration for Infor tenant and API endpoints.

Provides consistent URL construction across all projects.
Base URL is derived from the .ionapi credentials file (iu field),
not hardcoded.
"""
from .auth import get_credentials


def get_tenant_id():
    """Get tenant ID from credentials."""
    creds = get_credentials()
    return creds['ti']


def get_base_url(service=''):
    """
    Get base URL for Infor API services.

    The base URL is derived from the 'iu' (ION API URL) field in the
    credentials file, making this fully portable across tenants/environments.

    Args:
        service: Service path suffix. Examples:
            - '' (empty): Base tenant URL
            - 'GENAI/coresvc': GenAI Core Service
            - 'GENAI/chatsvc': GenAI Chat Service
            - 'COLEMANDDP/iddpuisvc': IDP Document Processor
            - 'IDM': Infor Document Management
            - 'CSI/IDORequestService/ido': SyteLine IDO operations

    Returns:
        Complete base URL for the service
    """
    creds = get_credentials()
    iu = creds['iu'].rstrip('/')
    ti = creds['ti']
    base = f"{iu}/{ti}"

    if service:
        return f"{base}/{service}"
    return base


# Common service URL factories
def GENAI_CORE_URL():
    """GenAI Core Service URL for tool/agent management."""
    return get_base_url('GENAI/coresvc')


def GENAI_CHAT_URL():
    """GenAI Chat Service URL for agent execution."""
    return get_base_url('GENAI/chatsvc')


def IDP_URL():
    """IDP Document Processor URL."""
    return get_base_url('COLEMANDDP/iddpuisvc')


def get_mongoose_config():
    """SyteLine MongooseConfig header value, derived from tenant ID."""
    return f"{get_tenant_id()}_DALS"


def IDO_URL():
    """SyteLine IDO Request Service URL."""
    return get_base_url('CSI/IDORequestService/ido')
