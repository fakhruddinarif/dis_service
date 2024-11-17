import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seeder.user_seeder import seed_users, seed_accounts

# Seed users and accounts
seed_users()
seed_accounts()