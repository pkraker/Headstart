from datetime import datetime
import math
from marshmallow import Schema, fields, pre_load, validates, ValidationError


class SearchParamSchema(Schema):
    q = fields.Str(required=True)
    sorting = fields.Str(required=True)
    from_ = fields.Date(required=True, data_key="from",
                        format="%Y-%m-%d")
    to = fields.Date(required=True,
                     format="%Y-%m-%d")
    vis_type = fields.Str(require=True)
    limit = fields.Int()
    year_range = fields.Str()
    today = fields.Str()
    language = fields.Str()
    lang_id = fields.Str()
    time_range = fields.Str()
    document_types = fields.List(fields.Str())
    article_types = fields.List(fields.Str())
    unique_id = fields.Str()
    raw = fields.Boolean()
    sg_method = fields.Str()
    vis_id = fields.Str(default=None)
    optradio = fields.Str()
    service = fields.Str()

    @pre_load
    def fix_years(self, in_data, **kwargs):
        if len(in_data.get('from')) == 4:
            in_data["from"] = in_data["from"]+"-01-01"
        if len(in_data.get('to')) == 4:
            in_data["to"] = in_data["to"]+"-12-31"
        return in_data

    @pre_load
    def fix_limit(self, in_data, **kwargs):
        try:
            in_data["limit"] = int(in_data["limit"])
            return in_data
        except Exception:
            return in_data

    @validates('from_')
    def is_not_in_future(self, date):
        if date > datetime.today().date():
            raise ValidationError("Starting date can't be in the future.")

    @validates('limit')
    def limit_is_int(self, limit):
        if not isinstance(limit, int):
            raise ValidationError("Limit must be an integer.")


class TripleParamsSchema(SearchParamSchema):
    from_ = fields.Date(data_key="from",
                    format="%Y-%m-%d")

    class Meta:
        dateformat = "%Y-%m-%d"
    
    @pre_load
    def fix_years(self, in_data, **kwargs):
        try:
            if math.isnan(float(in_data.get('from'))):
                in_data["from"] = "1800"
        except Exception:
            pass
        if len(in_data.get('from')) == 4:
            in_data["from"] = in_data["from"]+"-01-01"
        if len(in_data.get('to')) == 4:
            in_data["to"] = in_data["to"]+"-12-31"
        return in_data