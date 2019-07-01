# -*- coding: utf-8 -*-
""""
This module computes the skills duration from a freelance's experiences
"""
import json
from typing import List

import pandas as pd


def process_freelance(freelance: dict) -> dict:
    """
    Build a json of computed skills duration for a given freelance
    :param freelance: a base freelance payload
    :return: a json encoded object of skills durations
    """
    formatted_skills = format_skills(freelance)

    computed_skills = compute_durations(formatted_skills)

    output = format_output(id=freelance['freelance']['id'], computed_skills=computed_skills)

    return output


def compute_durations(skills: dict) -> List[dict]:
    """
    Compute the duration in months of each skill
    :param skills: the formatted_skills
    :return: the computed durations
    """
    return (
        pd.DataFrame.from_dict(skills)  # build the dataframe
            .groupby(['id', 'name'])['durationInMonths']
            .sum()  # merge all lists of months into one list
            .apply(lambda x: len(set(x)))  # unique count of months
            .reset_index()  # as dataframe
            .to_dict('records')  # output formatted records
    )


def format_skills(freelance: dict) -> List[dict]:
    """
    Format the skills to be loaded in a pandas dataframe
    :param freelance: the initial payload
    :return: the formatted skills
    """
    return [
        {
            'id': skill['id'],
            'name': skill['name'],
            'durationInMonths': get_month_list(start_date=pro_xp['startDate'], end_date=pro_xp['endDate'])
        }
        for pro_xp in freelance['freelance']['professionalExperiences']
        for skill in pro_xp['skills']
    ]


def format_output(id: int, computed_skills: List[dict]) -> str:
    """
    Format the output for pretty-printing
    :param id: id of the freelance
    :param computed_skills: array of computed skills durations
    :return: the json
    """
    return json.dumps({
        'freelance': {
            'id': id,
            'computedSkills': computed_skills
        }
    }, indent=4)


def get_month_list(start_date: str, end_date: str) -> List[object]:
    """
    Generate a list of months between the start_date and end_date, excluding the end_date
    :param start_date: start of the range
    :param end_date: end of the range
    :return: a list of months as pandas timestamps
    """
    return list(pd.date_range(start=pd.to_datetime(start_date),
                              end=pd.to_datetime(end_date),
                              closed='left',
                              freq='1MS'))
