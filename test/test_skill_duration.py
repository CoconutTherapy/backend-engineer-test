import json
import unittest
from datetime import datetime

import pytz
from pandas import Timestamp

from lib.skill_duration import get_month_list, format_skills, compute_durations, process_freelance


class TestSkillDuration(unittest.TestCase):

    def test_month_list_generation(self):
        start_date = '2019-01-01T00:00:00+01:00'
        end_date = '2019-04-01T00:00:00+01:00'

        should = [
            Timestamp('2019-01-01', freq='MS', tz=pytz.FixedOffset(60)),
            Timestamp('2019-02-01', freq='MS', tz=pytz.FixedOffset(60)),
            Timestamp('2019-03-01', freq='MS', tz=pytz.FixedOffset(60))
        ]

        month_list = get_month_list(start_date=start_date, end_date=end_date)

        self.assertEqual(month_list, should)
        self.assertRaises(Exception, get_month_list, None, None)
        self.assertRaises(Exception, get_month_list, start_date, None)
        self.assertRaises(Exception, get_month_list, None, end_date)

    def test_skills_formatting(self):
        freelance = {
            'freelance': {
                'professionalExperiences': [
                    {
                        'startDate': '2019-01-01T00:00:00+01:00',
                        'endDate': '2019-04-01T00:00:00+01:00',
                        'skills': [
                            {
                                'id': 1,
                                'name': 'Java'
                            }, {
                                'id': 2,
                                'name': 'Python'
                            },
                        ]
                    }, {
                        'startDate': '2018-10-01T00:00:00+01:00',
                        'endDate': '2018-12-01T00:00:00+01:00',
                        'skills': [
                            {
                                'id': 3,
                                'name': 'AWS'
                            }, {
                                'id': 2,
                                'name': 'Python'
                            }, {
                                'id': 4,
                                'name': 'Cobol'
                            },
                        ]
                    }
                ]
            }
        }

        first_experience = [Timestamp('2019-01-01', freq='MS', tz=pytz.FixedOffset(60)),
                            Timestamp('2019-02-01', freq='MS', tz=pytz.FixedOffset(60)),
                            Timestamp('2019-03-01', freq='MS', tz=pytz.FixedOffset(60))]

        second_experience = [Timestamp('2018-10-01', freq='MS', tz=pytz.FixedOffset(60)),
                             Timestamp('2018-11-01', freq='MS', tz=pytz.FixedOffset(60))]

        should = [
            {'id': 1, 'name': 'Java', 'durationInMonths': first_experience},
            {'id': 2, 'name': 'Python', 'durationInMonths': first_experience},
            {'id': 3, 'name': 'AWS', 'durationInMonths': second_experience},
            {'id': 2, 'name': 'Python', 'durationInMonths': second_experience},
            {'id': 4, 'name': 'Cobol', 'durationInMonths': second_experience}
        ]

        formatted_skills = format_skills(freelance)

        self.assertEqual(formatted_skills, should)
        self.assertRaises(Exception, format_skills, None)

    def test_computation(self):
        first_experience = [Timestamp('2019-01-01'), Timestamp('2019-02-01'), Timestamp('2019-03-01')]
        second_experience = [Timestamp('2018-12-01'), Timestamp('2019-01-01')]

        skills = [
            {'id': 1, 'name': 'Fortran', 'durationInMonths': first_experience},
            {'id': 2, 'name': 'Python', 'durationInMonths': first_experience},
            {'id': 2, 'name': 'Python', 'durationInMonths': second_experience},
            {'id': 3, 'name': 'Cobol', 'durationInMonths': second_experience}
        ]

        should = [
            {'id': 1, 'name': 'Fortran', 'durationInMonths': 3},
            {'id': 2, 'name': 'Python', 'durationInMonths': 4},
            {'id': 3, 'name': 'Cobol', 'durationInMonths': 2}
        ]

        durations = compute_durations(skills)

        self.assertEqual(durations, should)
        self.assertRaises(Exception, compute_durations, None)

    def test_functional_process(self):
        freelance = {
            'freelance': {
                'id': 20,
                'professionalExperiences': [
                    {
                        'startDate': '2019-01-01T00:00:00+01:00',
                        'endDate': '2019-07-01T00:00:00+01:00',
                        'skills': [
                            {
                                'id': 1,
                                'name': 'Erlang'
                            }, {
                                'id': 2,
                                'name': 'Python'
                            },
                        ]
                    }, {
                        'startDate': '2018-10-01T00:00:00+01:00',
                        'endDate': '2019-05-01T00:00:00+01:00',
                        'skills': [
                            {
                                'id': 3,
                                'name': 'Lisp'
                            }, {
                                'id': 2,
                                'name': 'Python'
                            }, {
                                'id': 4,
                                'name': 'Cobol'
                            },
                        ]
                    }
                ]
            }
        }

        should = json.dumps({
            'freelance': {
                'id': 20,
                'computedSkills': [
                    {'id': 1, 'name': 'Erlang', 'durationInMonths': 6},
                    {'id': 2, 'name': 'Python', 'durationInMonths': 9},
                    {'id': 3, 'name': 'Lisp', 'durationInMonths': 7},
                    {'id': 4, 'name': 'Cobol', 'durationInMonths': 7}
                ]
            }
        }, indent=4)

        processed_freelance = process_freelance(freelance)

        self.assertEqual(processed_freelance, should)
        self.assertRaises(Exception, process_freelance, None)
