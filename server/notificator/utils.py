from string import Template


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def ready_template():
    template_file_content = "Dear ${PERSON_NAME}, \n" + "This is a test message. \n" + "Have a great weekend! \n" + "${BACKUP_REPOS_LIST} \n" + "Yours Truly\n"
    return Template(template_file_content)
