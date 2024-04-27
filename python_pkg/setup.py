from setuptools import setup, find_packages

setup(
    name='persona_link', 
    version='0.1.0', 
    description='Give a face and voice to your AI Agents',
    author='Abhinav Dayal',
    author_email='abhinav@enligence.com',
    long_description=open('README.md').read(),
    
    install_requires=[
        'aiohttp',
        'pydantic',
        'aiofiles',
    ],
    
    # Optional dependencies
    extras_require={
        'azure' : ["azure-storage-blob"],
        'postgres' : ["tortoise-orm", "asyncpg"],
        'sqlite' : ["tortoise-orm"],
        'azure-tts' : ["azure-cognitiveservices-speech"]
    },
    
    packages=find_packages(),
)