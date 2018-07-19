"""The main execution script for this package for testing."""
# from gym_super_mario_bros._app.cli import main


# # execute the main entry point of the CLI
# main()


from gym_super_mario_bros import SuperMarioBrosEnv
from nes_py._app.play_human import play


env = SuperMarioBrosEnv()
play(env, fps=60)
