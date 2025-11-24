# 📡 API Documentation

Complete reference for all API endpoints of the HR Hiring Assistant.

---

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently: None (placeholder user_id = 1)

Future: JWT token in Authorization header

---

## Endpoints

### 1. Start Chat

Initialize a new chat session for creating a job post.

```
POST /start-chat
```

#### Request

```bash
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

**Request Body**:
```json
{
  "user_id": 1
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (currently 1) |

#### Response

**Status**: `200 OK`

```json
{
  "session_id": 1,
  "first_message": "Hello! I'm here to help you create a compelling job posting. Let's start with the basics.\n\nWhat is the job title for the position you're hiring for?",
  "status": "success"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `session_id` | integer | Unique chat session ID |
| `first_message` | string | Initial question from AI |
| `status` | string | "success" or "error" |

#### Example Response
```json
{
  "session_id": 1,
  "first_message": "What is the job title?",
  "status": "success"
}
```

#### Backend Process
1. Creates new `ChatSession` record
2. Initializes Interview Agent
3. Generates first question
4. Returns session ID and question

---

### 2. Send Message

Send user message and get AI response with live preview update.

```
POST /send-message
```

#### Request

```bash
curl -X POST http://localhost:8000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "user_message": "Senior Full-Stack Engineer"
  }'
```

**Request Body**:
```json
{
  "session_id": 1,
  "user_message": "Senior Full-Stack Engineer"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | integer | Yes | Chat session ID |
| `user_message` | string | Yes | User's response |

#### Response

**Status**: `200 OK`

```json
{
  "ai_response": "Great! That's a solid position. Now, how many years of experience are you looking for in this role?",
  "preview": {
    "job_title": "Senior Full-Stack Engineer",
    "company": "",
    "summary": "",
    "responsibilities": [],
    "requirements": [],
    "nice_to_haves": [],
    "salary_range": ""
  },
  "chat_complete": false,
  "message_count": 2,
  "status": "success"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `ai_response` | string | Next question or completion message |
| `preview` | object | Current job post state |
| `chat_complete` | boolean | Is chat finished? |
| `message_count` | integer | Total messages in session |
| `status` | string | "success" or "error" |

#### Preview Object Structure

```json
{
  "job_title": "Senior Full-Stack Engineer",
  "company": "TechCorp",
  "summary": "We are looking for...",
  "responsibilities": [
    "Build and maintain scalable APIs",
    "Lead technical projects",
    "Mentor junior developers"
  ],
  "requirements": [
    "5+ years of experience",
    "Strong in Python and React",
    "Experience with PostgreSQL"
  ],
  "nice_to_haves": [
    "Experience with Kubernetes",
    "Published technical blog"
  ],
  "salary_range": "$120,000 - $150,000"
}
```

#### Backend Process
1. Stores user message in ChatSession
2. Interview Agent processes answer
3. Composer Agent generates content
4. Formatter Agent polishes output
5. Updates preview
6. Returns response

---

### 3. Get Posts

Retrieve all saved job posts for the user.

```
GET /posts
```

#### Request

```bash
curl -X GET http://localhost:8000/api/posts \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Query Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | integer | No | Filter by user (default: 1) |
| `skip` | integer | No | Pagination skip (default: 0) |
| `limit` | integer | No | Pagination limit (default: 50) |

#### Response

**Status**: `200 OK`

```json
{
  "posts": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Senior Full-Stack Engineer",
      "company": "TechCorp",
      "summary": "We are looking for a talented...",
      "responsibilities": ["Build APIs", "Lead projects"],
      "requirements": ["5+ years experience"],
      "nice_to_haves": ["Kubernetes experience"],
      "salary_range": "$120k-$150k",
      "created_at": "2025-11-24T10:30:00",
      "updated_at": "2025-11-24T10:30:00"
    }
  ],
  "count": 1,
  "status": "success"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `posts` | array | Array of job posts |
| `count` | integer | Total number of posts |
| `status` | string | "success" or "error" |

#### Post Object Structure

```json
{
  "id": 1,
  "user_id": 1,
  "chat_session_id": 1,
  "title": "Senior Full-Stack Engineer",
  "company": "TechCorp",
  "summary": "Job summary text...",
  "responsibilities": "[\"Task 1\", \"Task 2\"]",
  "requirements": "[\"Requirement 1\"]",
  "nice_to_haves": "[\"Nice to have 1\"]",
  "salary_range": "$120k-$150k",
  "created_at": "2025-11-24T10:30:00",
  "updated_at": "2025-11-24T10:30:00"
}
```

---

### 4. Save Post

Save the current job post to the database.

```
POST /save-post
```

#### Request

```bash
curl -X POST http://localhost:8000/api/save-post \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "post_data": {
      "title": "Senior Full-Stack Engineer",
      "company": "TechCorp",
      "summary": "...",
      "responsibilities": ["Build APIs"],
      "requirements": ["5+ years"],
      "nice_to_haves": [],
      "salary_range": "$120k-$150k"
    }
  }'
