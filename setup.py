from setuptools import setup, find_packages

setup(
    name='shape-test',
    version='1.0.0',
    author='Mariana Franz',
    author_email='franzmariana81@gmail.com',
    description='Tech Case for Shape Interview',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'py4j',
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
    ],
    entry_points={
        'console_scripts': [
            'my_script=main.main:main',
        ],
    },
    package_data={'equipment': ['data\equipment.json'], 'equipment_sensor': ['data\equipment_sensors.csv'],
                  'equipment_failure_sensors': ['data\equipment_failure_sensors.txt']}
)