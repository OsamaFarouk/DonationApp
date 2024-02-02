import re
from datetime import datetime

USERS_FILE = "./Users.txt"
PROJECTS_FILE = "./Projects.txt"

# User class to store user information
class User:
    def __init__(self, first_name, last_name, email, password, mobile, is_active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile = mobile
        self.is_active = is_active


# Project class to store project information
class Project:
    def __init__(self, title, details, target_amount, start_date, end_date, creator, donors, funds_collected, is_closed):
        self.title = title
        self.details = details
        self.target_amount = target_amount
        self.start_date = start_date
        self.end_date = end_date
        self.creator = creator
        self.donors = donors
        self.funds_collected = funds_collected
        self.is_closed = is_closed
        self.status = "Open" if not is_closed else "Closed"

    
    def donate(self, amount, user):
        print(f"Current Date: {datetime.now()}")
        print(f"Project End Date: {self.end_date}")
        print(f"Target Amount: {self.target_amount}")
        print(f"Funds Collected: {self.funds_collected}")

        if not self.is_closed and datetime.now().date() < self.end_date.date() and self.target_amount > self.funds_collected:
            self.donors.append((user, amount))
            self.funds_collected += amount
            print(f"Donation of {amount} EGP added successfully.")
            if self.funds_collected >= self.target_amount:
                self.is_closed = True
                self.status = "Closed - Reached Target"
                print(f"The project '{self.title}' has reached its target amount.")
            elif datetime.now().date() > self.end_date.date():
                self.is_closed = True
                self.status = "Closed"
                print(f"The project '{self.title}' has reached its end date.")
            else:
                self.status = "Open"
        else:
            self.status = "Closed - End Date Passed or Reached Target"
            print("Donation cannot be accepted. Project has ended or reached its target amount.")

# Authentication System
class AuthenticationSystem:
    def is_valid_email(email):
      pattern = r'^\S+@\S+\.\S+$'
      match = re.match(pattern, email)
      return bool(match)
    
    def is_valid_egyptian_phone_number(phone_number):
      pattern = r'^01[0-2]\d{8}$'
      match = re.match(pattern, phone_number)
      return bool(match)
      
    def is_valid_password(password):
      if len(password) < 8:
         return False
      has_letter = any(char.isalpha() for char in password)
      has_digit = any(char.isdigit() for char in password)
      return has_letter and has_digit  
    @staticmethod
    def register():
        print("Registration:")
        first_name = input("First name: ")
        while not first_name or not first_name.isalpha():
            first_name = input("Please Enter Valid First Name!!!")
            first_name = input("First name: ")
        last_name = input("Last name: ")
        while not last_name or not last_name.isalpha():
            last_name = input("Please Enter Valid Last Name!!!")
            last_name = input("Last name: ")
        email = input("Email: ")
        # Validate Email
        while not AuthenticationSystem.is_valid_email(email):
            email = input("Please Enter A Valid Email !!!")
            email = input("Email: ")
        password = input("Password: ")
        while not AuthenticationSystem.is_valid_password(password):
            password = input("Password must be at least 8 characters and numbers.")
            password = input("Password: ")
        confirm_password = input("Confirm password: ")
        while confirm_password != password:
            confirm_password = input("Confirm_Password Not Equal Password!!! Enter It Again..")
            confirm_password = input("Confirm password: ")
        mobile = input("Mobile phone: ")
        # Validate Egyptian phone numbers
        while not AuthenticationSystem.is_valid_egyptian_phone_number(mobile):
            mobile = input("Please Enter A Valid Egyptian Phone Number !!!")
            mobile = input("Mobile phone: ")

        # Validate Egyptian phone numbers
        if not re.match(r'^01[0-9]{9}$', mobile):
            print("Invalid mobile number. Please enter a valid Egyptian phone number.")
            return

        users = AuthenticationSystem.read_users_file()
        # Check if the user already exists
        for user in users:
            if user.email == email:
                print("User already exists. Please login.")
                return

        new_user = User(first_name, last_name, email, password, mobile, False)
        users.append(new_user)
        AuthenticationSystem.write_users_file(users)

        print("Registration successful. Please log in.")

    @staticmethod
    def login():
        print("Login:")
        email = input("Email: ")
        password = input("Password: ")

        users = AuthenticationSystem.read_users_file()

        for user in users:
            if user.email == email and user.password == password:
                user.is_active = True
                AuthenticationSystem.write_users_file(users)
                print("Login successful.")
                return

        print("Invalid email or password.")

    @staticmethod
    def read_users_file():
        users = []
        try:
            with open(USERS_FILE, "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 6:  # Check if the data has the expected number of elements
                        first_name, last_name, email, password, mobile, is_active_str = data
                        is_active = is_active_str.strip().lower() == 'true'
                        users.append(User(first_name, last_name, email, password, mobile, is_active))
        except FileNotFoundError:
            print('File not found')
        return users


    @staticmethod
    def write_users_file(users):
        with open(USERS_FILE, "w") as file:
            for user in users:
                file.write(f"{user.first_name},{user.last_name},{user.email},{user.password},{user.mobile},{user.is_active}\n")


# Projects system
class ProjectManager:
    @staticmethod
    def create_project(user):
        print("Create Project:")

        # Validate Title
        while True:
            title = input("Title: ")
            if not title or not title.isalpha():
                print("Invalid input. Title must contain only alphabetic characters. Please try again.")
            else:
                break

        # Validate Details
        while True:
            details = input("Details: ")
            if not details or not details.replace(" ", "").isalpha():
                print("Invalid input. Details must contain only alphabetic characters. Please try again.")
            else:
                break

        # Validate Target Amount
        while True:
            try:
                target_amount = float(input("Total target (e.g., 250000 EGP): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number for the target amount.")

        # Validate Date Format
        while True:
            start_date_str = input("Start date (YYYY-MM-DD): ")
            end_date_str = input("End date (YYYY-MM-DD): ")
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                if start_date <= end_date:
                    break
                else:
                    print("End date must be equal to or after the start date. Please try again.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        projects = ProjectManager.read_projects_file()

        # Create new project
        new_project = Project(title, details, target_amount, start_date, end_date, user, [], 0, False)
        new_project.is_closed = False  # Ensure is_closed is set to False when creating a new project
        projects.append(new_project)
        ProjectManager.write_projects_file(projects)

        print("Project created successfully.")

    
    @staticmethod
    def view_projects(user):
        print("\nAll Projects:")
        projects = ProjectManager.read_projects_file()

        for project in projects:
            # Update project status based on the current date, start date, and end date
            today = datetime.now().date()
            start_date = project.start_date.date()
            end_date = project.end_date.date()

            if not project.is_closed:
                if start_date > today:
                    project.status = f"Closed : Will open on {start_date}"
                elif start_date <= today <= end_date:
                    project.status = "Open"
                else:
                    project.is_closed = True
                    if project.funds_collected >= project.target_amount:
                        project.status = "Closed - Reached funds Target"
                    else:
                        project.status = "Closed"
                    ProjectManager.write_projects_file(projects)

        # Check if there are no available open projects
        open_projects = [project for project in projects if not project.status.startswith("Closed")]
        if not open_projects:
            print("\nAll Projects are Closed:")
            for i, project in enumerate(projects, 1):
                print(f"{i}. Title: {project.title}, Status: {project.status}")
            go_back_option = input("Do you want to go back to the main menu? (yes/no): ").lower()
            if go_back_option == 'yes':
                return

        for i, project in enumerate(projects, 1):
            print(f"{i}. Title: {project.title}, Creator: {project.creator.first_name} {project.creator.last_name}, Status: {project.status}")

        try:
            project_index = int(input("Enter the number of the project to view details: ")) - 1
            if 0 <= project_index < len(projects):
                selected_project = projects[project_index]

                # Display project details
                print(f"Details of Project: {selected_project.title}")
                print(f"Creator: {selected_project.creator.first_name} {selected_project.creator.last_name}")
                print(f"Details: {selected_project.details}")
                print(f"Target Amount: {selected_project.target_amount} EGP")
                print(f"Start Date: {selected_project.start_date.strftime('%Y-%m-%d')}")
                print(f"End Date: {selected_project.end_date.strftime('%Y-%m-%d')}")
                print(f"Funds Collected: {selected_project.funds_collected} EGP")
                print(f"Status: {selected_project.status}")

                # Check if the project is closed
                if selected_project.status.startswith("Closed"):
                    print("This project is closed. Donations are not accepted.")
                else:
                    donate_option = input("Do you want to donate to this project? (yes/no): ").lower()
                    if donate_option == 'yes':
                        donation_amount = float(input("Enter the donation amount: "))
                        selected_project.donate(donation_amount, user)
                        ProjectManager.write_projects_file(projects)  # Write updated project data to file

            else:
                print("Invalid project number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


    @staticmethod
    def edit_project(user):
        print("Edit Project:")
        projects = ProjectManager.read_projects_file()

        # Display projects created by the user
        user_projects = [project for project in projects if project.creator.email.lower() == user.email.lower()]
        if not user_projects:
            print("You haven't created any projects to edit.")
            return

        print("\nYour Projects:")
        for i, project in enumerate(user_projects, 1):
            print(f"{i}. Title: {project.title}, Status: {'Closed' if project.is_closed else 'Open'}")

        try:
            project_index = int(input("Enter the number of the project to edit: ")) - 1
            if 0 <= project_index < len(user_projects):
                project_to_edit = user_projects[project_index]

                # Validate if the project is closed
                if project_to_edit.is_closed:
                    print("Cannot edit a closed project.")
                    return

                print("Editing project:")
                project_to_edit.title = input("New Title: ")
                project_to_edit.details = input("New Details: ")
                project_to_edit.target_amount = float(input("New Total target (e.g., 250000 EGP): "))
                project_to_edit.start_date = datetime.strptime(input("New Start date (YYYY-MM-DD): "), "%Y-%m-%d")
                project_to_edit.end_date = datetime.strptime(input("New End date (YYYY-MM-DD): "), "%Y-%m-%d")
                ProjectManager.write_projects_file(projects)
                print("Project edited successfully.")
            else:
                print("Invalid project number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    @staticmethod
    def delete_project(user):
        print("Delete Project:")

        projects = ProjectManager.read_projects_file()

        if not projects:
            print("There are no projects to delete.")
            return

        # Display projects created by the user
        user_projects = [project for project in projects if project.creator.email.lower() == user.email.lower()]
        if not user_projects:
            print("You haven't created any projects delete.")
            return

        print("\nYour Projects:")
        for i, project in enumerate(user_projects, 1):
            print(f"{i}. Title: {project.title}, Status: {'Closed' if project.is_closed else 'Open'}")

        try:
            project_index = int(input("Enter the number of the project to delete: ")) - 1
            if 0 <= project_index < len(user_projects):
                project_to_delete = user_projects[project_index]

                # Check if the project is closed
                if project_to_delete.is_closed:
                    print("Cannot delete a closed project.")
                    return

                projects.remove(project_to_delete)
                ProjectManager.write_projects_file(projects)
                print(f"Project '{project_to_delete.title}' deleted successfully.")
            else:
                print("Invalid project number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    @staticmethod
    def read_projects_file():
        projects = []
        try:
            with open(PROJECTS_FILE, "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) >= 9:
                        users = AuthenticationSystem.read_users_file()
                        creator_email = data[5].strip().lower()
                        creator = next((user for user in users if user.email.lower() == creator_email), None)
                        funds_collected = float(data[7]) if data[7] else 0.0
                        is_closed = data[8].strip() == 'True'
                        # Convert the end date string to a datetime object
                        end_date = datetime.strptime(data[4], "%Y-%m-%d")
                        projects.append(Project(data[0], data[1], float(data[2]), datetime.strptime(data[3], "%Y-%m-%d"),
                                                end_date, creator, [], funds_collected, is_closed))
        except FileNotFoundError:
            print('File not found')
        return projects


    @staticmethod
    def write_projects_file(projects):
        with open(PROJECTS_FILE, "w") as file:
            for project in projects:
                file.write(f"{project.title},{project.details},{project.target_amount},"
                        f"{project.start_date.strftime('%Y-%m-%d')},{project.end_date.strftime('%Y-%m-%d')},"
                        f"{project.creator.email},,{project.funds_collected},{project.is_closed}\n")


# Main Program
def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option (1/2/3): ")

        if choice == '1':
            AuthenticationSystem.register()
        elif choice == '2':
            AuthenticationSystem.login()
            users = AuthenticationSystem.read_users_file()
            current_user = next(user for user in users if user.is_active)
            while True:
                print("\n1. Create Project")
                print("2. View all Projects and donate")
                print("3. Edit Project")
                print("4. Delete Project")
                print("5. Logout")
                sub_choice = input("Select an option (1/2/3/4/5): ")

                if sub_choice == '1':
                    ProjectManager.create_project(current_user)
                elif sub_choice == '2':
                    ProjectManager.view_projects(current_user)
                elif sub_choice == '3':
                    ProjectManager.edit_project(current_user)
                elif sub_choice == '4':
                    ProjectManager.delete_project(current_user)
                elif sub_choice == '5':
                    print("Logging out.")
                    current_user.is_active = False
                    AuthenticationSystem.write_users_file(users)
                    break
                else:
                    print("Invalid option. Please try again.")
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
