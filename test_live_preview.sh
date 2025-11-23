#!/bin/bash

# Test Live Preview Functionality
echo "🧪 Testing Live Preview Updates"
echo "================================="

# Start chat
echo "1. Starting chat session..."
START_RESPONSE=$(curl -s -X POST http://localhost:8000/api/start-chat -H "Content-Type: application/json" -d '{}')
SESSION_ID=$(echo $START_RESPONSE | jq -r '.session_id')
echo "   Session ID: $SESSION_ID"

# Check initial preview (should be empty)
echo "2. Checking initial preview..."
PREVIEW_RESPONSE=$(curl -s http://localhost:8000/api/post-preview/$SESSION_ID)
echo "   Initial preview job_post: $(echo $PREVIEW_RESPONSE | jq '.job_post')"

# Send job title
echo "3. Sending job title: 'Senior Software Engineer'..."
MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/send-message -H "Content-Type: application/json" -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Senior Software Engineer\"}")
echo "   AI Response: $(echo $MESSAGE_RESPONSE | jq -r '.response' | head -c 50)..."

# Check preview after job title
echo "4. Checking preview after job title..."
sleep 1
PREVIEW_RESPONSE=$(curl -s http://localhost:8000/api/post-preview/$SESSION_ID)
TITLE=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.title')
echo "   Job title in preview: '$TITLE'"

# Send company name
echo "5. Sending company: 'TechCorp Inc'..."
MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/send-message -H "Content-Type: application/json" -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"TechCorp Inc\"}")
echo "   AI Response: $(echo $MESSAGE_RESPONSE | jq -r '.response' | head -c 50)..."

# Check preview after company
echo "6. Checking preview after company..."
sleep 1
PREVIEW_RESPONSE=$(curl -s http://localhost:8000/api/post-preview/$SESSION_ID)
TITLE=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.title')
COMPANY=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.company')
echo "   Title: '$TITLE', Company: '$COMPANY'"

# Send location and type
echo "7. Sending location and type: 'Remote, Full-time'..."
MESSAGE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/send-message -H "Content-Type: application/json" -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Remote, Full-time\"}")
echo "   AI Response: $(echo $MESSAGE_RESPONSE | jq -r '.response' | head -c 50)..."

# Check preview after location/type
echo "8. Checking preview after location/type..."
sleep 1
PREVIEW_RESPONSE=$(curl -s http://localhost:8000/api/post-preview/$SESSION_ID)
TITLE=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.title')
COMPANY=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.company')
LOCATION=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.location')
JOB_TYPE=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.job_type')
WORKPLACE_TYPE=$(echo $PREVIEW_RESPONSE | jq -r '.job_post.workplace_type')
echo "   Title: '$TITLE'"
echo "   Company: '$COMPANY'"
echo "   Location: '$LOCATION'"
echo "   Job Type: '$JOB_TYPE'"
echo "   Workplace Type: '$WORKPLACE_TYPE'"

echo ""
echo "✅ Live Preview Test Complete!"
echo "================================="
echo "The preview should update live as the user answers questions."