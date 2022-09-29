import datetime
import json
import re
from enum import Enum


class CrowdinJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            offset = obj.utcoffset()

            if offset < datetime.timedelta():
                sign = "-"
                offset = offset.seconds / 60 - 24 * 60
            else:
                sign = "+"
                offset = offset.seconds / 60

            offset = abs(int(offset))

            return "{date_time}{sign}{offset_h:02}:{offset_m:02}".format(
                date_time=obj.strftime("%Y-%m-%dT%H:%M:%S"),
                sign=sign,
                offset_h=offset // 60,
                offset_m=offset % 60,
            )

        if isinstance(obj, Enum):
            try:
                return super().default(obj.value)
            except TypeError:
                return obj.value

        return super().default(obj)


class CrowdinJSONDecoder(json.JSONDecoder):
    datetime_re = re.compile(
        r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
        r"[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})"
        r"(?::(?P<second>\d{1,2})(?:[\.,](?P<microsecond>\d{1,6})\d{0,6})?)?"
        r"(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$"
    )

    def _get_timezone(self, tzinfo):
        if tzinfo == "Z":
            return datetime.timezone.utc

        elif tzinfo is not None:
            offset_mins = int(tzinfo[-2:]) if len(tzinfo) > 3 else 0
            offset = 60 * int(tzinfo[1:3]) + offset_mins
            return datetime.timezone(
                datetime.timedelta(minutes=-offset if tzinfo[0] == "-" else offset),
                "{sign}{h:02}{m:02}".format(
                    sign=tzinfo[0], h=offset // 60, m=offset % 60
                ),
            )

    def _parse_datetime(self, value):
        match = self.datetime_re.match(value)
        if match:
            kw = match.groupdict()
            kw["microsecond"] = kw["microsecond"] and kw["microsecond"].ljust(6, "0")
            tzinfo = self._get_timezone(kw.pop("tzinfo"))
            kw = {k: int(v) for k, v in kw.items() if v is not None}
            kw["tzinfo"] = tzinfo
            return datetime.datetime(**kw)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook, **kwargs)

    def object_hook(self, parsed_object):
        for key, value in parsed_object.items():
            if not isinstance(value, (str, bytes)):
                continue

            date_value = self._parse_datetime(value)

            if isinstance(date_value, datetime.datetime):
                parsed_object[key] = date_value

        return parsed_object


def dumps(obj):
    return json.dumps(obj, cls=CrowdinJSONEncoder)


def loads(s):
    return json.loads(s, cls=CrowdinJSONDecoder)
