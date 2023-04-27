import yaml
import argparse


def find_unused_jobs_and_commands(config_path):
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)

    job_in_jobs: set = set(config_data.get('jobs', {}).keys())
    command_in_commands = set(config_data.get('commands', {}).keys())

    jobs_in_workflows: set = set()
    for workflow in config_data.get('workflows', {}).items():
        _, data_dict = workflow
        try:
            jobs = data_dict.get('jobs', [])
            for job in jobs:
                if type(job) is dict:
                    jobs_in_workflows.add(list(job.keys())[0])
                else:
                    jobs_in_workflows.add(job)
        except Exception:
            continue

    commands_in_jobs = set()
    for job in config_data.get('jobs', {}).items():
        _, data_dict = job
        try:
            steps = data_dict.get('steps', [])
            for step in steps:
                if type(step) is dict:
                    commands_in_jobs.add(list(step.keys())[0])
                else:
                    commands_in_jobs.add(step)
        except Exception:
            continue

    commands_in_commands = set()
    for command in config_data.get('commands', {}).items():
        _, data_dict = command
        try:
            steps = data_dict.get('steps', [])
            for step in steps:
                if type(step) is dict:
                    commands_in_commands.add(list(step.keys())[0])
                else:
                    commands_in_commands.add(step)
        except Exception:
            continue

    not_used_jobs = job_in_jobs - jobs_in_workflows
    not_used_commands = command_in_commands - commands_in_jobs - commands_in_commands

    print("Unused jobs:")
    for job in not_used_jobs:
        print(f"  - {job}")

    print("Unused command:")
    for command in not_used_commands:
        print(f"  - {command}")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Find unused jobs and commands in CircleCI config.yml')
    parser.add_argument('config_file_path', help='Path to CircleCI config.yml file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    config_file_path = args.config_file_path
    find_unused_jobs_and_commands(config_file_path)
