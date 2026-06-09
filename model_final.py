import matplotlib.pyplot as plt
import random
import math

# EXPERIMENT SETTINGS


TOTAL_POPULATION = 2000
INITIAL_INFECTED = 100
DAYS_TO_SIMULATE = 200
SPREAD_RATE = 20

# EMOTIONAL_INTENSITY_E = int(input())
EMOTIONAL_INTENSITY_E = 3   
PLATFORM_WALL_W = int(input())      

SIMULATIONS = 15         



def run_simulation(E, W):
    # media literacy (1~10)
    population_literacy = [random.randint(1, 10) for _ in range(TOTAL_POPULATION)]
    
    # states: 0=S, 1=I, 2=L, 3=R
    states = [0] * TOTAL_POPULATION
    
  
    for i in range(INITIAL_INFECTED):
        states[i] = 1
    
    history_S, history_I, history_L, history_R = [], [], [], []
    
    for day in range(DAYS_TO_SIMULATE):
        
        # count
        current_S = states.count(0)
        current_I = states.count(1)
        current_L = states.count(2)
        current_R = states.count(3)
        
        history_S.append(current_S)
        history_I.append(current_I)
        history_L.append(current_L)
        history_R.append(current_R)
        
        #1. I → L 
        for i, state in enumerate(states):
            if state == 1:  # Infected (공유자)
                
                if random.random() < (W / 120):
                    states[i] = 2  # I → L
        
        #2. spread
        current_I = states.count(1)
        exposures = current_I * SPREAD_RATE
        
        susceptible_indices = [i for i, s in enumerate(states) if s == 0]
        random.shuffle(susceptible_indices)
        
        for i in range(min(exposures, len(susceptible_indices))):
            person_id = susceptible_indices[i]
            L = population_literacy[person_id]
            
            # Cognitive Friction
            F = 2.5*L-1.8*math.exp(0.4)*E+1.0*W+0.6*(L*W)-0.5*(E*L)
            
            
            # determining state
            if F <= 0.0:
                states[person_id] = 1  # I
            elif F <= 28.21:
                states[person_id] = 2  # L
            else:
                states[person_id] = 3  # R

        #3. L → R 
        for i, state in enumerate(states):
            if state == 2:  # Lurker
                
                L_val = population_literacy[i]
                F = 2.5*L_val-1.8*math.exp(0.4)*E+1.0*W+0.6*(L_val*W)-0.5*(E*L_val)
                
                if F > 2 and random.random() < (F / 120):
                    states[i] = 3  # L → R
        
        #4. L → I 
        for i, state in enumerate(states):
            if state == 2:
               
                if random.random() < (E / 120):
                    states[i] = 1  # L → I
    
    return history_S, history_I, history_L, history_R



# repeat
avg_S = [0] * DAYS_TO_SIMULATE
avg_I = [0] * DAYS_TO_SIMULATE
avg_L = [0] * DAYS_TO_SIMULATE
avg_R = [0] * DAYS_TO_SIMULATE

for _ in range(SIMULATIONS):
    S, I, L, R = run_simulation(EMOTIONAL_INTENSITY_E, PLATFORM_WALL_W)
    
    for t in range(DAYS_TO_SIMULATE):
        avg_S[t] += S[t]
        avg_I[t] += I[t]
        avg_L[t] += L[t]
        avg_R[t] += R[t]

# calculate average
avg_S = [x / SIMULATIONS for x in avg_S]
avg_I = [x / SIMULATIONS for x in avg_I]
avg_L = [x / SIMULATIONS for x in avg_L]
avg_R = [x / SIMULATIONS for x in avg_R]


final_I = avg_I[-1]
final_L = avg_L[-1]
final_bias = final_I + final_L

print(EMOTIONAL_INTENSITY_E, PLATFORM_WALL_W)
print("Final Infected (I):", final_I)
print("Final Lurkers (L):", final_L)
print("Total Biased Population (I + L):", final_bias)
print('proportion: ', final_L/final_bias)


# graph

plt.figure(figsize=(10, 6))

plt.plot(avg_S, label='Susceptible (S)', color='gray', linewidth=2, linestyle='--')
plt.plot(avg_I, label='Infected / Spreaders (I)', color='red', linewidth=3)
plt.plot(avg_L, label='Lurkers (L)', color='orange', linewidth=3)
plt.plot(avg_R, label='Resistant (R)', color='green', linewidth=3)


plt.title(f"Simulation (E={EMOTIONAL_INTENSITY_E}, W={PLATFORM_WALL_W})")
plt.xlabel("Days")
plt.ylabel("Population")

plt.xticks(range(0, DAYS_TO_SIMULATE + 1, 2))

plt.legend()
plt.grid(True, linestyle=':')

plt.tight_layout()
plt.show()
