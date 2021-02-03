from setuptools import setup, find_packages

package_path = "."

with open('{package_path}/requirements.txt'.format(package_path=package_path), 'r') as f:
    INSTALL_REQUIRES = f.readlines()

try:
    with open('{package_path}/requirements-dev.txt'.format(package_path=package_path), 'r') as f:
        TESTS_REQUIRE = f.readlines()
except:
        TESTS_REQUIRE = None

try:
    with open("README.md", "r") as readmefile:
        long_description = readmefile.read()
except:
        long_description = None

setup(
    name='envio_email_api',
    version='1.31.1',
    packages=find_packages(include=['envio_email_api*']),
    description='Envio Email API Angular',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/al118345/proyecto_api_envio_email',
    license='AGPL',
    author='https://1938.com.es/',
    include_package_data=True,
    author_email='1938web@gmail.com',
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    namespace_packages=['envio_email_api'],
)
