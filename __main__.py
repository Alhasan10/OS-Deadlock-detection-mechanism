import csv

#In this function it should read from files .csv
def read_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # This is to skip the first row of the file .csv
        data = [([row[0]] + list(map(int, row[1:]))) for row in csv_reader] # This is to read the remaining rows in file .csv
    return data

# In this function we check Detection Algorithm and in the attributes i pass data of files.csv
def detect_deadlock(allocation, request, available):
    num_processes = len(allocation) # To get the number of processes
    num_resources = len(allocation[0]) - 1 # To get the number of resources & sub 1 for process name
    #print(num_resources)
    work = [available[0][i] for i in range(num_resources)] # Put availabel resources in work
    finish = [False] * num_processes # A boolean value to check if the process has finished
    safe_sequence = [] # An empty list to add safe sequance processes in it

    # Loop to check if Im still contains all processes
    while len(safe_sequence) < num_processes:
        found = False # Flag to define every process in the first false to check it after if chould it work after
        # For loop to check each process
        for i in range(num_processes):
            # Check process still not finish
            if not finish[i]:
                current_req = [request[i][j+1] for j in range(num_resources)] # A list we put in it request resources
                # Check if all the request resources are less than or equal to the available resources
                if all(current_req[j] <= int(work[j]) for j in range(num_resources)):
                    print(f"Process executed: {allocation[i][0]}") # Print the process is executed
                    work = [int(work[j]) + allocation[i][j+1] for j in range(num_resources)] # Update the available resources by adding the allocation of the current process
                    print(f"Available resources: {' '.join(map(str, work))}")
                    finish[i] = True # Process finshed
                    safe_sequence.append(allocation[i][0]) # Append the current process to the safe sequence
                    found = True # Process is done
                    break

                else:
                    print(f"Process: {allocation[i][0]} can't execute, move to next process")

        # Is there deadlock
        if not found:
            deadlock_processes = [allocation[i][0] for i in range(num_processes) if not finish[i]]
            return False, deadlock_processes, []

    print("\nFinal available recources:" ,work)
    return True, safe_sequence, []

# REad data from file .csv using finction read_csv
allocation_matrix = read_csv('Allocation.csv')
request_matrix = read_csv('Request.csv')
available_matrix = read_csv('Available.csv')

# Detect deadlock
safe_state, safe_sequence, deadlock_processes = detect_deadlock(allocation_matrix, request_matrix, available_matrix)

if safe_state:
    print("Safe State")
    print("Safe sequence:", ' '.join(safe_sequence))
else:
    print("Deadlock detected, Please try agin !!")
