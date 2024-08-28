from models import Profile, EmploymentStint
from typing import Iterable
import json
import openai
import instructor
from pydantic import BaseModel
from tqdm.asyncio import tqdm_asyncio as asyncio
from asyncio import run, Semaphore
import random
from collections import defaultdict
from textwrap import dedent
from jinja2 import Template

client = instructor.from_openai(openai.AsyncOpenAI())

def get_stints(file_path:str) -> Iterable[EmploymentStint]:
    with open(file_path, "r") as f:
        for line in f:
            profile = Profile(**json.loads(line))
            for stint in profile.stints:
                yield (stint, profile.uuid)

async def generate_achievements(stint: EmploymentStint, uuid:str, semaphore: Semaphore) -> EmploymentStint:   
    class Achievements(BaseModel):
        achievements: list[str]
    
    async with semaphore:
        achievements = await client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Achievements,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates achievements for a resume."
            },
            {
                "role": "user",
                "content": f"Generate {random.randint(1, 3)} achievements for the following stint: {stint.model_dump_json()}"
            }
        ]
        )

        stint.achievements = achievements.achievements
        return uuid, stint

async def main():
    semaphore = Semaphore(10)
    coros = [generate_achievements(stint, uuid, semaphore) for stint,uuid in get_stints("./data/profiles.jsonl")]
    stints = await asyncio.gather(*coros)

    profiles_uuid_to_stints = defaultdict(list)

    for uuid,stint in stints:
        profiles_uuid_to_stints[uuid].append(stint)
    
    for profile_uuid in profiles_uuid_to_stints:
        with open(f"./data/resumes/{profile_uuid}.txt", "w+") as f:
            

            # Create a simple resume template
            resume_template = Template(dedent("""
            Resume for {{ profile.uuid }}

            {% for stint in profile.stints %}
            {{ stint.start_date.strftime('%Y-%m-%d') }} to {{ stint.end_date.strftime('%Y-%m-%d') }}
            {{ stint.company }} - {{ stint.seniority_level.capitalize() }} ({{ stint.industry.capitalize() }})
            Achievements:
            {% for achievement in stint.achievements %}
            - {{ achievement }}
            {% endfor %}
            {% endfor %}
            """))

            profile = Profile(
                uuid = profile_uuid,
                stints = profiles_uuid_to_stints[profile_uuid]
            )
            
            # Render the resume using the template
            rendered_resume = resume_template.render(profile=profile)

            f.write(rendered_resume)
                
    

if __name__ == "__main__":
    run(main())