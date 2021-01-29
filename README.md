# Image Processor

A serverless Google Cloud Function that resizes, crops, and optimizes an image stored on a Google Cloud Storage bucket. Built with Python and Flask.

## Usage

Send a HTTP POST request to the endpoint with the data below:

**inputFileGcs** (`string`, Required): The path to the image to process on Google Cloud Storage\
**outputFileGcs** (`string`, Required): The path to save the processed image to on Google Cloud Storage

**crop** (`object`, Optional): If specified, the function will crop the image to the provided constraints.\
**crop.cropUsing** (`'resolution' | 'ratio'`, Required if `crop` is provided): The method to crop with. `resolution` will crop the image to the provided resolution. `ratio` will crop the image to the provided ratio without stretching the image.\
**crop.horizontal** (`number`, Required if `crop` is provided): The horizontal resolution to crop to if `resolution` is used, or the horizontal ratio if `ratio` is used.\
**crop.vertical** (`number`, Required if `crop` is provided): The vertical resolution to crop to if `resolution` is used, or the vertical ratio if `ratio` is used.

**resize** (`object`, Optional): If specified, the function will resize the image to the provided size.\
**resize.ignoreAspectRatio** (`boolean`, Optional, defaults to `false`): Whether or not to ignore the image's aspect ratio when resizing.\
**resize.width** (`number`, Required if `resize` is provided): The horizontal resolution to resize to.\
**resize.height** (`number`, Required if `resize` is provided): The vertical resolution to resize to.

**optimize** (`object`, Optional): If specified, the function will optimize the image to reduce file size while maintaining good image quality.\
**optimize.quality** (`number`, Optional, defaults to `85`): Sets the image quality for the optimized image. Applies to JPEG images only.

## Example Request

```json
{
  "inputFileGcs": "path/to/input-image.jpg",
  "outputFileGcs": "path/to/output-image.jpg",
  "crop": {
    "cropUsing": "ratio",
    "horizontal": 16,
    "vertical": 9
  },
  "resize": {
    "ignoreAspectRatio": false,
    "width": 1920,
    "height": 1080
  },
  "optimize": {
    "quality": 90
  }
}
```

## Getting Started

To deploy the serverless function to Google Cloud Functions, [refer to the official Google Cloud documentation](https://cloud.google.com/functions/docs/deploying) and choose your preferred method of deployment.

The entry point for the Cloud Function is `process`.

You will need to set the following environment variables:

### Build Environment Variables

- **GOOGLE_FUNCTION_SOURCE**: `src/main.py`

### Runtime Environment Variables

- **GOOGLE_CLOUD_STORAGE_BUCKET**: The Google Cloud Storage bucket to use.
