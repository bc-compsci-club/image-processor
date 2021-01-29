# Image Processor

A serverless Google Cloud Function that resizes and optimizes an image stored on a Google Cloud Storage bucket. Built with Python and Flask.

## Getting Started

To deploy to Google Cloud Functions, [refer to the official Google Cloud documentation](https://cloud.google.com/functions/docs/deploying) and choose your preferred method of deployment.

The entry point for the Cloud Function is `process`.

You will need to set the following environment variables:

### Build Environment Variables

- **GOOGLE_FUNCTION_SOURCE**: `src/main.py`

### Runtime Environment Variables

- **GOOGLE_CLOUD_STORAGE_BUCKET**: The Google Cloud Storage bucket to use.
