#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <cstdlib>
#include <algorithm>

const std::string TARGET = "my_PASS_???W=?orD_.._";
const int POP_SIZE = 1000;
const double MUTATION_RATE = 0.01;
const int GENERATIONS = 1000;
const int ELITE_COUNT = POP_SIZE * 0.1; // 10% of the population

// Generate a random character
char randomChar()
{
    return ' ' + rand() % 95; // ASCII character between ' ' (space) and '~'
}

// Generate a random individual
std::string randomIndividual()
{
    std::string individual;
    for (int i = 0; i < TARGET.size(); i++)
    {
        individual += randomChar();
    }
    return individual;
}

// Fitness function
int fitness(const std::string &individual)
{
    int score = 0;
    for (int i = 0; i < individual.size(); i++)
    {
        if (individual[i] == TARGET[i])
        {
            score++;
        }
    }
    return score;
}

// Fitness-based selection
std::string selectParent(const std::vector<std::string> &population)
{
    int index1 = rand() % POP_SIZE;
    int index2 = rand() % POP_SIZE;

    // Choose the best one based on fitness value
    if (fitness(population[index1]) > fitness(population[index2]))
    {
        return population[index1];
    }
    else
    {
        return population[index2];
    }
}

int main()
{
    srand(time(NULL));

    std::vector<std::string> population;

    // Create initial population
    for (int i = 0; i < POP_SIZE; i++)
    {
        population.push_back(randomIndividual());
    }

    for (int gen = 0; gen < GENERATIONS; gen++)
    {
        std::vector<std::string> newPopulation;

        // Sort individuals by suitability
        std::sort(population.begin(), population.end(),
                  [](const std::string &a, const std::string &b)
                  {
                      return fitness(a) > fitness(b);
                  });

        // Transfer elite individuals directly to new population
        for (int i = 0; i < ELITE_COUNT; i++)
        {
            newPopulation.push_back(population[i]);
        }

        // Perform selection, crossover and
        // mutation operations for the remaining individuals
        for (int i = ELITE_COUNT; i < POP_SIZE; i++)
        {
            std::string parent1 = selectParent(population);
            std::string parent2 = selectParent(population);
            std::string child;

            // Crossover
            for (int j = 0; j < TARGET.size(); j++)
            {
                if ((rand() % 2) == 0)
                {
                    child += parent1[j];
                }
                else
                {
                    child += parent2[j];
                }
            }

            // Mutation
            for (int j = 0; j < TARGET.size(); j++)
            {
                if ((rand() / double(RAND_MAX)) < MUTATION_RATE)
                {
                    child[j] = randomChar();
                }
            }

            newPopulation.push_back(child);
        }

        population = newPopulation;

        // Print the best individual
        int bestFitness = -1;
        std::string bestIndividual;
        for (const auto &individual : population)
        {
            int currentFitness = fitness(individual);
            if (currentFitness > bestFitness)
            {
                bestFitness = currentFitness;
                bestIndividual = individual;
            }
        }

        std::cout << "Generation " << gen << ": " << bestIndividual << " (" << bestFitness << "/" << TARGET.size() << " correct)" << std::endl;

        if (bestFitness == TARGET.size())
        {
            std::cout << "Target found!" << std::endl;
            break;
        }
    }

    return 0;
}
