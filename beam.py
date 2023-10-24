import numpy as np
import random
import matplotlib.pyplot as plt

# Parametreler
L = 5  # Kiriş uzunluğu (m)
E = 2e11  # Elastik modülü (N/m^2) - Örnek olarak çelik için
P = 10000  # Uç yük (N)
max_deformation = 0.05  # Maksimum izin verilen bükülme (m)

# Bükülme formülü
def deformation(b, h):
    I = b * h**3 / 12
    return (P * L**3) / (3 * E * I)

# Fitness fonksiyonu
def fitness(individual):
    b, h = individual
    d = deformation(b, h)
    if d > max_deformation:  # Eğer bükülme sınırı aşılırsa, ceza puanı ekleyelim
        return 1e10
    return b * h * L  # Kirişin hacmi (ve dolayısıyla ağırlığı)

# Genetik algoritma parametreleri
pop_size = 10000
generations = 100
mutation_rate = 0.2
crossover_rate = 0.8
best_fitness_values = []

# Genetik algoritmayı çalıştırma
population = [(random.uniform(0.1, 1.0), random.uniform(0.1, 1.0)) for _ in range(pop_size)]

for generation in range(generations):
    # Fitness değerlerini hesapla
    fitness_values = [fitness(ind) for ind in population]
    
    # En iyi fitness değerini kaydet
    best_fitness_values.append(min(fitness_values))
    
    # Seçilim
    selected_indices = np.argsort(fitness_values)[:pop_size // 2]
    selected = [population[i] for i in selected_indices]
    
    # Yeni popülasyonu oluştur
    new_population = []
    for i in range(0, len(selected), 2):
        if np.random.rand() < crossover_rate and i+1 < len(selected):
            crossover_point = random.randint(0, 1)
            if crossover_point == 0:
                new_individual1 = (selected[i][0], selected[i+1][1])
                new_individual2 = (selected[i+1][0], selected[i][1])
            else:
                new_individual1 = (selected[i+1][0], selected[i][1])
                new_individual2 = (selected[i][0], selected[i+1][1])
            new_population.extend([new_individual1, new_individual2])
        else:
            new_population.append(selected[i])
            if i+1 < len(selected):
                new_population.append(selected[i+1])
    
    # Mutasyon
    for i in range(len(new_population)):
        if np.random.rand() < mutation_rate:
            mutate_dim = random.randint(0, 1)
            mutation_value = random.uniform(-0.05, 0.05)
            if mutate_dim == 0:
                new_population[i] = (max(0.1, new_population[i][0] + mutation_value), new_population[i][1])
            else:
                new_population[i] = (new_population[i][0], max(0.1, new_population[i][1] + mutation_value))
    
    # Yeni popülasyonu atama
    population = new_population

# En iyi bireyin ve optimal bireyin değerlerini bulma
best_individual = population[np.argmin(fitness_values)]

# En iyi birey için hesaplamalar
best_b, best_h = best_individual
best_I = best_b * best_h**3 / 12  # Inertia
best_M = P * L  # Moment
best_d = deformation(best_b, best_h)  # Deformasyon

# Ortalama birey için hesaplamalar
avg_b = np.mean([individual[0] for individual in population])
avg_h = np.mean([individual[1] for individual in population])
avg_I = avg_b * avg_h**3 / 12
avg_M = P * L
avg_d = deformation(avg_b, avg_h)

output_details = f"""
Ayrıntılı Sonuçlar:
-------------------
Verilen Değerler:
  Elastik Modül (E)       : {E:.2e} N/m^2
  Uzunluk (L)             : {L} m
  Uçta Uygulanan Yük (P)  : {P} N
  Yükün Konumu            : Uçta (L = {L} m)
  Yükün Yönü              : Aşağıya doğru

En İyi Birey:
  Genişlik (b)            : {best_b:.4f} m
  Yükseklik (h)           : {best_h:.4f} m
  Inertia (I)             : {best_I:.2e} m^4
  Moment (M)              : {best_M:.2e} N.m
  Deformasyon             : {best_d:.2e} m

Ortalama Birey:
  Genişlik (b)            : {avg_b:.4f} m
  Yükseklik (h)           : {avg_h:.4f} m
  Inertia (I)             : {avg_I:.2e} m^4
  Moment (M)              : {avg_M:.2e} N.m
  Deformasyon             : {avg_d:.2e} m
"""

print(output_details)


# En iyi ve optimal uygunluk değerlerini hesaplama
best_overall_fitness = min(best_fitness_values)
optimal_fitness = np.mean(best_fitness_values)

# Grafikle gösterme
plt.figure(figsize=(12, 7))

# Optimal, en iyi ve elde edilen uygunluk değerlerini grafikte gösterme
plt.axhline(y=optimal_fitness, color='blue', linestyle='--', label=f'Optimal Uygunluk: {optimal_fitness:.6f}')
plt.axhline(y=best_overall_fitness, color='green', linestyle='--', label=f'En İyi Uygunluk: {best_overall_fitness:.6f}')
plt.plot(best_fitness_values, marker='o', linestyle='', markersize=2, label='Elde Edilen Uygunluk Değeri', color='orange')

plt.xlabel('Jenerasyon')
plt.ylabel('Uygunluk Değeri')
plt.title('Genetik Algoritma İlerlemesi')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(np.arange(0, generations, 5))  # X eksenini daha hassas hale getirme
plt.yticks(np.arange(min(best_fitness_values), max(best_fitness_values), (max(best_fitness_values) - min(best_fitness_values))/20))  # Y eksenini daha hassas hale getirme
plt.show()