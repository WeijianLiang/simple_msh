from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
import numpy as np

elements =np.loadtxt('elements.txt',dtype='int')


vertices =np.loadtxt('vertices.txt')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


lw =1.5

ax.plot3D(vertices[elements[:8],0],vertices[elements[:8],1],vertices[elements[:8],2],'r-',linewidth=lw,label='0~7')
ax.plot3D(vertices[elements[8:24],0],vertices[elements[8:24],1],vertices[elements[8:24],2],'b--',linewidth=lw,label='8~23')
ax.plot3D(vertices[elements[24:36],0],vertices[elements[24:36],1],vertices[elements[24:36],2],'g--',linewidth=lw,label='24~35')
ax.plot3D(vertices[elements[36:48],0],vertices[elements[36:48],1],vertices[elements[36:48],2],'c--',linewidth=lw,label='26~47')
ax.plot3D(vertices[elements[48:64],0],vertices[elements[48:64],1],vertices[elements[48:64],2],'y--',linewidth=lw,label='48~63')



ax.scatter(vertices[elements[0],0],vertices[elements[0],1],vertices[elements[0],2],marker='s',c='r',s=20,label='start point',edgecolor='r')
ax.scatter(vertices[elements[8],0],vertices[elements[8],1],vertices[elements[8],2],marker='s',c='b',s=20,edgecolor='b')
ax.scatter(vertices[elements[24],0],vertices[elements[24],1],vertices[elements[24],2],marker='s',c='g',s=20,edgecolor='g')
ax.scatter(vertices[elements[36],0],vertices[elements[36],1],vertices[elements[36],2],marker='s',c='c',s=20,edgecolor='c')
ax.scatter(vertices[elements[48],0],vertices[elements[48],1],vertices[elements[48],2],marker='s',c='y',s=20,edgecolor='y')



print vertices[elements[:8]]

ax.scatter(vertices[:,0],vertices[:,1],vertices[:,2],marker='o',c='k',s=15,edgecolor='none')

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

ax.legend(loc='upper center', ncol=3)

# plt.show()



ax.view_init(elev=20., azim=330)
plt.savefig('a_modify',format='pdf')

