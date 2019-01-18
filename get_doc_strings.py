import re

from paragraph_generator import AnswerChecker, WordLists, ParagraphsGenerator

TAB = '    '


def get_version():
    with open('setup.py', 'r') as f:
        text = f.read()
    return re.search(r"(?<=VERSION = ')[0-9.]+", text).group()


def set_version():
    with open('README.rst', 'r') as f:
        readme_text = f.read()
    new_text = re.sub(r"(?<=paragraph_generator v)[0-9.]+", get_version(), readme_text)
    with open('README.rst', 'w') as f:
        f.write(new_text)


def get_init_docs(class_):
    class_heading = f"\n:class: {class_.__name__}\n\n{TAB}:method __init__:\n"
    types = get_types(class_.__init__)
    docs = get_docs(class_.__init__)
    if types:
        class_heading += f'{TAB}{TAB}:types: {types}\n'

    if docs:
        class_heading += f'{TAB}{TAB}:docs: {docs}\n'
    else:
        class_heading += '\n'

    return class_heading


def get_method_docs(class_):
    methods = []
    for method_name in dir(class_):
        if not method_name.startswith('_'):
            method = getattr(class_, method_name)
            rst_doc = f'{TAB}:method {method_name}:\n'
            types = get_types(method)
            docs = get_docs(method)
            if types:
                rst_doc += f'{TAB}{TAB}:types: {types}\n'
            if docs:
                rst_doc += f'{TAB}{TAB}:docs: {docs}\n'
            methods.append(rst_doc)
    return '\n'.join(methods)


def get_docs(method):
    return get_documentation(method, '__doc__')


def get_types(method):
    return get_documentation(method, '__annotations__')


def get_documentation(method, type_str):
    try:
        documentation = getattr(method, type_str)
    except AttributeError:
        documentation = None
    return documentation if documentation else None


def insert_docs():
    classes = (AnswerChecker, WordLists, ParagraphsGenerator)
    doc_strs = []
    for el in classes:
        doc_str = get_init_docs(el) + get_method_docs(el)
        doc_strs.append(doc_str)

    block_statement = '\n\n'.join(doc_strs)
    block_statement = block_statement.replace('\n', f'\n{TAB}')
    replace_str = 'Basic Documentation:\n--------------------\n\n' + block_statement

    with open('README.rst', 'r') as f:
        text = f.read()

    new_text = text[:text.find('Basic Documentation')] + replace_str
    # print(new_text)

    with open('README.rst', 'w') as f:
        f.write(new_text)


set_version()
insert_docs()