```

**Request Body**:
```json
{
  "session_id": 1,
  "post_data": {
    "title": "string",
    "company": "string",
    "summary": "string",
    "responsibilities": ["string"],
    "requirements": ["string"],
    "nice_to_haves": ["string"],
    "salary_range": "string"
  }
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | integer | Yes | Chat session ID |
| `post_data` | object | Yes | Complete post data |
| `post_data.title` | string | Yes | Job title |
| `post_data.company` | string | No | Company name |
| `post_data.summary` | string | No | Job summary |
| `post_data.responsibilities` | array | No | List of responsibilities |
| `post_data.requirements` | array | No | Required qualifications |
| `post_data.nice_to_haves` | array | No | Optional qualifications |
| `post_data.salary_range` | string | No | Salary information |

#### Response

**Status**: `200 OK`

```json
{
  "post_id": 1,
  "message": "Job post saved successfully!",
  "success": true,
  "status": "success"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `post_id` | integer | Saved post ID |
| `message` | string | Success message |
| `success` | boolean | Whether save succeeded |
| `status` | string | "success" or "error" |

#### Backend Process
1. Extracts post data
2. Creates JobPost record
3. Links to ChatSession
4. Saves to database
5. Returns post_id

---

### 5. Get Post Preview

Get live preview of the current job post being created.

```
POST /post-preview
```

#### Request

```bash
curl -X POST http://localhost:8000/api/post-preview \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1
  }'
```

**Request Body**:
```json
{
  "session_id": 1
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | integer | Yes | Chat session ID |

#### Response

**Status**: `200 OK`

```json
{
  "preview": {
    "job_title": "Senior Full-Stack Engineer",
    "company": "TechCorp",
    "summary": "We are looking for a talented...",
    "responsibilities": ["Build APIs", "Lead projects"],
    "requirements": ["5+ years experience"],
    "nice_to_haves": ["Kubernetes experience"],
    "salary_range": "$120k-$150k"
  },
  "status": "success"
}
```

#### Backend Process
1. Retrieves ChatSession
2. Extracts accumulated data
3. Generates current preview
4. Returns formatted preview

---

### 6. Regenerate Section

Regenerate a specific section of the job post.

```
POST /regenerate
```

#### Request

```bash
curl -X POST http://localhost:8000/api/regenerate \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "section": "responsibilities"
  }'
```

**Request Body**:
```json
{
  "session_id": 1,
  "section": "responsibilities"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | integer | Yes | Chat session ID |
| `section` | string | Yes | Section to regenerate (see below) |

**Valid Sections**:
- `summary` - Job summary
- `responsibilities` - List of responsibilities
- `requirements` - Required qualifications
- `nice_to_haves` - Nice to have skills
- `full` - Entire post

#### Response

**Status**: `200 OK`

```json
{
  "section": "responsibilities",
  "content": [
    "Build and maintain scalable backend APIs",
    "Design and implement database schemas",
    "Mentor junior developers",
    "Participate in code reviews"
  ],
  "status": "success"
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `section` | string | Section that was regenerated |
| `content` | string/array | New generated content |
| `status` | string | "success" or "error" |

#### Backend Process
1. Retrieves ChatSession data
2. Calls appropriate Agent
3. Regenerates section
4. Updates preview
5. Returns new content

---

## Error Responses

### Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong",
  "status": "error",
  "status_code": 400
}
```

### Common Errors

#### 400 Bad Request
```json
{
  "detail": "Missing required field: user_id",
  "status": "error",
  "status_code": 400
}
```

#### 404 Not Found
```json
{
  "detail": "Chat session not found",
  "status": "error",
  "status_code": 404
}
```

#### 500 Internal Server Error
```json
{
  "detail": "OpenAI API error: rate limit exceeded",
  "status": "error",
  "status_code": 500
}
```

### Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check your request format |
| 401 | Unauthorized | Add valid authentication |
| 404 | Not Found | Check session/post ID |
| 429 | Rate Limited | Wait before retrying |
| 500 | Server Error | Check backend logs |
| 503 | Service Unavailable | Backend is down |

---

## Request/Response Examples

### Example 1: Complete Flow

**Step 1: Start Chat**
```bash
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

Response: `session_id: 1`

**Step 2: Send First Message**
```bash
curl -X POST http://localhost:8000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "user_message": "Senior Full-Stack Engineer"
  }'
```

Response: Next question + preview update

**Step 3: Continue Conversation**
```bash
# Repeat send-message with different answers
```

**Step 4: Save Post**
```bash
curl -X POST http://localhost:8000/api/save-post \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "post_data": {...}
  }'
```

Response: `post_id: 1`

**Step 5: View All Posts**
```bash
curl -X GET http://localhost:8000/api/posts
```

Response: Array of all posts

---

## Rate Limiting

Currently: No rate limiting

Future:
- 100 requests per minute per user
- 10 post creations per day per user
- 1000 preview requests per hour per user

---

## Pagination

For endpoints returning arrays:

```bash
curl -X GET 'http://localhost:8000/api/posts?skip=0&limit=10'
```

Parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 50, max: 100)

