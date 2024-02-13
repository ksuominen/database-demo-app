import queries


def print_instructions():
    print("1: Print all persons")
    print("2: Print certificate holders")
    print("3: Add a person")
    print("q: quit")


def start():
    while True:
        print_instructions()
        op = input("What do you want to do? ")
        if op == "1":
            queries.all_rows_from_table("person")
        elif op == "2":
            cert = input("What certificate? ")
            try:
                queries.get_certificate_holders(cert)
            except Exception:
                print("Sorry, something went wrong")
        elif op == "3":
            name = input("Name: ")
            age = input("Age: ")
            try:
                age = int(age)
            except Exception:
                print("Sorry, the age needs to be a number")
                continue
            student = input("Is the person a student? (y/n) ")
            if student.lower() == "y":
                student = "True"
            elif student.lower() == "n":
                student = "False"
            else:
                print("Incorrect answer")
                continue
            queries.add_person(name, age, student)
        elif op.lower() == "q":
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    start()
