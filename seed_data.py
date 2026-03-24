import uuid
import random
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, Base
from models.models import User, Profile

def seed_db_bulk():
    db = SessionLocal()
    
    first_names_m = ["Rohan", "Karan", "Aarav", "Vikram", "Rahul", "Aditya", "Aryan", "Kabir", "Shaurya", "Dhruv", "Rishabh", "Sameer", "Dev", "Neil", "Yash", "Vivaan", "Advik", "Ayaan", "Ishaan", "Reyansh"]
    first_names_f = ["Priya", "Anya", "Zara", "Kriti", "Neha", "Ananya", "Riya", "Diya", "Tara", "Kiara", "Nisha", "Meera", "Maya", "Sana", "Isha", "Rashi", "Kavya", "Aisha", "Mira", "Sara"]
    last_names = ["Sharma", "Patel", "Singh", "Kapoor", "Ali", "Mehta", "Deshmukh", "Joshi", "Das", "Reddy", "Nair", "Iyer", "Sen", "Gupta", "Malhotra", "Verma", "Rao", "Chauhan", "Bose", "Khanna"]
    locations = ["Mumbai", "Bangalore", "Delhi", "Pune", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Chandigarh"]
    professions = ["Software Engineer", "UX Designer", "Startup Founder", "Data Scientist", "Art History Student", "Marketing Manager", "Architect", "Photographer", "Chef", "Musician", "Writer", "Doctor", "Lawyer", "Teacher", "Pilot"]
    
    bios = [
        "Looking for someone who can match my chaotic energy. 🚀✨",
        "Tech nerd by day, guitarist by night. ☕🌌",
        "Swipe right if you know your Hogwarts house. 🌙🎨",
        "Always hustling but making time for the good things in life. 🏙️🐕",
        "Let's explore the universe together. 📊✨",
        "Coffee addict and weekend trekker. ⛰️☕",
        "Looking for my cosmic match. 🌠",
        "Foodie, traveler, and amateur astronomer. 🔭🍕",
        "Dog parent looking for a co-parent. 🐕❤️",
        "Let's skip the small talk and debate aliens. 👽🛸",
        "Just a star looking for its orbit. ⭐",
        "Introvert who will talk your ear off if we click. 🎧📚",
        "Will cancel plans to stay in and watch anime. 🍿✨",
        "Gym rat with a soft heart. 🏋️‍♂️🥺",
        "Looking for the moon to my sun. 🌞🌜"
    ]

    all_users = []
    
    # Generate 30 Male Profiles
    for i in range(1, 31):
        fn = random.choice(first_names_m)
        ln = random.choice(last_names)
        all_users.append({
            "id": f"dummy_m_{i}_{uuid.uuid4().hex[:4]}",
            "email": f"{fn.lower()}.{ln.lower()}{i}@dummy-jodi.com",
            "full_name": f"{fn} {ln}",
            "avatar_url": f"https://i.pravatar.cc/400?img={i + 10}", # Pravatar images 11-40
            "age": random.randint(21, 35),
            "gender": "male",
            "location": random.choice(locations),
            "profession": random.choice(professions),
            "bio": random.choice(bios),
            "looking_for": "female"
        })

    # Generate 30 Female Profiles
    for i in range(1, 31):
        fn = random.choice(first_names_f)
        ln = random.choice(last_names)
        all_users.append({
            "id": f"dummy_f_{i}_{uuid.uuid4().hex[:4]}",
            "email": f"{fn.lower()}.{ln.lower()}{i}@dummy-jodi.com",
            "full_name": f"{fn} {ln}",
            "avatar_url": f"https://i.pravatar.cc/400?img={i + 40}", # Pravatar images 41-70
            "age": random.randint(21, 35),
            "gender": "female",
            "location": random.choice(locations),
            "profession": random.choice(professions),
            "bio": random.choice(bios),
            "looking_for": "male"
        })

    # Shuffle to mix them up
    random.shuffle(all_users)

    count = 0
    for data in all_users:
        # Avoid overriding if email exists
        if db.query(User).filter(User.email == data["email"]).first():
            continue
            
        user = User(
            id=data["id"],
            email=data["email"],
            full_name=data["full_name"],
            avatar_url=data["avatar_url"]
        )
        db.add(user)
        
        profile = Profile(
            id=str(uuid.uuid4()),
            user_id=user.id,
            name=data["full_name"],
            age=data["age"],
            gender=data["gender"],
            location=data["location"],
            profession=data["profession"],
            bio=data["bio"],
            avatar_url=data["avatar_url"],
            looking_for=data["looking_for"]
        )
        db.add(profile)
        count += 1
        
    db.commit()
    print(f"✅ Successfully injected {count} new dummy profiles into the database!")
    db.close()

if __name__ == "__main__":
    seed_db_bulk()
