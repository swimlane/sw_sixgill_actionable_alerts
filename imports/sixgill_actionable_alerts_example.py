from sw_cybersixgill_actionable_alerts import SixgillActionableAlertsBaseClass, SwimlaneActionableAlertFields, \
    SixgillAPIRequests
from datetime import datetime

SKIP_ALERTS = ["GithubAlertRule"]

MOST_RECENT_ACTIONABLE_ALERT = "most_recent_actionable_alert"


class SwMain(SixgillAPIRequests):

    def __init__(self, context):
        super(SwMain, self).__init__(context)
        self.context = context
        self.actionable_alerts = []

    def process_actionable_alerts(self, alert):
        """process the actionable alerts."""

        if alert.get('id') not in self.state and alert.get('alert_name') not in SKIP_ALERTS:

            self.state.update({alert.get('id'): True})

            alert_info_raw_response = self.get_alert_info(alert.get('id'))

            alert_item_content = {'site': '', 'creator': '', 'content': '', 'title': '',
                                  'tags': []}
            alert_content_raw_response = ''
            if alert_info_raw_response.get('es_id') is not None and alert_info_raw_response.get(
                    'es_id') != 'Not Applicable':
                alert_content_raw_response = self.get_alert_content(alert.get('id'))
                for item in alert_content_raw_response:
                    if item.get('_id') == alert_info_raw_response.get('es_id'):
                        alert_item_content = item.get('_source')
            else:
                alert_item_content['content'] = alert_content_raw_response
            raw_response = SwimlaneActionableAlertFields(alert.get('id'), alert.get('title'),
                                                         alert.get('threat_level'),
                                                         alert.get('threats'),
                                                         alert.get('date'),
                                                         alert.get('lang'),
                                                         alert_item_content.get('creator'),
                                                         alert_item_content.get('site'),
                                                         str(alert_item_content.get('content')),
                                                         alert_item_content.get('title'),
                                                         alert_item_content.get(
                                                             'tags')).__dict__

            return raw_response

    def update_most_recent_actionable_alert(self):
        """update most_recent_actionable_alert filed in state object."""

        if MOST_RECENT_ACTIONABLE_ALERT in self.state:
            if datetime.strptime(self.actionable_alerts[0].get('date'), "%Y-%m-%d %H:%M:%S") >= datetime.strptime(
                    self.state.get(MOST_RECENT_ACTIONABLE_ALERT), "%Y-%m-%d %H:%M:%S"):
                self.state.update({MOST_RECENT_ACTIONABLE_ALERT: self.actionable_alerts[0].get('date')})
        else:
            self.state.update({MOST_RECENT_ACTIONABLE_ALERT: self.actionable_alerts[0].get('date')})

    def execute(self):
        """returns the actionable alerts from sixgill."""
        try:
            offset = 0

            while True:
                alerts = self.get_actionable_alerts(offset)

                if not alerts:
                    break

                if MOST_RECENT_ACTIONABLE_ALERT in self.state:
                    if datetime.strptime(alerts[0].get('date'), "%Y-%m-%d %H:%M:%S") <= datetime.strptime(
                            self.state.get(MOST_RECENT_ACTIONABLE_ALERT), "%Y-%m-%d %H:%M:%S"):
                        break

                offset += len(alerts)

                for alert in alerts:
                    processed_alert = self.process_actionable_alerts(alert)
                    if processed_alert:
                        self.actionable_alerts.append(processed_alert)

            if len(self.actionable_alerts) > 0:
                self.update_most_recent_actionable_alert()

            return self.actionable_alerts
        except Exception:
            raise