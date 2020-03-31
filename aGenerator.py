from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import numpy as np
import os
import matplotlib.pyplot as plt




# Output option
mesh_file_output = True
p_file_output = False
p_vol_file_output = False
p_pre_file_output = False

n_vel_bc_file_output = True
n_pre_bc_file_output = False
p_file_output = False
p_vol_file_output = False

ppc = 16  # particle per cell
p = 0

mlim = [0., 56, 0, 16]
mesh_size = 0.5

plim = [0, 56, 0, 16]
polygon = Polygon([(0,0),(56,0),(56,6),(36,6),(18,15),(0,15)])
#polygon = Polygon([(0,0),(1,0),(1,1),(0,1)])

# Nodal velocity bc (0 velocity)
# format:= [[xmin,xmax,ymin,ymax,direction]]
# direction:= 0->solid x, 1->solid y, 2->fluid x, 3->fluid y

bcv = [[0., 56., 0., 0., 0], 
[0., 0., 0., 16., 1],
[56, 56, 0., 16., 1],
[0, 34, 0., 0, 10],
[18,18,0,16,11],
[36,36,0,16,12]]


p_bcv = [[1., 1., 0., 1., 0], 
[0., 1., 1., 1., 1]]

a=mesh_size/np.sqrt(ppc)*2
p_bcv_polygon=Polygon([(56,6),(36,6),(18,15),(0,15),(0,15-a),(18-0.5*a,15-a),(36-a,6-a),(56,6-a)])
p_bcv_polygon2=Polygon([(56,6),(0,6),(0,0),(56,0)])




#polygon = Polygon([(0,0),(1,0),(1,1),(0,1)])

# Nodal velocity bc (0 velocity)
# format:= [[xmin,xmax,ymin,ymax,direction]]
# direction:= 0->solid x, 1->solid y, 2->fluid x, 3->fluid y






















n_bc_p = [[0., 3., 0., 0., 0]]

fig1, ax1 = plt.subplots()
# Nodal traction bc
# format:= [[xmin,xmax,ymin,ymax,direction,value]]
#bct = [[  0,  0.1,  1,  1, 1, -1e4]]

# pt pressure bc
# format:= [[xmin,xmax,ymin,ymax,value]]
ptbcp = []
#ptbcp = [[  0,  0.02,  1-0.5*dcell,  1,  0]]

# pt traction bc
# format:= [[xmin,xmax,ymin,ymax,direction,value]]
stress = -10e3
f = stress
#ptbct = [[  0,  0.02,  1-0.5*dcell,  1, 1, f]]
ptbct = []

# Mesh file
nx = int(np.round((mlim[1] - mlim[0]) / mesh_size) + 1)
ny = int(np.round((mlim[3] - mlim[2]) / mesh_size) + 1)
mx = np.linspace(mlim[0], mlim[1], nx)
my = np.linspace(mlim[2], mlim[3], ny)

xv, yv = np.meshgrid(mx, my)

mpos = np.concatenate((xv.reshape(-1, 1), yv.reshape(-1, 1)), axis=1)

nele = (nx - 1) * (ny - 1)
node = np.zeros((nele, 4))

for i in xrange(nele):
    a = np.floor(i / (nx - 1)) + i
    node[i, :] = np.asarray([a, a + 1, a + nx + 1, a + nx])


mesh_file = "mesh.txt"

f_m = open(mesh_file, "w")
head = '{}\n{}\n{} {} \n'.format("#! elementShape quadrilateral",
                                 "#! elementNumPoints 4", nx * ny, nele)

f_m.write(head)
np.savetxt(f_m, mpos, fmt="%.7f", delimiter="\t")
np.savetxt(f_m, node, fmt="%i", delimiter="\t")
f_m.close()

#plot mesh
Z = np.zeros(xv.shape)
plt.pcolor(xv,yv,Z,cmap='RdBu',vmin=-1, vmax=1,edgecolor='k')



# Mesh constrain
nbcv = len(bcv)
e = 1.e-8
n_vel_bc_file = "velocity-constraint.txt"
f_bcv = open(n_vel_bc_file, "w")

for i in xrange(nbcv):
    f_bcv.write('n_set: {}\ndirection: {}\n'.format(i, bcv[i][4]))
    index = []
    for j in xrange(nx * ny):
        if ((bcv[i][0] - e) < mpos[j, 0] < (bcv[i][1] + e)) and ((bcv[i][2] - e) < mpos[j, 1] < (bcv[i][3] + e)):
            index.append(j)
    index = np.asarray(index)
    if (bcv[i][4]==0):
        plt.plot(mpos[index][:,0],mpos[index][:,1],'rx')
    elif (bcv[i][4]==1):
        plt.plot(mpos[index][:,0],mpos[index][:,1],'r-')
    np.savetxt(f_bcv, index, fmt="%i", newline=", ")
    f_bcv.write('\n')
f_bcv.close()


# Mesh constrain: pore pressure
n = len(n_bc_p)
e = 1.e-8
n_pre_bc_file = "pore-pressure-constraint.txt"
f_bc_p = open(n_pre_bc_file, "w")

