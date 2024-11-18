import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seeder.user_seeder import seed_users, seed_accounts
from seeder.photo_seeder import seed_sell_photos, seed_post_photos

# Seed users and accounts
seed_users()
seed_accounts()

# Seed photos post and sell
seed_sell_photos()
seed_post_photos()