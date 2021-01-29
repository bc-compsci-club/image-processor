from marshmallow import Schema, fields, validate


class CropSchema(Schema):
    cropUsing = fields.Str(validate=validate.OneOf(
        ["resolution", "ratio"]), required=True)
    horizontal = fields.Int(validate=validate.Range(min=1), required=True)
    vertical = fields.Int(validate=validate.Range(min=1), required=True)


class ResizeSchema(Schema):
    ignoreAspectRatio = fields.Boolean(required=False)
    width = fields.Int(validate=validate.Range(min=1), required=True)
    height = fields.Int(validate=validate.Range(min=1), required=True)


class OptimizeSchema(Schema):
    quality = fields.Int(validate=validate.Range(
        min=1, max=100), required=False)


class RequestSchema(Schema):
    inputFileGcs = fields.Str(required=True)
    outputFileGcs = fields.Str(required=True)
    crop = fields.Nested(CropSchema, required=False)
    resize = fields.Nested(ResizeSchema, required=False)
    optimize = fields.Nested(OptimizeSchema, required=False)
