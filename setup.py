import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="termdoro",
  version="2.0.0",
  author="Niyazi Suleymanov",
  author_email="niyazisuleymanov@protonmail.com",
  description="Pomodoro in your terminal",
  long_description=long_description,
  long_description_content_type="text/markdown",
  license="MIT",
  url="https://github.com/niyazisuleymanov/termdoro",
  project_urls={
    "Bug Tracker": "https://github.com/niyazisuleymanov/termdoro/issues"
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ],
  package_data={"termdoro": ["termdoro.mp3", "termdoro.png"]},
  install_requires=["bullet", "python-dateutil", "playsound", "pyfiglet"],
  packages=['termdoro'],
  python_requires=">=3.6",
  entry_points={"console_scripts": ["termdoro=termdoro.main:main"]}
)
