# lib/helpers.py
from models.owner import Owner
from models.dog import Dog



def get_owners():
    return Owner.get_all()

def add_owner():
    name = input("Enter the owner's name: ")
    try:
        owner = Owner.create(name)
        print(f'{owner.name} has been added!')
        return owner
    except Exception as exc:
        print("Error creating owner: ", exc)

def delete_owner(owner):
    for dog in owner.dogs():
        dog.delete()
    owner.delete()

def add_dog(owner):
    name = input(f"Enter name for {owner.name}'s new dog: ")
    age = input(f"Enter age for {owner.name}'s new dog: ")
    breed = input(f"Enter breed for {owner.name}'s new dog: ")
    try:
        dog = Dog.create(name, int(age), breed, owner.id)
        print(f'{dog.name} has been added!')
        return dog
    except Exception as exc:
        print("Error creating dog: ", exc)

def update_dog(dog):
    name_input = input(f"Enter name for {dog.name}'s to change or hit <enter> to leave it as is: ")
    if name_input != '':
        dog.name = name_input
    age_input = input(f"Enter age for {dog.age}'s to change or hit <enter> to leave it as is: ")
    if age_input != '':
        dog.age = int(age_input)
    breed_input = input(f"Enter breed for {dog.breed}'s to change or hit <enter> to leave it as is: ")
    if breed_input != '':
        dog.breed = breed_input
    try:
        dog.update()
        print(f'{dog.name} has been updated!')
        return dog
    except Exception as exc:
        print("Error updating dog: ", exc)

def delete_dog(dog):
    dog.delete()

def exit_program():
    blank()
    print("Goodbye!")
    exit()

def list_members(members):
    print('****************')
    blank()
    for i, m in enumerate(members):
        print(f"{i+1}. {m.name}")
    blank()
    print('****************')
    
def display_owner(owner):
    blank()
    print(owner.name)
    blank()
    print (f"{owner.name}'s Dogs:")
    list_members(owner.dogs())

def display_dog_details(owner, dog):
    blank()
    print(f"Here are the details on {owner.name}'s selected dog:")
    print("~~~~~~~~~~~~~~~")
    print(f"     Name: {dog.name}")
    print(f"     Age: {dog.age}")
    print(f"     Breed: {dog.breed}")
    print("~~~~~~~~~~~~~~~")
    blank()

def blank():
    print("")


