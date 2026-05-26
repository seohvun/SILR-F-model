import matplotlib.pyplot as plt
import random
import math

# EXPERIMENT SETTINGS


TOTAL_POPULATION = 2000
INITIAL_INFECTED = 100
DAYS_TO_SIMULATE = 200
SPREAD_RATE = 20

# EMOTIONAL_INTENSITY_E = int(input())
EMOTIONAL_INTENSITY_E = 3   # 감정 강도 (높을수록 bias 강함)
PLATFORM_WALL_W = int(input())         # 플랫폼 개입 강도0

SIMULATIONS = 15             # 여러 번 돌려 평균 내기


# 시뮬레이션 함수
def run_simulation(E, W):
    # 개인별 media literacy (1~10)
    population_literacy = [random.randint(1, 10) for _ in range(TOTAL_POPULATION)]
    
    # 상태: 0=S, 1=I, 2=L, 3=R
    states = [0] * TOTAL_POPULATION
    
    # 초기 감염자 설정
    for i in range(INITIAL_INFECTED):
        states[i] = 1
    
    history_S, history_I, history_L, history_R = [], [], [], []
    
    for day in range(DAYS_TO_SIMULATE):
        
        # 현재 상태 카운트
        current_S = states.count(0)
        current_I = states.count(1)
        current_L = states.count(2)
        current_R = states.count(3)
        
        history_S.append(current_S)
        history_I.append(current_I)
        history_L.append(current_L)
        history_R.append(current_R)
        
        #1. I → L 전이 (🔥 핵심: Wall이 공유 억제)
        for i, state in enumerate(states):
            if state == 1:  # Infected (공유자)
                
                # Wall이 강할수록 공유 포기하고 Lurker로 이동
                if random.random() < (W / 120):
                    states[i] = 2  # I → L
        
        #2. 정보 확산 (I만 공유)
        current_I = states.count(1)
        exposures = current_I * SPREAD_RATE
        
        susceptible_indices = [i for i, s in enumerate(states) if s == 0]
        random.shuffle(susceptible_indices)
        
        for i in range(min(exposures, len(susceptible_indices))):
            person_id = susceptible_indices[i]
            L = population_literacy[person_id]
            
            # Cognitive Friction
            F = 2.5*L-1.8*math.exp(0.4)*E+1.0*W+0.6*(L*W)-0.5*(E*L)
            
            
            # 상태 결정
            if F <= 0.0:
                states[person_id] = 1  # I
            elif F <= 43.15:
                states[person_id] = 2  # L
            else:
                states[person_id] = 3  # R

        #3. L → R 전이 (🔥 비판적 전환)
        for i, state in enumerate(states):
            if state == 2:  # Lurker
                
                L_val = population_literacy[i]
                F = 2.5*L_val-1.8*math.exp(0.4)*E+1.0*W+0.6*(L_val*W)-0.5*(E*L_val)
                
                # F가 높을수록 R로 갈 확률 증가
                if F > 2 and random.random() < (F / 120):
                    states[i] = 3  # L → R
        
        #4. L → I 전이 (🔥 잠재적 폭발)
        for i, state in enumerate(states):
            if state == 2:
                # 감정이 강할수록 다시 공유 시작
                if random.random() < (E / 120):
                    states[i] = 1  # L → I
    
    return history_S, history_I, history_L, history_R



# 여러 번 실행해서 평균내기

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

# 평균 계산
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


# 그래프


plt.figure(figsize=(10, 6))

plt.plot(avg_S, label='Susceptible (S)', color='gray', linewidth=2, linestyle='--')
plt.plot(avg_I, label='Infected / Spreaders (I)', color='red', linewidth=3)
plt.plot(avg_L, label='Lurkers (L)', color='orange', linewidth=3)
plt.plot(avg_R, label='Resistant (R)', color='green', linewidth=3)


plt.title(f"Simulation (E={EMOTIONAL_INTENSITY_E}, W={PLATFORM_WALL_W})")
plt.xlabel("Days")
plt.ylabel("Population")

# 🔥 핵심 추가 (x축 간격 촘촘하게)
plt.xticks(range(0, DAYS_TO_SIMULATE + 1, 2))

plt.legend()
plt.grid(True, linestyle=':')

plt.tight_layout()
plt.show()