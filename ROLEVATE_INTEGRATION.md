# Rolevate GraphQL Integration

## Overview
The hiring assistant now integrates with Rolevate's GraphQL API, allowing you to:
- Search for jobs on Rolevate
- Browse companies and their job listings
- Check email availability
- Access Rolevate job market data

## Available Endpoints

### Health Check
```bash
GET /api/rolevate/health
```
Check if Rolevate API is available.

**Response:**
```json
{
  "status": "healthy",
  "rolevate": true
}
```

### Get GraphQL Schema
```bash
GET /api/rolevate/schema
```
Get all available queries and mutations in Rolevate's GraphQL API.

**Response:**
```json
{
  "queries": [
    { "name": "health", "description": null },
    { "name": "me", "description": null },
    { "name": "checkEmailExists", "description": null },
    { "name": "checkEmail", "description": null },
    { "name": "file", "description": null },
    { "name": "files", "description": null },
    { "name": "publicFiles", "description": null },
    { "name": "companyById", "description": null },
    { "name": "companyBySlug", "description": null },
    { "name": "allCompanies", "description": null },
    { "name": "companyReviews", "description": null },
    { "name": "job", "description": null },
    { "name": "jobs", "description": null },
    { "name": "searchJobs", "description": null },
    { "name": "jobsByCompany", "description": null },
    { "name": "jobBySlug", "description": null },
    { "name": "myCompanyJobs", "description": null }
  ],
  "mutations": [
    { "name": "register", "description": null },
    { "name": "login", "description": null },
    { "name": "refreshToken", "description": null },
    { "name": "revokeToken", "description": null },
    { "name": "logout", "description": null },
    { "name": "generateApiKey", "description": null },
    { "name": "revokeApiKey", "description": null },
    { "name": "uploadFile", "description": null },
    { "name": "updateFile", "description": null },
    { "name": "deleteFile", "description": null },
    { "name": "restoreFile", "description": null },
    { "name": "presignedUrl", "description": null },
    { "name": "createCompany", "description": null },
    { "name": "updateCompany", "description": null },
    { "name": "deleteCompany", "description": null },
    { "name": "addCompanyReview", "description": null },
    { "name": "createJob", "description": null },
    { "name": "updateJob", "description": null },
    { "name": "deleteJob", "description": null },
    { "name": "publishJob", "description": null },
    { "name": "unpublishJob", "description": null },
    { "name": "toggleJobFavorite", "description": null }
  ]
}
```

### Search Jobs
```bash
GET /api/rolevate/jobs/search?query=engineer&limit=10&offset=0
```
Search for jobs on Rolevate.

**Query Parameters:**
- `query` (required): Search query string (e.g., "engineer", "python developer")
- `limit` (optional): Number of results (1-100, default: 10)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "jobs": [
    {
      "id": "uuid",
      "titleEn": "Senior Software Engineer",
      "descriptionEn": "Job description...",
      "company": { "name": "Company Name" },
      "employmentType": "FULL_TIME",
      "salaryMin": 5000,
      "salaryMax": 8000,
      "locationCity": "Dubai",
      "locationCountry": "UAE"
    }
  ],
  "query": "engineer",
  "limit": 10,
  "offset": 0
}
```

### Get Companies
```bash
GET /api/rolevate/companies?limit=100&offset=0
```
Get all companies from Rolevate.

**Query Parameters:**
- `limit` (optional): Number of results (1-1000, default: 100)
- `offset` (optional): Pagination offset (default: 0)

### Get Company by Slug
```bash
GET /api/rolevate/company/{slug}
```
Get detailed information about a company.

**Parameters:**
- `slug`: Company slug (e.g., "google", "amazon")

**Response includes:**
- Company name, description, logo
- Industry, size, website
- Culture, benefits, and job listings

### Get Company Jobs
```bash
GET /api/rolevate/company/{company_id}/jobs
```
Get all active jobs for a specific company.

**Parameters:**
- `company_id`: Rolevate company ID (UUID)

### Get Job Details
```bash
GET /api/rolevate/job/{job_id}
```
Get detailed information about a specific job.

**Parameters:**
- `job_id`: Rolevate job ID (UUID)

**Response includes:**
- Job title (English and Arabic)
- Description and responsibilities
- Requirements and skills
- Salary, location, employment type
- Application and view counts

### Check Email
```bash
GET /api/rolevate/email/check?email=user@example.com
```
Check if an email exists on Rolevate.

**Query Parameters:**
- `email` (required): Email address to check

**Response:**
```json
{
  "exists": true/false
}
```

## Integration Features

### RolevateGraphQLClient Class
The backend includes a `RolevateGraphQLClient` class that provides:

```python
from integrations.rolevate import RolevateGraphQLClient

