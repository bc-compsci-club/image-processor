import os
import subprocess
import imghdr
import tempfile

import flask
from marshmallow import ValidationError
from google.cloud import storage

import request_schema

# Initialize Google Cloud Storage
client = storage.Client()
bucket = client.bucket(os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET"))


def process(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        # flask.Flask.make_response>`.
        `make_response <http://flask.pocoo.org/docs/1.0/api/
    """
    req_json = request.get_json()

    # Validate request body
    try:
        schema = request_schema.RequestSchema()
        schema.load(data=req_json)
    except ValidationError as err:
        print(err.messages)
        return flask.abort(400, err.messages)

    # File and directory variables
    image_file_name = req_json["inputFileGcs"].split("/")[-1]
    image_dir = os.path.join(tempfile.gettempdir(), 'to-process')
    image_path = os.path.join(image_dir, image_file_name)
    processed_image_dir = os.path.join(tempfile.gettempdir(), "processed")
    processed_image_path = os.path.join(processed_image_dir, image_file_name)

    # Create used directories if they don't exist
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    if not os.path.isdir(processed_image_dir):
        os.mkdir(processed_image_dir)

    # Download image from Google Cloud Storage
    download_blob = bucket.blob(req_json["inputFileGcs"])
    if not download_blob.exists():
        # File does not exist
        return flask.abort(404)
    download_blob.download_to_filename(image_path)

    # Process image with ImageMagick
    command_parts = ["convert", f'"{image_path}"']

    # Image crop
    if "crop" in req_json:
        separator = ""

        if (req_json["crop"]["cropUsing"] == "resolution"):
            separator = "x"
        elif (req_json["crop"]["cropUsing"] == "ratio"):
            separator = ":"
        else:
            return flask.abort(400)

        command_parts.extend(
            ["-gravity", "Center", "-crop", f'{req_json["crop"]["horizontal"]}{separator}{req_json["crop"]["vertical"]}'])

    # Image resize
    if "resize" in req_json:
        resize_arg = f'{req_json["resize"]["width"]}x{req_json["resize"]["height"]}'

        # Check if key exists and that it is True, otherwise don't ignore the aspect ratio
        if "ignoreAspectRatio" in req_json["resize"] and req_json["resize"]["ignoreAspectRatio"]:
            resize_arg += "\!"

        command_parts.extend(
            ["-resize", resize_arg])

    # Image optimize
    if "optimize" in req_json:
        image_type = imghdr.what(image_path)

        if image_type == "jpeg":
            # Default to 85 and change if the user provided a quality
            quality = "85"
            if "quality" in req_json["optimize"]:
                quality = str(req_json["optimize"]["quality"])

            command_parts.extend(
                ["-sampling-factor", "4:2:0", "-strip", "-quality", quality, "-interlace", "JPEG", "-colorspace", "sRGB"])

        elif image_type == "png":
            command_parts.append("-strip")

        else:
            return flask.abort(400)

    # Add the output file name
    command_parts.append(processed_image_path)

    # Construct the final command and run it
    convert_command = " ".join(command_parts)
    subprocess.run(convert_command, shell=True, check=True)

    # Upload converted image to Google Cloud Storage
    upload_blob = bucket.blob(req_json["outputFileGcs"])
    upload_blob.upload_from_filename(processed_image_path)

    # Return new location
    res = flask.Response(status=201)
    res.headers["Location"] = f'gs://{bucket.name}/{req_json["outputFileGcs"]}'
    return res
