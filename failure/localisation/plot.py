import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.special import lambertw
from scipy.integrate import quad


def weight_function(dist,L):
    return np.power(1-np.power(np.minimum(np.abs(dist),L)/L,2),2)


def compute_k(d,e0,ef):
    ductility = (2*ef/e0) -1
    etam1 = ductility - 1
    return np.real(0.5 * e0 * etam1 * lambertw((2*np.exp(2/etam1))/((1-d) * etam1)))

def damage_response(k,e0,ef):
    if k > e0:
        return 1.0 - e0/k * np.exp(-(k-e0)/(ef-e0))
    else:
        return 0.0

def compute_gF(k,e0,ef,E):
    if k > e0:
        return quad(lambda x: (1-damage_response(x,e0,ef))*E*x,e0,k)[0]
    else:
        return 0.0


E=1
e0 = 1
ef = 2
k_0 = compute_k(0.999,e0,ef)
R = 1
# x = np.linspace(-R,R,100)
GF = quad(lambda x: compute_gF(k_0*weight_function(x,R),e0,ef,E), -R, R)[0]
gF_inf = E*e0*(ef-e0)
# plt.plot(x,weight_function(x,R))
print("G_F: {}, l_d {}".format(GF,GF/gF_inf))
# print(quad(lambda x: damage_response(k_0*weight_function(x,R),e0,ef), -R, R)[0])
# plt.show()

ef_values = np.linspace(2,100,5)
# ef_values = [2,3,4]
for i,ef in enumerate(ef_values):
    d_vals = np.linspace(0,0.9999999,100)
    gf = np.zeros(d_vals.shape)
    for j,d in enumerate(d_vals):
        k_0 = compute_k(d,e0,ef)
        GF = quad(lambda x: compute_gF(k_0*weight_function(x,R),e0,ef,E), -R, R)[0]
        gF_inf = E*e0*(ef-e0)
        # print("{} {}".format(ef,GF/gF_inf))
        gf[j] = GF/gF_inf
    plt.plot(d_vals,gf,label="ef={:.1f}".format(ef))
# plt.yscale("log")
plt.legend()
plt.show()
