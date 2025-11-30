def vacuum_world():
    goal_state = {'A': '0', 'B': '0'}
    cost = 0
    location_input = input("Enter Location of Vacuum: ")  
    status_input = input("Enter status of " + location_input + ": ")  
    status_input_complement = input("Enter status of other room: ")
    
    print("Initial Location Condition: " + str(goal_state))
    
    if location_input == 'A':
      
        print("Vacuum is placed in Location A")
        if status_input == '1':
            print("Location A is Dirty.")
            
            goal_state['A'] = '0'
            cost += 1  
            print("Cost for CLEANING A: " + str(cost))
            print("Location A has been Cleaned.")
            
            if status_input_complement == '1':
                
                print("Location B is Dirty.")
                print("Moving right to Location B.")
                cost += 1  
                print("COST for moving RIGHT: " + str(cost))
                
                goal_state['B'] = '0'
                cost += 1  
                print("COST for SUCK: " + str(cost))
                print("Location B has been Cleaned.")
            else:
                print("Location B is already clean. No action.")
        else:
            print("Location A is already clean.")
            if status_input_complement == '1':  
                print("Location B is Dirty.")
                print("Moving right to Location B.")
                cost += 1
                print("COST for moving RIGHT: " + str(cost))
               
                goal_state['B'] = '0'
                cost += 1  
                print("Cost for SUCK: " + str(cost))
                print("Location B has been Cleaned.")
            else:
                print("Location B is already clean. No action.")
    
    else:
        print("Vacuum is placed in Location B")
        
        if status_input == '1':
            print("Location B is Dirty.")
            
            goal_state['B'] = '0'
            cost += 1 
            print("COST for CLEANING B: " + str(cost))
            print("Location B has been Cleaned.")
            
            if status_input_complement == '1':
              
                print("Location A is Dirty.")
                print("Moving left to Location A.")
                cost += 1  
                print("COST for moving LEFT: " + str(cost))
                
                goal_state['A'] = '0'
                cost += 1  
                print("COST for SUCK: " + str(cost))
                print("Location A has been Cleaned.")
            else:
                print("Location A is already clean. No action.")
        else:
            print("Location B is already clean.")
            if status_input_complement == '1': 
                print("Location A is Dirty.")
                print("Moving left to Location A.")
                cost += 1  
                print("COST for moving LEFT: " + str(cost))
                
                goal_state['A'] = '0'
                cost += 1  
                print("Cost for SUCK: " + str(cost))
                print("Location A has been Cleaned.")
            else:
                print("Location A is already clean. No action.")
    
   
    print("GOAL STATE: ")
    print(goal_state)
    print("Performance Measurement: " + str(cost))


vacuum_world()