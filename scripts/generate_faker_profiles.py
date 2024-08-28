from datetime import datetime
from models import EmploymentStint, Profile, SeniorityLevel, industries
import random
from faker import Faker
from typing import Literal
from dateutil.relativedelta import relativedelta

faker = Faker()


def determine_if_promoted(curr_level: SeniorityLevel) -> SeniorityLevel:
    is_prompted = random.random() < 0.2 # 50% chance of being prompted at each level
    if not is_prompted or curr_level == "senior":
        return curr_level

    return "mid" if curr_level == "junior" else "senior"
    

def generate_random_stint(start: datetime, curr_level: SeniorityLevel) -> EmploymentStint:
    tenure =random.randint(1, 60)

    return EmploymentStint(
        start_date=start,
        end_date=start + relativedelta(months=tenure),
        company=faker.company(),
        achievements=[],
        seniority_level=determine_if_promoted(curr_level),
        industry=random.choice(industries),
    )

def generate_random_profile(start_year: int, stints: int):
    start = datetime(start_year, 8, 1)
    curr_level = "junior"

    res = []

    for i in range(stints):
        stint = generate_random_stint(start, curr_level)
        start = stint.end_date 
        curr_level = stint.seniority_level
        res.append(stint)

    return Profile(stints=res)

if __name__ == "__main__":
    profiles = [
        generate_random_profile(random.randint(2010, 2024), random.randint(1, 5))
        for _ in range(10)
    ]

    with open("./data/profiles.jsonl", "w+") as f:
        for profile in profiles:
            f.write(profile.model_dump_json() + "\n")