for i in xrange(n):
    index = []
    for j in xrange(nx * ny):
        if ((n_bc_p[i][0] - e) < mpos[j, 0] < (n_bc_p[i][1] + e)) and ((n_bc_p[i][2] - e) < mpos[j, 1] < (n_bc_p[i][3] + e)):
            index.append(j)
    index = np.asarray(index)
    bc_p = np.ones((len(index), 1)) * n_bc_p[i][4]

    plt.plot(mpos[index][:,0],mpos[index][:,1],'bs',markersize=2, markeredgewidth=0)
    pore_pressure_constrain = np.concatenate((index.reshape(-1,1), bc_p), axis=1)
    f_bc_p.write('{}\n'.format(len(index)))
    np.savetxt(f_bc_p, pore_pressure_constrain, fmt="%i", newline="\n")
f_bc_p.close()



# point file
np_each_dim = np.round(np.sqrt(ppc))
nx = int(np.round((plim[1] - plim[0]) / mesh_size) * np_each_dim)
ny = int(np.round((plim[3] - plim[2]) / mesh_size) * np_each_dim)
pt_size = mesh_size / np_each_dim
mx = np.linspace(plim[0] + 0.5 * pt_size, plim[1] - 0.5 * pt_size, nx)
my = np.linspace(plim[2] + 0.5 * pt_size, plim[3] - 0.5 * pt_size, ny)

xv, yv = np.meshgrid(mx, my)
ppos = np.concatenate((xv.reshape(-1, 1), yv.reshape(-1, 1)), axis=1)

#sort pt index based on x coordinate
newpos = ppos[ppos[:,0].argsort()]


index=[]
for i in xrange(len(newpos)):
    point = Point(newpos[i][0],newpos[i][1])
    if polygon.contains(point):
        index.append(i)



n_pt=len(index)
final_ppos = newpos[index]


# Pt File
p_file = "particle.txt"
f_p = open(p_file, "w")
head = '{0:d}\n'.format(len(index))
f_p.write(head)
np.savetxt(f_p, final_ppos, fmt="%.7f", delimiter="\t")
f_p.close()


# Particle free surface from line
index = []
index2=[]
pore_p=[]
stress=[]
phi =15. 
j=0
K0=1-np.sin(phi/180*3.1415926)
nu=0.3
for i in xrange(n_pt):
    point = Point(final_ppos[i][0],final_ppos[i][1])
    if p_bcv_polygon.contains(point):
        index.append(i)
        for l in range(j,i+1):
            p=(final_ppos[i][1]-final_ppos[l][1])*9.81*1000
            sigmayy= -(final_ppos[i][1]-final_ppos[l][1])*9.81*(2000*0.7+1000*0.3-1000)
            sigmaxx= K0*sigmayy
            sigmazz= sigmaxx
            sigmaxy= 0

            pore_p.append(p)
            stress.append([sigmaxx,sigmayy,sigmazz,0,0,0])
        j=i+1
    if p_bcv_polygon2.contains(point):
        index2.append(i)




pore_p = np.asarray(pore_p)
stress =np.asarray(stress)

f_p_pore_pressure = open("particle-pore-pressure.txt","w")
head = '{0:d}\n'.format(n_pt)
f_p_pore_pressure.write(head)
np.savetxt(f_p_pore_pressure, pore_p)

f_p_stress = open("particle-stress.txt","w")
head = '{0:d}\n'.format(n_pt)
f_p_stress.write(head)
np.savetxt(f_p_stress, stress)
# # Particle free surface from polygon
# n = len(p_bcv)
# e = pt_size
# f_bc_p = open(p_pre_bc_file, "w")

# index = []
# for j in xrange(n_pt):
#     point = Point(final_ppos[j][0],final_ppos[j][1])
#     if p_bcv_polygon.contains(point):
#         index.append(j)


index = np.asarray(index)
p_free_surface = "free-surface-particle.txt"
np.savetxt(p_free_surface, index, fmt="%i", newline=", ")


index2 = np.asarray(index2)
bottom = "bottom-particle.txt"
np.savetxt(bottom, index2, fmt="%i", newline=", ")







# f_bc_v.close()
plt.plot(final_ppos[index,0],final_ppos[index,1],'r*', markersize=1.5, markeredgewidth=0)




# # creat mesh and particle


# p_pre_file = "particle-pore-pressure.txt"

# # b.c.
# # nodal b.c.



# # point b.c.
# p_vel_bc_file = "particle-velocity-constraint.txt"
# p_pre_bc_file = "particle-pore-pressure-constraint.txt"

# # pt pore pressure
# f_ptp = open(p_pre_file, "w")
# porepressure = np.ones((len(index), 1)) * p
# head = '{}\n'.format(len(index))

# f_ptp.write(head)
# np.savetxt(f_ptp, porepressure, fmt="%.7f", delimiter="\t")
# f_ptp.close()

# plt.plot(final_ppos[:,0],final_ppos[:,1],'b.', markersize=1.5, markeredgewidth=0)
# #plt.axis(np.asarray([0., 60, 0, 15])+np.asarray([-1,1,-1,1]))

ax1.set_aspect('equal')
plt.savefig('geometry.pdf')
