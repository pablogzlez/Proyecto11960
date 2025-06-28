import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 1. Definición de las funciones componentes
def d(t, T):
    """Función base triangular periódica"""
    return np.abs(t - T * np.floor(t / T + 0.5))

def f1(t, T=29.530589):
    return d(t, T)

def f2(t, T=27.212220):
    return d(t, T)

def f3(t, T=27.55455):
    return d(t, T)

def vector_func(t):
    """Función vectorial que devuelve las 3 componentes"""
    return np.array([f1(t), f2(t), f3(t)])

def norm_func(t):
    """Norma euclidiana del vector f(t)"""
    return np.linalg.norm(vector_func(t))

# 2. Función para encontrar raíces comunes
def find_common_roots(epsilon=0.5, search_range=(0, 177)):
    """
    Encuentra valores de t donde f(t) ≈ [0,0,0]
    
    Parámetros:
        epsilon: margen de error aceptable
        search_range: rango de búsqueda (inicio, fin)
    
    Retorna:
        Array con las raíces encontradas
    """
    # Puntos candidatos (considerando los períodos)
    step = min(29.530589, 27.212220, 27.55455)/2  # Paso de búsqueda
    search_points = np.arange(search_range[0], search_range[1], step)
    
    roots = []
    
    for t0 in search_points:
        # Optimización local
        res = minimize(norm_func, t0, method='Nelder-Mead', tol=epsilon)
        
        # Verificación del resultado
        if res.fun < epsilon:
            root = round(res.x[0], 4)
            if all(np.abs(vector_func(root)) < 3*epsilon):
                roots.append(root)
    
    # Eliminar duplicados y ordenar
    unique_roots = np.unique(np.round(roots, decimals=3))
    
    return unique_roots

# 3. Cálculo de las raíces
common_roots = find_common_roots(epsilon=0.5)
print("Valores de t donde f(t) ≈ [0,0,0]:")
print(common_roots)

# 4. Visualización gráfica
t_values = np.linspace(0, 150, 1000)
f_values = np.array([vector_func(t) for t in t_values])

plt.figure(figsize=(14, 7))

# Graficar cada componente
plt.plot(t_values, f_values[:, 0], color='#FC6B6B', label='f1(t), T=mes sinódico', linewidth=2)
plt.plot(t_values, f_values[:, 1], color='#5554FF', label='f2(t), T=mes draconítico', linewidth=2)
plt.plot(t_values, f_values[:, 2], color='#4ECDC4', label='f3(t), T=mes anomalístico', linewidth=2)

# Marcar las raíces encontradas
for root in common_roots:
    if np.abs(root) <= 177:  # Solo mostrar en el rango visible
        plt.axvline(root, color='gray', linestyle='--', alpha=0.5)
        plt.plot(root, 0, 'ro', markersize=8)

# Configuración del gráfico
plt.axhline(0, color='black', linewidth=0.5)
plt.xlabel('t en días', fontsize=12)
plt.ylabel('d(t) en días', fontsize=12)
plt.title('Componentes de la función vectorial f(t)', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Mostrar y guardar el gráfico
plt.savefig('ceros_funcion_vectorial.png', dpi=300)
plt.show()