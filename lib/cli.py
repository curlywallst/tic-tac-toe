# lib/cli.py

from helpers import (
    blank,
    exit_program,
    list_members,
    display_owner,
    display_dog_details,
    add_owner,
    get_owners,
    add_dog,
    delete_owner,
    delete_dog,
    update_dog
)

def main():
    greet()
    select_owner()

def select_owner():
    choice = ''
    while choice.lower() != 'e':
        print("Your Owners:")
        list_members(get_owners())
        select_owner_menu()
        choice = input("> ")
        if choice.isnumeric() and int(choice) in range(1, len(get_owners())+1):
            owner = get_owners()[int(choice) - 1]
            selected_owners_dogs(owner)
        elif choice.lower() == "a":
            add_owner()
            list_members(get_owners())
            select_owner_menu()
        elif choice.lower() != "e":
            print("Invalid choice")
    exit_program()


def selected_owners_dogs(owner):
    choice = ''
    while choice.lower() != 'b':
        display_owner(owner)
        owners_dogs_menu()
        choice = input("> ")
        if choice.isnumeric() and int(choice) in range(1, len(owner.dogs())+1):
            dog = owner.dogs()[int(choice) - 1]
            selected_dog(owner, dog)
        elif choice.lower() == "a":
            add_dog(owner)
            display_owner(owner)
            owners_dogs_menu()
        elif choice.lower() == "d":
            delete_owner(owner)
            choice = 'b'
        elif choice.lower() == "e":
            exit_program()
        elif choice.lower() != "b":
            print("Invalid choice")

def selected_dog(owner, dog):
    choice = ''
    while choice.lower() != 'b':
        display_dog_details(owner, dog)
        dog_menu()
        choice = input("> ")
        if choice.lower() == "e":
            exit_program()
        elif choice.lower() == "d":
            delete_dog(dog)
            choice = 'b'
        elif choice.lower() == 'u':
            update_dog(dog)
        elif choice.lower() != "b":
            print("Invalid choice")

# Menu messaging

def menu():
    blank()
    print("Please choose from the following:")
    blank()
    print("     Type O or o to see the Owners")
    print("     Type E or e to Exit")
    blank()

def select_owner_menu():
    blank()
    print("Please select the number of the owner to see their details")
    print('                 or')
    print("Type A or a to add a new owner")
    print("Or type E or e to exit")
    blank()

def owners_dogs_menu():
    blank()
    print("Please choose from the following:")
    blank()
    print("     Type the number of the dog to see its details")
    print('                 or')
    print("     Type A or a to add a new dog for this owner")
    print("     Type D or d to delete this owner")
    print("     Type B or b to go back to the previous menu")
    print("     Or type E or e to exit") 
    blank()

def dog_menu():
    blank()
    print("Please choose from the following:")
    blank()
    print("     Type D or d to delete this dog")
    print("     Type U or u to update this dog's details")
    print("     Type B or b to go back to the previous menu")
    print("     Or type E or e to exit")  
    blank()  

def greet():
    print('Hello and welcome to the dog walker manager!')
    print('Use this app to manage the owners and their dogs in your Dog Walking Business')
    print(' ')


if __name__ == "__main__":
    main()
