import re
from shutil import copytree
from pathlib import Path
import click
import yaml

@click.command()
@click.option("--generate", "-gen", is_flag=True, required=True, help="Generate new blank files")
def cli(generate):
    # Open the day.yaml and increment the day 
    day_path = Path(__file__).parent.parent / 'course' / 'day.yaml'
    with open(day_path, 'r+') as f:
        day_yaml = yaml.safe_load(f)
        next_day= day_yaml['day'] + 1
        day_yaml['day'] = next_day
        
        with open(day_path, 'w') as f:
            yaml.dump(day_yaml, f)

    # Update all references in tests
    tests_dir = Path(__file__).parent.parent / 'tests'
    test_files = tests_dir.glob('**/*_test.py')
    for file in test_files:
        with open(file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if re.search('day[0-9]*', line):
                    line = re.sub('day[0-9]*', f'day{next_day}', line)
                    lines[i] = line

            with open(file, 'w') as f:
                f.writelines(lines)

    # Create new day folder and copy golden files into it
    new_day_path = Path(__file__).parent.parent / 'course' / f'day{next_day}'
    golden_path= Path(__file__).parent.parent / 'course' / 'golden'
    copytree(golden_path, new_day_path)


if __name__ == "__main__":
    cli()
