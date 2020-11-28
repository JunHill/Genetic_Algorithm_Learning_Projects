import random

class _2DParticle():
    def __init__(self, optimizing_func):
        self.func = optimizing_func
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*optimizing_func['search_domain'], (-1)**(bool(random.getrandbits(1))) * random.random()* optimizing_func['search_domain']])
        self.score = float('inf')
        self.best_pos = self.position
        self.best_val = float('inf')
        self.vel = np.array([0, 0])

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

class _10DParticle():
    def __init__(self, optimizing_func):
        self.func = optimizing_func
        self.position = []
        for _ in range(10):
            self.position.append((-1) ** (bool(random.getrandbits(1))) * random.random()*optimizing_func['search_domain'])
        self.position = np.array(self.position)
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

class PSO_Star():
    def __init__(self, n_particles, n_gen, optimizing_func):
        self.n_particles = n_particles
        self.particles = []
        self.n_gen = n_gen
        for _ in range(self.n_particles):
            if optimizing_func['dimension'] == 2:
                self.particles.append(_2DParticle(optimizing_func))
            elif optimizing_func['dimension'] == 10:
                self.particles.append(_10DParticle(optimizing_func))
        self.gen_best_pos = self.particles[0].position.copy()
        self.gen_best_val = self.particles[0].best_val

        self.w = 0.7298
        self.c1 = self.c2 = 1.49618
    def solve(self):
        for i in range(self.n_gen):
            self.last_pos = [self.particles[x].position.copy() for x in range(self.n_particles)]
            self.last_score = [self.particles[x].score for x in range(self.n_particles)]
            for particle in self.particles:
                particle.fitness()

            for particle in self.particles:
                if particle.score < self.gen_best_val:
                    self.gen_best_val = particle.score
                    self.gen_best_pos = particle.position.copy()

            for particle in self.particles:
                new_velocity = (self.w*particle.vel) + (self.c1*random.random()) * (particle.best_pos - particle.position) + (random.random()*self.c2) * (self.gen_best_pos - particle.position)
                particle.vel = new_velocity
                particle.move()
            self.print_particle()
    def print_particle(self):
        print('---------------------------')
        for pid,particle in enumerate(self.particles):
            print(f'{self.last_pos[pid]} ({self.last_score[pid]}) -> {particle.position} ({particle.score}) => changed ({round(particle.score - self.last_score[pid],3)})')
    def print_best_gen(self):
        print(f'best gen at {self.gen_best_pos} achieves {round(self.gen_best_val,5)}!')


class PSO_Ring():
    def __init__(self, n_particles, n_gen, optimizing_func):
        self.n_particles = n_particles
        self.best_of_particles_score = [float('inf')] * n_particles
        self.best_of_particles_pos = [None] * n_particles
        self.particles = []
        for _ in range(self.n_particles):
            if optimizing_func['dimension'] == 2:
                self.particles.append(_2DParticle(optimizing_func))
            elif optimizing_func['dimension'] == 10:
                self.particles.append(_10DParticle(optimizing_func))

        self.n_gen = n_gen
        self.mini_swarms = []
        for x in zip(np.arange(n_particles-2), np.arange(n_particles-2) + 1, np.arange(n_particles-2)+2):
            self.mini_swarms.append(x)
        self.mini_swarms.append((n_particles - 2, n_particles - 1, 0))
        self.mini_swarms.append((n_particles - 1, 0, 1))
        self.mini_scores = [float('inf')] * len(self.mini_swarms)
        self.mini_pos = [None] * len(self.mini_swarms)

        self.w = 0.7298
        self.c1 = self.c2 = 1.49618

    def update_best_of_swarm(self):
        for i in range(len(self.mini_swarms)):
            for px in [self.particles[x] for x in self.mini_swarms[i]]:
                if px.score < self.mini_scores[i]:
                    self.mini_scores[i] = px.score
                    self.mini_pos[i] = px.position.copy()
        for pid,particle in enumerate(self.particles):
            for sid, trio in enumerate(self.mini_swarms):
                if pid in trio:
                    if self.best_of_particles_score[pid] > self.mini_scores[sid]:
                        self.best_of_particles_score[pid] = self.mini_scores[sid]
                        self.best_of_particles_pos[pid] = self.mini_pos[sid].copy()

    def solve(self):
        for i in range(self.n_gen):
            for particle in self.particles:
                particle.fitness()

            self.update_best_of_swarm()

                
            for pid,particle in enumerate(self.particles):
                new_velocity = (self.w*particle.vel) + (self.c1*random.random()) * (particle.best_pos - particle.position) + (random.random()*self.c2) * (self.best_of_particles_pos[pid] - particle.position)
                particle.vel = new_velocity
                particle.move()

            self.print_particle()
    def print_particle(self):
        print('---------------------------')
        for particle in self.particles:
            print(f'{particle.score} - {particle.position} : vel {particle.vel}')


from function_list import *

solver = PSO_Star(1028, 150, Rastrigin_10)
#solver.print_particle()
solver.solve()
#solver.print_particle()