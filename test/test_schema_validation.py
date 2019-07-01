import json
import unittest

from lib.schema_validator import is_valid


class TestSchemaValidation(unittest.TestCase):
    @classmethod
    def get_json(cls, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def setUp(self):
        self.freelance = self.get_json('test/fixtures/freelancer_good.json')
        self.schema = self.get_json('exercise/freelancer_schema.json')

    # validation test
    def test_good_format(self):
        self.assertTrue(self.freelance, self.schema)

    # required values
    def test_missing_freelance(self):
        self.freelance.pop('freelance')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_id(self):
        self.freelance['freelance'].pop('id')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_pro_xp(self):
        self.freelance['freelance'].pop('professionalExperiences')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_skills(self):
        self.freelance['freelance']['professionalExperiences'][0].pop('skills')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_start_date(self):
        self.freelance['freelance']['professionalExperiences'][0].pop('startDate')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_end_date(self):
        self.freelance['freelance']['professionalExperiences'][0].pop('endDate')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_skill_id(self):
        self.freelance['freelance']['professionalExperiences'][0]['skills'][0].pop('id')
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_missing_skill_name(self):
        self.freelance['freelance']['professionalExperiences'][0]['skills'][0].pop('name')
        self.assertFalse(is_valid(self.freelance, self.schema))

    # types
    def test_wrong_type_pro_xp(self):
        self.freelance['freelance']['professionalExperiences'] = 'I'
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_skills(self):
        self.freelance['freelance']['professionalExperiences'][0]['skills'] = 'got'
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_start_date(self):
        self.freelance['freelance']['professionalExperiences'][0]['startDate'] = 9
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_end_date(self):
        self.freelance['freelance']['professionalExperiences'][0]['endDate'] = 9
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_skill_id(self):
        self.freelance['freelance']['professionalExperiences'][0]['skills'][0]['id'] = 'problems'
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_freelance(self):
        self.freelance['freelance'] = 'but'
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_id(self):
        self.freelance['freelance']['id'] = 'the'
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_wrong_type_skill_name(self):
        self.freelance['freelance']['professionalExperiences'][0]['skills'][0]['name'] = Exception
        self.assertFalse(is_valid(self.freelance, self.schema))

    # dates format
    def test_start_date_format(self):
        self.freelance['freelance']['professionalExperiences'][0]['startDate'] = "ain't"
        self.assertFalse(is_valid(self.freelance, self.schema))

    def test_end_date_format(self):
        self.freelance['freelance']['professionalExperiences'][0]['endDate'] = 'one'
        self.assertFalse(is_valid(self.freelance, self.schema))
