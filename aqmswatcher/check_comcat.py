import geojson
import requests
from datetime import datetime, timedelta
import smtplib
import tomputils.util as tutil
from aqmswatcher import logger


COMCAT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
AQMS_URL = "https://avo.alaska.edu/admin/catalog/catalogResults.php"
LOOKBACK = 30
# CERT = tutil.get_env_var("CERT", None)
CERT = None


def get_comcat_events():
    logger.debug("Requesting ComCat events")
    end_time = datetime.now()
    start_time = end_time - timedelta(days=LOOKBACK)
    comcat_args = {'starttime': start_time.isoformat(),
                   'endtime': end_time.isoformat(),
                   'catalog': 'av',
                   'minmagnitude': -1}
    r = requests.get(COMCAT_URL, params=comcat_args, verify=CERT)
    comcat_events = geojson.loads(r.content)
    evids = []
    for event in comcat_events['features']:
        ids = event['properties']['ids'].split(",")
        for id in ids:
            if id.startswith("av"):
                evids.append(id[2:].rstrip(","))
    return evids


def get_aqms_events():
    logger.debug("Requesting AQMS events")
    cert = tutil.get_env_var("CERT", None)
    end_time = datetime.now()
    start_time = end_time - timedelta(days=LOOKBACK)
    aqms_args = {'from': start_time.strftime("%Y/%m/%d"),
                 'to': end_time.strftime("%Y/%m/%d"),
                 'review': "F",
                 'format': "summary",
                 'selectFlag': "selected",
                 'result': "display"
                 }
    response = requests.get(AQMS_URL, params=aqms_args, verify=CERT)
    evids = []
    for event in response.text.splitlines()[2:]:
        parts = event.split()
        if len(parts) < 14:
            continue
        evids.append(parts[13])
    return evids


def report_error(missing, extra):
    mailhost = tutil.get_env_var('MAILHOST')
    sender = tutil.get_env_var('SENDER')
    recipients = tutil.get_env_var('RECIPIENTS')

    message = "From: {}\nTo: {}\nSubject: AQMS ComCat error\n\n"
    message = message.format(sender, recipients)
    if missing:
        logger.info("Found missing events")
        message += "Events not in ComCat:\n"
        for evid in missing:
            message += "\t{}\n".format(evid)
        message += "\n"

    if extra:
        logger.info("Found extra events")
        message += "Events that should be removed from ComCat:\n"
        for evid in extra:
            message += "\t{}\n".format(evid)
        message += "\n"

    try:
        smtpObj = smtplib.SMTP(mailhost)
        smtpObj.sendmail(sender, recipients.split(','), message)
    except smtplib.SMTPException:
        pass


def main():
    comcat_events = get_comcat_events()
    aqms_events = get_aqms_events()

    missing = [evid for evid in aqms_events if evid not in comcat_events]
    extra = [evid for evid in comcat_events if evid not in aqms_events]

    if missing or extra:
        report_error(missing, extra)


if __name__ == '__main__':
    main()
