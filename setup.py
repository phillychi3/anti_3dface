import setuptools

setuptools.setup(
    name='anti3dface',
    version='1',
    author="phillychi3",
    author_email="phillychi3@gmail.com",
    description="anti 3d face",
    long_description="""# anti3dface""",
    long_description_content_type='text/markdown',
    url="https://github.com/phillychi3/anti_3dface",
    packages=setuptools.find_packages(),
    package_data={
        'anti3dface': ['GenWanMin-L.ttc'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'opencv-python',
        'numpy',
        'Pillow',
    ],
    python_requires='>=3',
    
 )