import random
from function_list import *

class Particle():
    def __init__(self, optimizing_func, n_dimensions = 2):
        self.func = optimizing_func
        self.position =  np.array([(-1) ** (bool(random.getrandbits(1))) * \
            random.random() * optimizing_func['search_domain'] for _ in range(n_dimensions)])
        self.score = float('inf')
        self.best_pos = self.position
        self.best_val = float('inf')
        self.vel = np.zeros(self.position.shape)

    def move(self):
        self.position = self.position + self.vel
        for i in range(len(self.position)):
            if self.position[i] > self.func['search_domain']:
                self.position[i] = self.func['search_domain']
            elif self.position[i] < -self.func['search_domain']:
                self.position[i] = -self.func['search_domain']

    def fitness(self):
        self.score = self.func['score'](self.position)
        if self.score < self.best_val:
            self.best_val = self.score
            self.best_pos = self.position
        return 1

class PSO():
    FITNESS_CALL_LIMIT = 10**6
    STD_THRESHOLD = 0.00001
    def __init__(self, n_particles, n_gen, optimizing_func, topology):
        self.topology = topology
        self.n_particles = n_particles
        self.particles = []
        self.n_gen = n_gen
        self.optimize_func = optimizing_func
        self.particles = [Particle(optimizing_func, \
                optimizing_func['dimension']) for _ in range(self.n_particles)]
        self.gen_best_pos = [None for _ in range(self.n_particles)]
        self.gen_best_val = [float('inf') for _ in range(self.n_particles)]
        self.the_one_val = float('inf')
        self.the_one_pos = None

        self.w = 0.7298
        self.c1 = self.c2 = 1.49618

    def solve(self,track=False):
        cnt = 0
        for i in range(self.n_gen):
            result = []
            for particle in self.particles:
                result.append(particle.position)
            result = np.array(result)
            for ind, particle in enumerate(self.particles):
                cnt += particle.fitness()

                if particle.score < self.gen_best_val[ind]:
                    self.gen_best_val[ind] = particle.score
                    self.gen_best_pos[ind] = particle.position.copy()
                if particle.score < self.the_one_val:
                    self.the_one_val = particle.score
                    self.the_one_pos = particle.position.copy()
                if cnt > PSO.FITNESS_CALL_LIMIT and self.optimize_func['dimension'] == 10:
                    return result, self.the_one_val, self.the_one_pos
                
                     
            if track == True:
                np.savetxt(f"result/{self.topology}/{self.optimize_func['name']}/gen{i}.txt", result)

            for ind, particle in enumerate(self.particles):
                tmp = -1
                tmp_val = float('inf')
                for _ in [(ind + self.n_particles - 1) % self.n_particles, ind, (ind + 1) % self.n_particles]:
                    if self.gen_best_val[_] < tmp_val:
                        tmp_val = self.gen_best_val[_]
                        tmp =  _
                new_velocity = (self.w*particle.vel) + (self.c1*random.random()) * (particle.best_pos - \
                    particle.position) + (random.random()*self.c2) * ((self.the_one_pos if \
                        self.topology == 'star' else self.gen_best_pos[tmp])  - particle.position)
                particle.vel = new_velocity
                particle.move()

            
            if np.array([x.score for x in self.particles]).std() < PSO.STD_THRESHOLD:
                return result, self.the_one_val, self.the_one_pos
            
        return result, self.the_one_val, self.the_one_pos

    def print_particle(self):
        print('---------------------------')
        for pid, particle in enumerate(self.particles):
            print(f'{particle.score} - {particle.vel}')

    def print_best_gen(self):
        res_id = np.argmin(self.gen_best_val)
        print(f'best gen at {self.gen_best_pos[res_id]} achieves {round(self.gen_best_val[res_id],5)}!')
