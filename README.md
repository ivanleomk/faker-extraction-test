# Introduction

This repository showcases a simple way to generate fake resume profiles using `faker`. We do so by generating a random number of employment stints followed by a random number of achievements for each stint.

This allows us to generate a large number of fake profiles with simulated promotions and achievements. We also have users across a wide variety of industries and seniority levels.

## Instructions

1. First create a virtual environment and install the requirements.

```bash
uv venv
uv pip install -r requirements.txt
```

2. Then run the `scripts/generate_faker_profiles.py` script to generate a large number of fake profiles. Currently we're generating only 10 profiles but this can be easily modified.

```bash
python3 ./scripts/generate_faker_profiles.py
```

3. Finally, run the `scripts/generate_fake_resumes.py` script to generate a large number of fake resumes. These are currently txt files that are being formatted using jinja2 but you can really generate them however you want

```bash
python3 ./scripts/generate_fake_resumes.py
```