client = RolevateGraphQLClient(api_key=None)

# Methods available:
client.search_jobs(query, limit, offset)
client.get_all_companies(limit, offset)
client.get_company_by_slug(slug)
client.get_company_jobs(company_id)
client.get_job_by_id(job_id)
client.check_email_exists(email)
client.get_schema_info()
client.query(graphql_query, variables)  # Raw GraphQL query
```

### Job Format Conversion
Convert our internal job format to Rolevate format:

```python
from integrations.rolevate import format_job_for_rolevate

job_data = format_job_for_rolevate(our_job_post)
```

## Rolevate GraphQL API Structure

### Job Type Fields
The API tracks the following job information:
- **Titles**: titleEn, titleAr
- **Descriptions**: descriptionEn, descriptionAr, shortDescriptionEn, shortDescriptionAr
- **Content**: responsibilitiesEn, responsibilitiesAr, requirementsEn, requirementsAr
- **Skills**: skills array
- **Details**: employmentType, jobLevel, workType, numberOfPositions
- **Location**: locationCity, locationCountry
- **Compensation**: salaryMin, salaryMax, salaryCurrency, salaryPeriod, bonuses, stockOptions
- **Interview**: autoInterviewEnabled, interviewLanguage, interviewPrompt, secondInterviewPrompt
- **Analytics**: viewCount, applicationCount, isFavorite
- **Metadata**: slug, status, deadline, metaDescription
- **User**: createdBy, updatedBy, deletedBy

### Company Type Fields
- **Basic**: name, slug, logo, industry, size
- **Descriptions**: description, descriptionAr, culture, cultureAr
- **Details**: website, email, city, country
- **Social**: linkedin, twitter, instagram, facebook
- **Content**: values, benefits, techStack, faQs, galleryImages
- **Relationships**: jobs (list), users (list), reviews (list)
- **Metadata**: primaryColor, stats, isActive

## Authentication

Currently, the integration works without authentication for public queries. For authenticated operations (creating, updating, publishing jobs), you would need to:

1. Register/Login to get an API token
2. Pass the token in the Authorization header

Example with authentication:
```python
client = RolevateGraphQLClient(api_key="your_api_key_here")
```

## Future Enhancements

1. **Job Publishing**: Add ability to publish generated jobs directly to Rolevate
2. **Authentication**: Integrate Rolevate authentication for job creation/updating
3. **Job Syncing**: Automatically sync jobs between our platform and Rolevate
4. **Analytics**: Track job performance on Rolevate
5. **Arabic Support**: Add Arabic translations for job content
6. **Advanced Search**: Implement faceted search with filters

## Testing

Test endpoints using curl:

```bash
# Check health
curl http://localhost:8000/api/rolevate/health

# Get schema
curl http://localhost:8000/api/rolevate/schema

# Search jobs (requires proper API authentication)
curl "http://localhost:8000/api/rolevate/jobs/search?query=python"

# Check email
curl "http://localhost:8000/api/rolevate/email/check?email=test@example.com"
```

## Error Handling

All endpoints return proper HTTP error codes:
- `200`: Success
- `400`: Bad request or API error
- `404`: Resource not found
- `503`: Rolevate API unavailable

Error responses include details about what went wrong:
```json
{
  "detail": "Error message describing the issue"
}
```
