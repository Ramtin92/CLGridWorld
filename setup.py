from setuptools import setup

setup(
    name='gym_clgridworld',
    version='1.0.0',
    packages=['clgridworld', 'clgridworld.action', 'clgridworld.dynamics', 'clgridworld.reward', 'clgridworld.state',
              'clgridworld.visualizer', 'clgridworld.wrapper', 'example', 'example.agents', 'tests', ],
    url='https://github.com/LeroyChristopherDunn/CurriculumLearningGridWorld',
    license='GNU GPLv3',
    author='Leroy Christopher Dunn',
    author_email='social.leroy.c.dunn@gmail.com',
    description='Curriculum Learning Environment for Reinforcement Learning Agents',
    install_requires=['gym==0.12.1', 'numpy', 'matplotlib']
)
