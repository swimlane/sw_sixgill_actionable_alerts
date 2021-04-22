from sixgill.sixgill_actionable_alert_client import SixgillActionableAlertClient
import requests
from sixgill.sixgill_base_client import SixgillBaseClient


class SixgillActionableAlertsBaseClass(object):

    def __init__(self, context):
        self.client_id = context.asset.get('client_id', '')
        self.client_secret = context.asset.get('client_secret', '')
        self.verify = context.asset.get('verify_ssl', False)
        self.organization_id = context.asset.get('organization_id', None)
        http_proxy = context.asset.get('http_proxy')
        session = requests.Session()
        session.proxies = {} if not http_proxy else http_proxy
        self.proxy = session
        self.state = context.state
        self.channel_id = '9edd89168582842d84430bac51a06eb3'

    def auth_test(self):
        """checks to see if asset inputs are valid."""
        response = SixgillBaseClient(self.client_id, self.client_secret, self.channel_id, verify=self.verify,
                                     session=self.proxy).get_access_token()

        return response


class SixgillAPIRequests(SixgillActionableAlertsBaseClass):

    def __init__(self, context):
        super(SixgillAPIRequests, self).__init__(context)
        self.sixgill_alert_client = SixgillActionableAlertClient(self.client_id, self.client_secret, self.channel_id,
                                                                 verify=self.verify, session=self.proxy)

    def get_actionable_alerts(self, offset):
        """returns the list of actionable alerts."""
        raw_response = self.sixgill_alert_client.get_actionable_alerts_bulk(offset=offset,
                                                                            organization_id=self.organization_id)

        return raw_response

    def get_alert_info(self, alert_id):
        """returns the actionable alert info for the specific actionable alert id."""
        alert_info_response = self.sixgill_alert_client.get_actionable_alert(actionable_alert_id=alert_id,
                                                                             organization_id=self.organization_id)

        return alert_info_response

    def get_alert_content(self, alert_id):
        """returns the actionable alert content for the specific actionable alert id."""
        alert_content_response = self.sixgill_alert_client.get_actionable_alert_content(
            actionable_alert_id=alert_id,
            organization_id=self.organization_id)

        return alert_content_response.get('items')


class SwimlaneActionableAlertFields:
    """returns the required fields to store in the swilane platform."""

    def __init__(self, alert_id, alert_title, threat_level, threat_types, date, language, threat_actor, source,
                 item_content, item_title, tags):
        self.alert_id = alert_id
        self.alert_title = alert_title
        self.threat_level = threat_level
        self.threat_types = threat_types
        self.date = date
        self.language = language
        self.threat_actor = threat_actor
        self.source = source
        self.item_content = item_content
        self.item_title = item_title
        self.tags = tags
        self.sixgill_portal_reference = f"https://portal.cybersixgill.com/#/?actionable_alert={alert_id}"
