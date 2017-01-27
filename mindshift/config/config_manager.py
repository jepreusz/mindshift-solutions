# script to create/modify config files
import configparser


class ConfigManager:

    def __init__(self):
        self.cfg_handler = configparser.ConfigParser()

    def create_sections(self, sections):
        for section in sections:
            self.cfg_handler.add_section(section)

    def add_config_entry(self, section, val_dict):
        for key, value in val_dict.items():
            self.cfg_handler.set(section, key, value)

    def save_config_file(self, filename):
        with open(filename, 'w') as file:
            self.cfg_handler.write(file)


if __name__ == "__main__":
    cfg_mgr = ConfigManager()
    cfg_mgr.create_sections(['general', 'source', 'context-extraction'])
    cfg_mgr.add_config_entry('source', {'files.directory': 'C:\\Users\\ramji\\Documents\\masters\\datasets'
                                                           '\\mindshift\\dataFiles'})
    cfg_mgr.add_config_entry('source', {'files.format': '.*txt'})

    cfg_mgr.add_config_entry('general', {'vocabulary.file': '..\\dataFiles\\business_terms.txt'})
    cfg_mgr.add_config_entry('context-extraction', {'training_data.file': '..\\dataFiles\\KM_articles_titles.xlsx'})
    cfg_mgr.add_config_entry('context-extraction', {'training_data.header.name': 'ArticleTitle'})
    cfg_mgr.save_config_file('default.cfg')
