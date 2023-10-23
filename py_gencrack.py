import random

TARGET = "my_PASS_???W=?orD_.._"
POP_SIZE = 1000
MUTATION_RATE = 0.01
GENERATIONS = 1000
ELITE_COUNT = int(POP_SIZE * 0.1)  # 10% of the population

# Generate a random character
def random_char():
    return chr(random.randint(32, 126))  # ASCII character between ' ' (space) and '~'

# Generate a random individual
def random_individual():
    return ''.join(random_char() for _ in range(len(TARGET)))

# Fitness function
def fitness(individual):
    return sum(1 for c1, c2 in zip(individual, TARGET) if c1 == c2)

# Fitness-based selection
def select_parent(population):
    index1 = random.randint(0, POP_SIZE-1)
    index2 = random.randint(0, POP_SIZE-1)

    # Choose the best one based on fitness value
    if fitness(population[index1]) > fitness(population[index2]):
        return population[index1]
    else:
        return population[index2]

def main():
    population = [random_individual() for _ in range(POP_SIZE)]
    
    for gen in range(GENERATIONS):
        population.sort(key=fitness, reverse=True)
        new_population = population[:ELITE_COUNT]

        # Perform selection, crossover, and mutation operations for the remaining individuals
        for _ in range(ELITE_COUNT, POP_SIZE):
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = []

            # Crossover
            for j in range(len(TARGET)):
                if random.randint(0, 1) == 0:
                    child.append(parent1[j])
                else:
                    child.append(parent2[j])

            # Mutation
            for j in range(len(TARGET)):
                if random.random() < MUTATION_RATE:
                    child[j] = random_char()

            new_population.append(''.join(child))

        population = new_population

        # Print the best individual
        best_individual = max(population, key=fitness)
        best_fitness = fitness(best_individual)
        
        print(f"Generation {gen}: {best_individual} ({best_fitness}/{len(TARGET)} correct)")
        
        if best_fitness == len(TARGET):
            print("Target found!")
            break

if __name__ == "__main__":
    main()