Response includes:
```json
{
  "items": [...],
  "total": 50,
  "skip": 0,
  "limit": 10
}
```

---

## Data Types

### String
```json
"field": "value"
```

### Integer
```json
"field": 123
```

### Boolean
```json
"field": true
```

### Array
```json
"field": ["item1", "item2", "item3"]
```

### Object
```json
"field": {
  "nested_field": "value"
}
```

### Datetime (ISO 8601)
```json
"created_at": "2025-11-24T10:30:00"
```

---

## Headers

### Required
```
Content-Type: application/json
```

### Optional (Future)
```
Authorization: Bearer <JWT_TOKEN>
User-Agent: YourApp/1.0
Accept-Language: en-US
```

---

## CORS

Currently Enabled for:
```
- http://localhost:3000
- http://localhost:8000
```

Production: Configure for your domain

---

## Health Check

Check if backend is running:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

## WebSocket (Future)

For real-time updates:

```
wss://localhost:8000/ws/chat/{session_id}
```

Currently: Polling only

---

## Testing Endpoints

### Using cURL

```bash
# Test health
curl http://localhost:8000/health

# Start chat
curl -X POST http://localhost:8000/api/start-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'

# Get posts
curl http://localhost:8000/api/posts
```

### Using Python

```python
import requests

# Start chat
response = requests.post(
    'http://localhost:8000/api/start-chat',
    json={'user_id': 1}
)
print(response.json())

# Send message
response = requests.post(
    'http://localhost:8000/api/send-message',
    json={
        'session_id': 1,
        'user_message': 'Senior Engineer'
    }
)
print(response.json())

# Get posts
response = requests.get('http://localhost:8000/api/posts')
print(response.json())
```

### Using JavaScript

```javascript
// Start chat
const response = await fetch('http://localhost:8000/api/start-chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: 1 })
});
const data = await response.json();
console.log(data);

// Send message
const response2 = await fetch('http://localhost:8000/api/send-message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: 1,
    user_message: 'Senior Engineer'
  })
});
const data2 = await response2.json();
console.log(data2);

// Get posts
const response3 = await fetch('http://localhost:8000/api/posts');
const data3 = await response3.json();
console.log(data3);
```

---

## Changelog

### v1.0.0 (Current)
- ✅ Basic endpoints (start-chat, send-message)
- ✅ Save and retrieve posts
- ✅ Live preview
- ✅ Section regeneration

### v1.1.0 (Planned)
- 📋 Authentication (JWT)
- 📋 Rate limiting
- 📋 WebSocket support
- 📋 Advanced filtering

### v2.0.0 (Future)
- 🔮 Export to PDF
- 🔮 Email integration
- 🔮 Multiple templates
- 🔮 Analytics

---

## Support

For API issues:
1. Check this documentation
2. Review the [Architecture](./ARCHITECTURE.md)
3. Check [TROUBLESHOOTING.md](./guides/TROUBLESHOOTING.md)
4. Review backend logs

---

**Last Updated**: November 24, 2025 | **Status**: ✅ Complete
