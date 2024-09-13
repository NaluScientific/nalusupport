import yaml
import argparse
from datetime import datetime

SOFTWARE_FILE = './_data/software.yml'
BOARDS_FILE = './_data/board.yml'

def update_naluscope_version(new_version):
    """Open the yml file for software versions and update the current version of NaluScope."""

    with open(SOFTWARE_FILE, 'r') as file:
        config = yaml.safe_load(file)

    key = 'naluscope'
    if 'current' in config[key]:
        # Move current version to archived
        current_version = config[key]['current'][0]
        config[key]['archived'].insert(0, current_version)

        # Update current with new version
        new_entry = {
            'name': new_version,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'downloads': {
                'windows': f'https://github.com/NaluScientific/NaluScope-Release/releases/download/{new_version}/NaluScope.Installer-{new_version[1:]}.0.exe',
                'linux': f'https://github.com/NaluScientific/{key}-Release/releases/download/{new_version}/{key}.tar.gz'
            }
        }
        config[key]['current'][0] = new_entry

    with open(SOFTWARE_FILE, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def update_naluscope_manual_version(new_version): 
    with open(BOARDS_FILE, 'r') as file:
        config = yaml.safe_load(file)

    for board in config.keys():
        if 'current' in config[board]:
            # Find the current NaluScope manual to archive
            current_manual = next((item for item in config[board]['current'] if 'Manual' in item['name']), None)
            if current_manual:
                # Extract the board name using split on ".-." and ".User.Manual.pdf"
                board_name_for_url = current_manual['url'].split('.-.')[1].split('.User.Manual.pdf')[0]

                # Move the current NaluScope manual to the archived section
                config[board]['archived'].insert(0, current_manual)
                config[board]['current'].remove(current_manual)

            # Add a new entry for the updated NaluScope manual
            new_manual_entry = {
                'name': f'NaluScope {new_version} Manual',
                'url': f'https://github.com/NaluScientific/NaluScope-Release/releases/download/{new_version}/NaluScope.{new_version[1:]}.-.{board_name_for_url}.User.Manual.pdf'
            }

            # Add the new manual to the current section
            config[board]['current'].insert(0, new_manual_entry)

    # Write the updated configuration back to the file
    with open(BOARDS_FILE, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update software version in Jekyll config file.")
    parser.add_argument('version', type=str, help="The new version number to add.")
    
    args = parser.parse_args()

    version = args.version
    if version[0] != 'v':
        print("Version number must start with 'v'.")
        exit(1)
    update_naluscope_version(version)
    update_naluscope_manual_version(version)


