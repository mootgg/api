# Moot API Docs

## Authentication

To authenticate with the API you need an API token (obtained from https://moot.gg/developers). For each API request this token should be sent in the `Authorization` header of the request.

Example request:
```
POST /moots HTTP/1.1
Authorization: 1cefabc6
Content-Type: application/json

{
    "content": "Your Moot content..."
}
```

Non authenticated requests will be immediately rejected by the API with response code 401, unless explicitly stated that the endpoint doesn't need authentication on this page.

## Ratelimiting

Unless explicitly stated otherwise on this page, all endpoints are ratelimited to prevent abuse of the API. Ratelimits are dynamic and are not guaranteed to remain the same, so inspecting response headers is important to make sure you don't get ratelimited. If you do get ratelimited the API will respond with a response code of 429, and a JSON object like this:

```json
{
    "global": true,
    "retry_after": 60000
}
```

| Field       | Type    | Description                                               |
|-------------|---------|-----------------------------------------------------------|
| global      | boolean | Whether the ratelimit is global.                          |
| retry_after | integer | How many milliseconds until you should retry the request. |

## Endpoints

The base URL for all API endpoints is `https://api.moot.gg`. The current API version is `v1`. All routes detailed below expect the base URL and the version to be prepended: `https://api.moot.gg/v1`

### `POST /moots`

Create a new Moot.

Returns: Moot

Schema:

| Field   | Type    | Description                           |
|---------|---------|---------------------------------------|
| content | string  | The content of the Moot.              |

### `GET /moots/{moot_id}`

Get a Moot based on its ID.

Returns: Moot

### `DELETE /moots/{moot_id}`

Delete a Moot.

Returns: Moot

## Objects

### Moot

| Field   | Type    | Description                           |
|---------|---------|---------------------------------------|
| id      | integer | The ID of the Moot.                   |
| content | string  | The content of the Moot.              |
| hidden  | boolean | Whether the Moot is marked as hidden. |
| flags   | integer | Bit flags for the Moot. (Values TBD)  |
| author  | User    | The author of the Moot.               |

### User

| Field    | Type    | Description                          |
|----------|---------|--------------------------------------|
| id       | integer | The user's unique ID.                |
| username | string  | The user's name.                     |
| avatar   | string  | The user's avatar hash.              |
| flags    | integer | Bit flags for the User. (Values TBD) |
