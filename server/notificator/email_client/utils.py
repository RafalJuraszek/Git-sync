from string import Template


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def ready_template():
    template_file_content = "Dear ${PERSON_NAME}, \n" + "I'm sending You  " + \
                            "emergency backups of ${MASTER_REPO} in case of losing acces to this repository.\n" \
                            + "${BACKUP_REPOS_LIST} \n" + "Have a great day! \n" + "Yours github friend\n"
    return Template(template_file_content)
