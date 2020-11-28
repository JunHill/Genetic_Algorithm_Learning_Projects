from utils import *

Rastrigin_2 = {
    'search_domain': 5.12,
    'score': Rastrigin_2_f,
    'dimension': 2,
    'name': "Rastrigin 2 Dimension"
}

Rastrigin_10 = {
    'search_domain': 5.12,
    'score': Rastrigin_10_f,
    'dimension': 10,
    'name': "Rastrigin 10 Dimension"
}

Rosenbrock_2 = {
    'search_domain': float('inf'),
    'score': RosenBrock,
    'dimension': 2,
    'name': "RosenBrock 2 Dimension"
}

Rosenbrock_10 = {
    'search_domain': float('inf'),
    'score': RosenBrock,
    'dimension': 10,
    'name': "RosenBrock 10 Dimension"
}

Ackley = {
    'search_domain': 5,
    'score': Ackley_f,
    'dimension': 2,
    'name': "Ackley"    
}

Eggholder = {
    'search_domain': 512,
    'score': Eggholder_f,
    'dimension': 2,
    'name': "Eggholder"    
}


