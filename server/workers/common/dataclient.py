import json
from dateutil.parser import parse


def detect_error(params):
    reason = []
    if len(params.get('q').split(" ")) < 4:
        reason.extend(["typo", "too specific"])
    else:
        reason.extend(["query length", "too specific"])
    from_ = params.get('from')
    to_ = params.get('to')
    if (from_ is not None and to_ is not None):
        timedelta = parse(to_) - parse(from_).days
        if timedelta <= 60:
            reason.append("timeframe too short")
    return json.dumps({"status": "error",
                       "reason": reason})
