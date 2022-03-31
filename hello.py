import streamlit as st
import numpy as np
import pandas as pd

import constraint
import math

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

#To print center required per day
def print_solutions2(sols): 
    st.write("Center Rent/Day:")
    st.write("""
    CR-1: {0:d} * RM 100 \n
    CR-2: {1:d} * RM 200 \n
    CR-3: {2:d} * RM 500 \n
    CR-4: {3:d} * RM 800 \n
    CR-5: {4:d} * RM 1200 \n
    """.format(sols["CR-1"], sols["CR-2"], sols["CR-3"], sols["CR-4"], sols["CR-5"]))

#To print center required on last day
def print_solutions_lastDay(sols2): 
    st.write("Center Rent Last Day:")
    st.write("""
    CR-1: {0:d} * RM 100 \n
    CR-2: {1:d} * RM 200 \n
    CR-3: {2:d} * RM 500 \n
    CR-4: {3:d} * RM 800 \n
    CR-5: {4:d} * RM 1200 \n
    """.format(sols2["CR-1"], sols2["CR-2"], sols2["CR-3"], sols2["CR-4"], sols2["CR-5"]))

#To print the minimum cost per day
def print_solutions_rent(minimum_cost): 
    #print(solution_found)
    st.write("""Rental Cost/Day(RM)        :  {}""".format(minimum_cost))

#To print the minimum cost on last day
def print_solutions_rent_lastDay(minimum_cost2): 
    #print(solution_found)
    st.write("""Rental Cost Last Day(RM)   :  {}""".format(minimum_cost2))

def vac_info(vac, age60, age35_60, age35, maxCapacityPerDay, day_age, lastDay_Client):
        #vac-A
        client_60=0
        #vac-B
        client_3565=0
        #vac-C
        client_35=0
        
        if vac == 1:
            client_60 = age60 - (math.floor(age60/maxCapacityPerDay)*maxCapacityPerDay)
            client_3565 = maxCapacityPerDay - client_60
            if client_60 == 0:
                client_60 = maxCapacityPerDay
                client_3565 = 0
        elif vac == 2:
            client_60 = age60 - (math.floor(age60/maxCapacityPerDay)*maxCapacityPerDay)
            client_3565 = maxCapacityPerDay - client_60
            if client_60 == 0:
                client_60 = maxCapacityPerDay
                client_3565 = 0
                
            age35_60_2 = age35_60 - client_3565
            client_3565 = age35_60_2 - (math.floor(age35_60_2/maxCapacityPerDay)*maxCapacityPerDay)
            client_35 = maxCapacityPerDay - client_3565
            client_60 = 0
        elif vac == 3:
            client_35 = lastDay_Client
            
        #output of each type of vaccine
        st.write("At Day: ", day_age)
        st.write("No. Vaccine Type A: ", client_60)
        st.write("No. Vaccine Type B: ", client_3565)
        st.write("No. Vaccine Type C: ", client_35)


