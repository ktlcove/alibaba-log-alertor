import fastentrypoints

from setuptools import setup, find_packages

version = '0.0.2'

requirements = [
    'iso8601',
    'aliyun-log-python-sdk',
    'kube_admission @ git+https://github.com/ktlcove/kube-admission.git',
]

entry_points = {
    "console_scripts": [
        'run_http_server = alibaba_log_alertor:http_main',
    ]
}

setup(name='alibaba-log-alertor',
      version=version,
      description="provide by ktlcove",
      long_description="",
      long_description_content_type='text/markdown',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      url='https://github.com/ktlcove/kube-admission.git',
      author='ktlove',
      author_email='ktl_cove@126.com',
      packages=find_packages(exclude=('test', 'doc',)),
      include_package_data=True,
      zip_safe=False,
      entry_points=entry_points,
      install_requires=requirements,
      )
