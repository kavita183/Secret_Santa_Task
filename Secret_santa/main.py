import csv
import random
from collections import defaultdict

class SecretSantaAssigner:
    def __init__(self, employees_file, previous_assignments_file, output_file):
        self.employees_file = employees_file
        self.previous_assignments_file = previous_assignments_file
        self.output_file = output_file
        self.employees = []
        self.previous_assignments = {}
        
    def read_employees(self):
        """Reads employee data from CSV and stores in a list."""
        try:
            with open(self.employees_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.employees = [row for row in reader]
        except FileNotFoundError:
            print(f"Error: File {self.employees_file} not found.")
            exit(1)
        
    def read_previous_assignments(self):
        """Reads last year's assignments to avoid repetition."""
        try:
            with open(self.previous_assignments_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.previous_assignments[row['Employee_EmailID']] = row['Secret_Child_EmailID']
        except FileNotFoundError:
            print(f"Warning: Previous assignments file {self.previous_assignments_file} not found. Proceeding without it.")

    def assign_secret_santa(self):
        """Assigns each employee a unique secret child while meeting constraints."""
        available_children = set(emp['Employee_EmailID'] for emp in self.employees)
        random.shuffle(self.employees)  # Shuffle for randomness
        assignments = {}

        for employee in self.employees:
            emp_email = employee['Employee_EmailID']
            possible_children = list(available_children - {emp_email})
            if emp_email in self.previous_assignments:
                previous_child = self.previous_assignments[emp_email]
                if previous_child in possible_children:
                    possible_children.remove(previous_child)
            
            if not possible_children:
                print("Error: No valid Secret Santa assignment found. Try again.")
                exit(1)
            
            chosen_child = random.choice(possible_children)
            assignments[emp_email] = chosen_child
            available_children.remove(chosen_child)

        return assignments

    def write_output(self, assignments):
        """Writes the final Secret Santa assignments to a CSV file."""
        with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for emp in self.employees:
                secret_child_email = assignments[emp['Employee_EmailID']]
                secret_child = next(e for e in self.employees if e['Employee_EmailID'] == secret_child_email)
                writer.writerow({
                    'Employee_Name': emp['Employee_Name'],
                    'Employee_EmailID': emp['Employee_EmailID'],
                    'Secret_Child_Name': secret_child['Employee_Name'],
                    'Secret_Child_EmailID': secret_child['Employee_EmailID']
                })

    def run(self):
        """Executes the full Secret Santa process."""
        self.read_employees()
        self.read_previous_assignments()
        assignments = self.assign_secret_santa()
        self.write_output(assignments)
        print(f"Secret Santa assignments saved to {self.output_file}")

# Example usage:
santa = SecretSantaAssigner('emp_table.csv', 'previous_assignments.csv', 'output.csv')
santa.run()
