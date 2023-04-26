import json


class Certificate:

    def __init__(self, receiver, certName, date,
                 certType, organization, certContent):
        self.receiver = receiver
        self.certName = certName
        self.date = date
        self.certType = certType
        self.organization = organization
        self.certContent = certContent

    def to_json(self):
        cert_dict = {
            'receiver': self.receiver,
            'certName': self.certName,
            'date': self.date,
            'certType': self.certType,
            'organization': self.organization,
            'certContent': self.certContent
        }
        return json.dumps(cert_dict, sort_keys=True)

    def from_json(json_dict):
        return Certificate(json_dict['receiver'], json_dict['certName'],
                           json_dict['date'], json_dict['certType'],
                           json_dict['organization'], json_dict[
                               'certContent'])
