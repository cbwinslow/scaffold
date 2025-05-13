from setuptools import setup

setup(
    name='cbw-scaffold',
    version='0.1.1',
    py_modules=['scaffold'],
    entry_points={
        'console_scripts': [
            'scaffold=scaffold:main',
        ],
    },
    author='Blaine Winslow',
    author_email='blaine.winslow@gmail.com',
    description='Smart directory/file scaffolding tool using a .scaffold, .json, or .yaml file.',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/cbwinslow/scaffold',
    install_requires=['pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
)
