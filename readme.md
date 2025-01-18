# URL Shortener Service

This service provides a simple yet powerful URL shortening functionality, allowing users to create shorter aliases for long URLs. It includes features such as URL expiry and analytics on URL access, making it a comprehensive tool for managing and distributing URLs.

## Features

* **URL Shortening**: Convert long URLs into short, manageable links that are easier to share.
* **Expiry Option**: Set an expiration time for short URLs, after which the links become inactive.
* **Analytics**: Track how many times each short URL has been accessed, along with access logs that include timestamps and IP addresses.
* **Password Protection**: Option to protect short URLs with a password, ensuring that only users with the password can access the original URL.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.8 or higher
* Pip for installing dependencies

### Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory and install the required dependencies:

```bash
pip install -r app/requirements.txt
```

3. Start the application:

```bash
uvicorn app.main:app --reload
```

## Usage

### Creating a Short URL

Send a POST request to `/surl/shorten` with the following JSON payload:

```json
{
  "url": "https://example.com",
  "expiry_hours": 24, // Optional, defaults to 24 hours
  "password": "secret" // Optional, for password protection
}
```

You will receive a response containing the original URL, the short key, and the expiry time.

### Accessing a Short URL

Simply navigate to the short URL provided by the service. If the URL is password-protected, append the password as a query parameter.

```
base_url/shorten/short_key?password
```
When its password protected, it will redirect to the original url.

### Viewing Analytics

Send a GET request to `/surl/analytics/{short_key}` to retrieve access counts and logs for a specific short URL.

## Development

This service uses FastAPI for the web framework, SQLAlchemy for ORM, and SQLite for the database. The codebase is structured as follows:

* **app/main.py**: Entry point of the application, setting up the FastAPI app and routes.
* **app/model/**: Contains SQLAlchemy models for the database tables.
* **app/router/**: Defines the routes for the web service.
* **app/schema/**: Pydantic models for request and response validation.
* **app/util.py**: Utility functions for hashing and key generation.

