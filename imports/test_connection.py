from sw_sixgill_actionable_alerts import SixgillActionableAlertsBaseClass


class SwMain(SixgillActionableAlertsBaseClass):

    def execute(self):
        try:
            self.auth_test()
        except Exception as e:
            return {'successful': False,
                    'errorMessage': "Auth request failed - please verify client_id and client_secret."}
        return {'successful': True}
