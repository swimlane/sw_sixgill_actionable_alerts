from sw_cybersixgill_actionable_alerts import SixgillActionableAlertsBaseClass


class SwMain(SixgillActionableAlertsBaseClass):

    def execute(self):
        try:
            self.auth_test()
        except Exception as e:
            return {'successful': False,
                    'errorMessage': str(e)}
        return {'successful': True}