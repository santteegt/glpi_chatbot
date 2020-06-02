from dateutil import relativedelta, parser
from typing import Dict, Text, Any, Optional
from rasa_sdk import Tracker
import unicodedata

from actions.constants import EntitySlotEnum


def close_interval_duckling_time(time_info: Dict[Text, Any]) -> Optional[Dict[Text, Any]]:
    """

    :param time_info: interval metadata from duckling
    :return: Dict with fields { EntitySlotEnum.START_TIME, EntitySlotEnum.END_TIME, EntitySlotEnum.GRAIN }
    """
    grain = time_info.get("to", time_info.get("from", {})).get("grain")
    start = time_info.get("to", {}).get("value")
    end = time_info.get("from", {}).get("value")
    if start or end:
        if start and end:
            parsed_start = parser.isoparse(start)
            parsed_end = parser.isoparse(end)
        else:
            delta_args = {f"{grain}s": 1}
            delta = relativedelta.relativedelta(**delta_args)
            if start:
                parsed_start = parser.isoparse(start)
                parsed_end = parsed_start + delta
            elif end:
                parsed_end = parser.isoparse(end)
                parsed_start = parsed_end - delta
        return {
            EntitySlotEnum.START_TIME: format_time_by_grain(parsed_start, grain),
            EntitySlotEnum.END_TIME: format_time_by_grain(parsed_end, grain),
            EntitySlotEnum.GRAIN: grain
        }


def make_interval_from_value_duckling_time(time_info: Dict[Text, Any]) -> Dict[Text, Any]:
    """

    :param time_info: value metadata from duckling
    :return: Dict with fields { EntitySlotEnum.START_TIME, EntitySlotEnum.END_TIME, EntitySlotEnum.GRAIN }
    """
    grain = time_info.get("grain")
    start = time_info.get("value")
    parsed_start = parser.isoparse(start)
    delta_args = {f"{grain}s": 1}
    delta = relativedelta.relativedelta(**delta_args)
    parsed_end = parsed_start + delta
    return {
        EntitySlotEnum.START_TIME: format_time_by_grain(parsed_start, grain),
        EntitySlotEnum.END_TIME: format_time_by_grain(parsed_end, grain),
        EntitySlotEnum.GRAIN: grain
    }


def parse_duckling_time_as_interval(time_entity: Dict[Text, Any]) -> Optional[Dict[Text, Any]]:
    """

    :param time_entity: metadata returned from duckling
    :return: Dict with fields { EntitySlotEnum.START_TIME, EntitySlotEnum.END_TIME, EntitySlotEnum.GRAIN }
    """
    time_info = time_entity.get("additional_info", {})
    if time_info.get("type") == "interval":
        return close_interval_duckling_time(time_info)
    elif time_info.get("type") == "value":
        return make_interval_from_value_duckling_time(time_info)


def remove_accents(text: Text) -> Text:
    """
    Remove accents from unicode text
    :param text: original text
    :return: normalized text
    """
    nkfd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


# TODO: To be reviewed
def format_time_by_grain(time, grain=None):
    grain_format = {
        "second": "%I:%M:%S%p, %A %b %d, %Y",
        "day": "%A %b %d, %Y",
        "week": "%A %b %d, %Y",
        "month": "%b %Y",
        "year": "%Y",
    }
    timeformat = grain_format.get(grain, "%I:%M%p, %A %b %d, %Y")
    return time.strftime(timeformat)


def parse_duckling_time(
    timeentity: Dict[Text, Any]
) -> Optional[Dict[Text, Any]]:
    timeinfo = timeentity.get("additional_info", {})
    if timeinfo.get("type") == "value":
        value = timeinfo.get("value")
        grain = timeinfo.get("grain")
        parsedtime = {
            "time": format_time_by_grain(parser.isoparse(value), grain),
            "grain": grain,
        }
        return parsedtime


def get_entity_details(
    tracker: Tracker, entity_type: Text
) -> Optional[Dict[Text, Any]]:
    all_entities = tracker.latest_message.get("entities", [])
    entities = [e for e in all_entities if e.get("entity") == entity_type]
    if entities:
        return entities[0]


def parse_duckling_currency(
    entity: Dict[Text, Any]
) -> Optional[Dict[Text, Any]]:
    if entity.get("entity") == "amount-of-money":
        amount = entity.get("additional_info", {}).get("value")
        currency = entity.get("additional_info", {}).get("unit")
        return {"amount_of_money": f"{amount:.2f}", "currency": currency}
    elif entity.get("entity") == "number":
        amount = entity.get("value")
        return {"amount_of_money": f"{amount:.2f}", "currency": "$"}