from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='paragraph_generator',
      version='1.0',
      description='sentence generator',
      long_description=readme(),
      keywords='',
      url='http://github.com/eric-s-s/paragraph_generator',
      author='Eric Shaw',
      author_email='shaweric01@gmail.com',
      license='MIT',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
      ],
      packages=find_packages(include=['paragraph_generator.*', 'paragraph_generator']),
      package_data={
          '': ['data/*.csv']
      },
      include_package_data=True,
      zip_safe=False)
