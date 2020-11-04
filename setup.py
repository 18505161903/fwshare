from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="fwshare",  # 这里是pip项目发布的名称
    version="2.0.1",  # 版本号，数值大的会优先被pip
    keywords=("pip", "fwshare"),
    description="fwshare",
    long_description="fwshare",
    license="fwshare",

    url="https://github.com/18505161903/fwshare",  # 项目相关文件地址，一般是github
    author="392161222",
    author_email="392161222@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]  # 这个项目需要的第三方库
)
