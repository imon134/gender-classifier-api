# Gender Classification API

## Overview
This is a simple REST API that classifies a person's gender based on their name using the **Genderize API**.  
It processes the raw API response and returns structured, enhanced data including confidence scoring and timestamps.

---

## Live API

Base URL: https://gender-classifier-api-six.vercel.app

## Endpoint

### GET `/api/classify`

Returns gender prediction for a given name.

---

## Query Parameters

| Parameter | Type   | Required | Description        |
|----------|--------|----------|--------------------|
| name     | string | Yes      | Name to classify   |

---

## Example Request
GET /api/classify?name=John


Full example: https://gender-classifier-api-six.vercel.app/?name=John
---

## Success Response

```json
{
  "status": "success",
  "data": {
    "name": "John",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-14T12:00:00Z"
  }
}
```
---

## Error Responses
### Bad Request — Missing or empty name

```json
{
  "status": "error",
  "message": "Name query parameter is required"
}
```
### Unprocessable Entity — Invalid input type

```json
{
  "status": "error",
  "message": "Name must be a string"
}
```
### OK — No Prediction Available

```json
{
  "status": "error",
  "message": "No prediction available for the provided name"
}
```
### Bad Gateway — External API failure

```json
{
  "status": "error",
  "message": "Failed to fetch data from Genderize API"
}
```
