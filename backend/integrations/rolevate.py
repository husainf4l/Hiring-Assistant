"""
Rolevate GraphQL Integration
Connects to Rolevate API to publish jobs
"""

import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime


class RolevateGraphQLClient:
    """Client for interacting with Rolevate GraphQL API"""
    
    BASE_URL = "https://rolevate.aqlaan.com/api/graphql"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Rolevate client
        
        Args:
            api_key: Optional API key for authentication
        """
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}"
            })
    
    def query(self, query_str: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query
        
        Args:
            query_str: GraphQL query string
            variables: Variables for the query
        
        Returns:
            Response data from GraphQL API
        """
        payload = {
            "query": query_str,
        }
        if variables:
            payload["variables"] = variables
        
        try:
            response = self.session.post(
                self.BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"errors": [{"message": str(e)}]}
    
    def search_jobs(self, query: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        Search for jobs on Rolevate
        
        Args:
            query: Search query string
            limit: Number of results
            offset: Offset for pagination
        
        Returns:
            Job search results
        """
        graphql_query = """
            query SearchJobs($filter: JobFilterInput!) {
                searchJobs(filter: $filter) {
                    id
                    titleEn
                    titleAr
                    descriptionEn
                    descriptionAr
                    employmentType
                    salaryMin
                    salaryMax
                    salaryCurrency
                    locationCity
                    locationCountry
                    jobLevel
                    viewCount
                    applicationCount
                }
            }
        """
        
        variables = {
            "filter": {
                "search": query,
                "skip": offset,
                "take": limit
            }
        }
        
        result = self.query(graphql_query, variables)
        jobs = result.get("data", {}).get("searchJobs", [])
        return {"jobs": jobs, "query": query, "limit": limit, "offset": offset}
    
    def get_all_companies(self, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        Get all companies from Rolevate
        
        Args:
            limit: Number of results (limit is ignored, API returns all)
            offset: Offset for pagination (offset is ignored, API returns all)
        
        Returns:
            List of companies
        """
        graphql_query = """
            query GetAllCompanies {
                allCompanies {
                    id
                    name
                    slug
                    logo
                    industry
                    description
                    descriptionAr
                    city
                    country
                    size
                    website
                    email
                }
            }
        """
        
        result = self.query(graphql_query)
        companies = result.get("data", {}).get("allCompanies", [])
        return {"companies": companies}
    
    def get_company_by_slug(self, slug: str) -> Dict[str, Any]:
        """
        Get company details by slug
        
        Args:
            slug: Company slug
        
        Returns:
            Company details
        """
        graphql_query = """
            query GetCompanyBySlug($slug: String!) {
                companyBySlug(slug: $slug) {
                    id
                    name
                    description
                    descriptionAr
                    logo
                    industry
                    size
                    website
                    culture
                    benefits
                    jobs {
                        id
                        titleEn
                        status
                    }
                }
            }
        """
        
        variables = {"slug": slug}
        return self.query(graphql_query, variables)
    
    def get_company_jobs(self, company_id: str) -> Dict[str, Any]:
        """
        Get all jobs for a company
        
        Args:
            company_id: Company ID
        
        Returns:
            List of company jobs
        """
        graphql_query = """
            query GetCompanyJobs($companyId: ID!) {
                jobsByCompany(companyId: $companyId) {
                    id
                    titleEn
                    titleAr
                    descriptionEn
                    descriptionAr
                    employmentType
                    salaryMin
                    salaryMax
                    locationCity
                    status
                    applicationCount
                    viewCount
                }
            }
        """
        
        variables = {"companyId": company_id}
        return self.query(graphql_query, variables)
    
    def get_job_by_id(self, job_id: str) -> Dict[str, Any]:
        """
        Get job details by ID
        
        Args:
            job_id: Job ID
        
        Returns:
            Job details
        """
        graphql_query = """
            query GetJob($id: ID!) {
                job(id: $id) {
                    id
                    titleEn
                    titleAr
                    descriptionEn
                    descriptionAr
                    responsibilitiesEn
                    responsibilitiesAr
                    requirementsEn
                    requirementsAr
                    skills
                    employmentType
                    jobLevel
                    salaryMin
                    salaryMax
                    salaryCurrency
                    locationCity
                    locationCountry
                    workType
                    applicationCount
                    viewCount
                }
            }
        """
        
        variables = {"id": job_id}
        return self.query(graphql_query, variables)
    
    def check_email_exists(self, email: str) -> Dict[str, Any]:
        """
        Check if email exists on Rolevate
        
        Args:
            email: Email address
        
        Returns:
            Email existence check result
        """
        graphql_query = """
            query CheckEmailExists($email: String!) {
                checkEmailExists(email: $email)
            }
        """
        
        variables = {"email": email}
        return self.query(graphql_query, variables)
    
    def get_health(self) -> Dict[str, Any]:
        """
        Check health of Rolevate API
        
        Returns:
            Health status
        """
        graphql_query = """
            query {
                health
            }
        """
        
        return self.query(graphql_query)
    
    def create_job(self, company_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new job on Rolevate (requires authentication)
        
        Args:
            company_id: Company ID
            job_data: Job data to create
        
        Returns:
            Created job details
        """
        graphql_mutation = """
            mutation CreateJob($companyId: UUID!, $data: CreateJobInput!) {
                createJob(companyId: $companyId, data: $data) {
                    id
                    titleEn
                    titleAr
                    status
                    createdAt
                }
            }
        """
        
        variables = {
            "companyId": company_id,
            "data": job_data
        }
        
        return self.query(graphql_mutation, variables)
    
    def update_job(self, job_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing job on Rolevate (requires authentication)
        
        Args:
            job_id: Job ID
            job_data: Job data to update
        
        Returns:
            Updated job details
        """
        graphql_mutation = """
            mutation UpdateJob($id: UUID!, $data: UpdateJobInput!) {
                updateJob(id: $id, data: $data) {
                    id
                    titleEn
                    titleAr
                    status
                    updatedAt
                }
            }
        """
        
        variables = {
            "id": job_id,
            "data": job_data
        }
        
        return self.query(graphql_mutation, variables)
    
    def publish_job(self, job_id: str) -> Dict[str, Any]:
        """
        Publish a job on Rolevate (requires authentication)
        
        Args:
            job_id: Job ID
        
        Returns:
            Published job details
        """
        graphql_mutation = """
            mutation PublishJob($id: UUID!) {
                publishJob(id: $id) {
                    id
                    status
                    updatedAt
                }
            }
        """
        
        variables = {"id": job_id}
        return self.query(graphql_mutation, variables)
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Get GraphQL schema information (queries and mutations available)
        
        Returns:
            Schema info including all queries and mutations
        """
        graphql_query = """
            {
                __schema {
                    queryType { 
                        fields { 
                            name 
                            description
                        } 
                    }
                    mutationType { 
                        fields { 
                            name 
                            description
                        } 
                    }
                }
            }
        """
        
        return self.query(graphql_query)


# Helper function to format job data for Rolevate API
def format_job_for_rolevate(job_post: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert our internal JobPost format to Rolevate API format
    
    Args:
        job_post: Our internal job post format
    
    Returns:
        Job data formatted for Rolevate API
    """
    return {
        "titleEn": job_post.get("title", ""),
        "titleAr": job_post.get("title", ""),  # TODO: Add Arabic translation
        "descriptionEn": job_post.get("summary", ""),
        "descriptionAr": job_post.get("summary", ""),  # TODO: Add Arabic translation
        "responsibilitiesEn": "\n".join(job_post.get("responsibilities", [])),
        "responsibilitiesAr": "\n".join(job_post.get("responsibilities", [])),  # TODO: Add Arabic translation
        "requirementsEn": "\n".join(job_post.get("requirements", [])),
        "requirementsAr": "\n".join(job_post.get("requirements", [])),  # TODO: Add Arabic translation
        "skills": job_post.get("skills", []),
        "employmentType": job_post.get("job_type", "FULL_TIME"),
        "jobLevel": job_post.get("seniority_level", "MID"),
        "locationCity": job_post.get("location", "").split(",")[0] if job_post.get("location") else "",
        "locationCountry": job_post.get("location", "").split(",")[-1].strip() if job_post.get("location") else "",
        "workType": job_post.get("workplace_type", "ON_SITE"),
    }