#The main CSP Algorithm function
def CSP_function(state, maxCapacityPerDay, age35, age35_60, age60, cr1, cr2, cr3, cr4, cr5):
    
    #Create CSP
    problem = constraint.Problem()
    problem2 = constraint.Problem()
    
    #Calculate total day required to vaccine all client. 
    totalClient = age35 + age35_60 + age60
    totalDay = totalClient/maxCapacityPerDay
    totalDay = math.ceil(totalDay)
    
    #Calculate the number of client on last day and round up(Nearest Hundred)
    lastDay_Client = totalClient - (math.floor(totalClient/maxCapacityPerDay) * maxCapacityPerDay)
    lastDay_Client_round = roundup(lastDay_Client)
    #print(math.floor(totalClient/maxCapacityPerDay))
    
    #Calculate on which day each category of client completed the vaccination
    #Vaccination start from the priority below:
    #Priority_1: Age < 35
    #Priority_2: Age Between 35-60
    #Priority_3: Age > 60
    day_age60 = math.ceil(age60/maxCapacityPerDay)
    day_age35_60 = math.ceil((age60+age35_60)/maxCapacityPerDay)
    day_age35 = math.ceil((age35+age35_60+age60)/maxCapacityPerDay)
            
    #Create CSP variables
    problem.addVariable('CR-1', range(cr1 + 1))
    problem.addVariable('CR-2', range(cr2 + 1))  
    problem.addVariable('CR-3', range(cr3 + 1))  
    problem.addVariable('CR-4', range(cr4 + 1))  
    problem.addVariable('CR-5', range(cr5 + 1))
    
    problem2.addVariable('CR-1', range(cr1 + 1))
    problem2.addVariable('CR-2', range(cr2 + 1))  
    problem2.addVariable('CR-3', range(cr3 + 1))  
    problem2.addVariable('CR-4', range(cr4 + 1))  
    problem2.addVariable('CR-5', range(cr5 + 1))
    
    #Add constraint to CSP
    problem.addConstraint(constraint.ExactSumConstraint(maxCapacityPerDay,[200,500,1000,2500,4000]),["CR-1", "CR-2", "CR-3", "CR-4", "CR-5"])
    problem2.addConstraint(constraint.ExactSumConstraint(lastDay_Client_round,[200,500,1000,2500,4000]),["CR-1", "CR-2", "CR-3", "CR-4", "CR-5"])

    #Get solution from CSP
    solutions = problem.getSolutions() 
    solutions2 = problem2.getSolutions() 
    
    #Calculate minimum cost per day
    minimum_cost = 9999
    solution_found = {}
    for s in solutions:
        current_sweetness = s['CR-1']*100 + s['CR-2']*250 + s['CR-3']*500 + s['CR-4']*800 + s['CR-5']*1200
        if current_sweetness < minimum_cost:
            minimum_cost = current_sweetness
            solution_found = s
    
    #Calculate minimum on last day
    minimum_cost2 = 9999
    solution_found2 = {}
    for s in solutions2:
        current_sweetness = s['CR-1']*100 + s['CR-2']*250 + s['CR-3']*500 + s['CR-4']*800 + s['CR-5']*1200
        if current_sweetness < minimum_cost2:
            minimum_cost2 = current_sweetness
            solution_found2 = s
    
    #Calculate total cost 
    totalCost = ((totalDay-1) * minimum_cost) + minimum_cost2
    
    #Code for output
    #st.write("--------------------------------")  
    st.write("          ", state, "Result     ")
    #st.write("--------------------------------")  
    st.write("MaxVaccine/Day: ", maxCapacityPerDay)
    st.write("Age > 60   : ", age60, "(Vac-A)")
    st.write("Age(35-60) : ", age35_60, "(Vac-B)")
    st.write("Age < 35   : ", age35, "(Vac-C)")
    st.write("      Total: ", totalClient)
    #st.write("--------------------------------")    
    print_solutions2(solution_found)
    print_solutions_lastDay(solution_found2)
    #st.write("--------------------------------")  
    print_solutions_rent(minimum_cost)
    print_solutions_rent_lastDay(minimum_cost2)
    st.write("Total Rental Cost(RM)      : ", totalCost)
    st.write("Total Duration(Day)        : ", totalDay)
    #st.write("---------------------------------")  
    st.write("(Age > 60)  Complete Vaccination at Day : ", day_age60)
    st.write("(Age(35-60) Complete Vaccination at Day : ", day_age35_60)
    st.write("(Age < 35)  Complete Vaccination at Day : ", day_age35)
    #st.write("---------------------------------")
    vac_info(1, age60, age35_60, age35, maxCapacityPerDay, day_age60, lastDay_Client)
    #st.write("---------------------------------")
    vac_info(2, age60, age35_60, age35, maxCapacityPerDay, day_age35_60, lastDay_Client)
    #st.write("---------------------------------")
    vac_info(3, age60, age35_60, age35, maxCapacityPerDay, day_age35, lastDay_Client)
    

#st.set_page_config(layout = "wide")

st.title("Question2")

st.write(CSP_function("ST-1", 5000, 115900, 434890, 15000, 20, 15, 10, 21, 5))
st.write("-------------------------")
st.write(CSP_function("ST-2", 10000, 100450, 378860, 35234, 30, 16, 15, 10, 2))
st.write("-------------------------")
st.write(CSP_function("ST-3", 7500, 223400, 643320, 22318, 22, 15, 11, 12, 3))
st.write("-------------------------")
st.write(CSP_function("ST-4", 8500, 269300, 859900, 23893, 16, 16, 16, 15, 1))
st.write("-------------------------")
st.write(CSP_function("ST-5", 9500, 221100, 450500, 19284, 19, 10, 20, 15, 1))
