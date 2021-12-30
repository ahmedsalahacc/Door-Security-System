from src.seeder.logItemSeeder import logItemSeeder
from src.seeder.userSeeder import userSeeder


def seed():
    userSeeder()
    logItemSeeder()
