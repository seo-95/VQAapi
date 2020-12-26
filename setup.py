import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='VQAtools',
     version='0.1',
     author="Matteo A. Senese",
     description="A VQA helper developed by"
                 "Aishwarya Agrawal and packaged by"
                 "Matteo A. Senese",
     url="https://github.com/seo-95/VQA",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )