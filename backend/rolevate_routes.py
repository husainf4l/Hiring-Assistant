"""
Rolevate Integration Routes
Exposes endpoints for searching and publishing jobs on Rolevate
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from integrations.rolevate import RolevateGraphQLClient, format_job_for_rolevate
except ImportError:
    from rolevate import RolevateGraphQLClient, format_job_for_rolevate

router = APIRouter()

# Initialize Rolevate client
rolevate_client = RolevateGraphQLClient()


@router.get("/rolevate/health")
async def check_rolevate_health():
    """Check health of Rolevate API"""
    result = rolevate_client.get_health()
    
    if "errors" in result:
        raise HTTPException(
            status_code=503,
            detail=f"Rolevate API error: {result['errors'][0]['message']}"
        )
    
    return {
        "status": "healthy" if result.get("data", {}).get("health") else "unhealthy",
        "rolevate": True
    }


@router.get("/rolevate/companies")
async def get_rolevate_companies(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    """
    Get all companies from Rolevate
    
    Args:
        limit: Number of companies to return (max 1000)
        offset: Pagination offset
    """
    result = rolevate_client.get_all_companies(limit=limit, offset=offset)
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching companies: {result['errors'][0]['message']}"
        )
    
    return {
        "companies": result.get("companies", []),
        "limit": limit,
        "offset": offset
    }


@router.get("/rolevate/company/{slug}")
async def get_rolevate_company(slug: str):
    """
    Get company details from Rolevate by slug
    
    Args:
        slug: Company slug
    """
    result = rolevate_client.get_company_by_slug(slug)
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching company: {result['errors'][0]['message']}"
        )
    
    company = result.get("data", {}).get("companyBySlug")
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company


@router.get("/rolevate/jobs/search")
async def search_rolevate_jobs(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Search for jobs on Rolevate
    
    Args:
        query: Search query
        limit: Number of results
        offset: Pagination offset
    """
    result = rolevate_client.search_jobs(query=query, limit=limit, offset=offset)
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error searching jobs: {result['errors'][0]['message']}"
        )
    
    return {
        "jobs": result.get("jobs", []),
        "query": query,
        "limit": limit,
        "offset": offset
    }


@router.get("/rolevate/company/{company_id}/jobs")
async def get_company_rolevate_jobs(company_id: str):
    """
    Get all jobs for a company on Rolevate
    
    Args:
        company_id: Rolevate company ID (UUID)
    """
    result = rolevate_client.get_company_jobs(company_id)
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching company jobs: {result['errors'][0]['message']}"
        )
    
    return {
        "company_id": company_id,
        "jobs": result.get("data", {}).get("jobsByCompany", [])
    }


@router.get("/rolevate/job/{job_id}")
async def get_rolevate_job(job_id: str):
    """
    Get job details from Rolevate
    
    Args:
        job_id: Rolevate job ID (UUID)
    """
    result = rolevate_client.get_job_by_id(job_id)
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching job: {result['errors'][0]['message']}"
        )
    
    job = result.get("data", {}).get("job")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.get("/rolevate/email/check")
async def check_email_on_rolevate(email: str = Query(..., min_length=5)):
    """
    Check if email exists on Rolevate
    
    Args:
        email: Email address to check
    """
    result = rolevate_client.check_email_exists(email)
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error checking email: {result['errors'][0]['message']}"
        )
    
    return result.get("data", {}).get("checkEmailExists", {})


@router.get("/rolevate/schema")
async def get_rolevate_schema():
    """
    Get GraphQL schema information from Rolevate
    Shows all available queries and mutations
    """
    result = rolevate_client.get_schema_info()
    
    if "errors" in result:
        raise HTTPException(
            status_code=400,
            detail=f"Error fetching schema: {result['errors'][0]['message']}"
        )
    
    schema = result.get("data", {}).get("__schema", {})
    return {
        "queries": schema.get("queryType", {}).get("fields", []),
        "mutations": schema.get("mutationType", {}).get("fields", [])
    }
