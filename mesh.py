import numpy


def cube_mesh(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, zmin=0.0, zmax=1.0, sizex=1, sizey=1, sizez=1):
    """Canonical tetrahedrization of the cube.
    Input:
    Edge lenghts of the cube
    Number of nodes along the edges.
    """
    # # Generate suitable ranges for parametrization
    # x_range = numpy.linspace(xmin, xmax, nx)
    # y_range = numpy.linspace(ymin, ymax, ny)
    # z_range = numpy.linspace(zmin, zmax, nz)

    # Generate suitable ranges for parametrization
    x_range = numpy.arange(xmin, xmax+1.e-15, sizex)
    y_range = numpy.arange(ymin, ymax+1.e-15, sizey)
    z_range = numpy.arange(zmin, zmax+1.e-15, sizez)

    nx=x_range.shape[0]
    ny=y_range.shape[0]
    nz=z_range.shape[0]


    # Create the vertices.
    x, y, z = numpy.meshgrid(x_range, y_range, z_range, indexing="ij")
    # Alternative with slightly different order:
    # ```
    # nodes = numpy.stack([x, y, z]).T.reshape(-1, 3)
    # ```
    nodes = numpy.array([x, y, z]).T.reshape(-1, 3)
    
    # Hexahedron:             Hexahedron20:          Hexahedron27:
    #        v
    # 3----------2            3----13----2           3----13----2
    # |\     ^   |\           |\         |\          |\         |\
    # | \    |   | \          | 15       | 14        |15    24  | 14
    # |  \   |   |  \         9  \       11 \        9  \ 20    11 \
    # |   7------+---6        |   7----19+---6       |   7----19+---6
    # |   |  +-- |-- | -> u   |   |      |   |       |22 |  26  | 23|
    # 0---+---\--1   |        0---+-8----1   |       0---+-8----1   |
    #  \  |    \  \  |         \  17      \  18       \ 17    25 \  18
    #   \ |     \  \ |         10 |        12|        10 |  21    12|
    #    \|      w  \|           \|         \|          \|         \|
    #     4----------5            4----16----5           4----16----5

    temp_v0 = numpy.add.outer(numpy.array(range(nx - 1)), nx * numpy.array(range(ny - 1)))
    v0 = numpy.add.outer(temp_v0, nx * ny * numpy.array(range(nz - 1))).T.flatten()

    temp_v3 = numpy.add.outer(numpy.array(range(nx-1)), nx * numpy.array(range(1, ny)))
    v3 = numpy.add.outer(temp_v3, nx * ny * numpy.array(range(nz-1))).T.flatten()

    temp_v4 = numpy.add.outer(numpy.array(range(nx-1)), nx * numpy.array(range(ny-1)))
    v4 = numpy.add.outer(temp_v4, nx * ny * numpy.array(range(1,nz))).T.flatten()

    temp_v7 = numpy.add.outer(numpy.array(range(nx-1)), nx * numpy.array(range(1,ny)))
    v7 = numpy.add.outer(temp_v7, nx * ny * numpy.array(range(1,nz))).T.flatten()

    elem = numpy.array([v0,v0,v3,v3,v4,v4,v7,v7],dtype='int').transpose()
    elem[:,1::4] +=1
    elem[:,2::4] +=1

    return nodes, elem
 


def cube_mesh_gimp(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, zmin=0.0, zmax=1.0, sizex=1, sizey=1, sizez=1):
 

    # Creat additional node for gimp
    x_range = numpy.arange(xmin-sizex, xmax+sizex+1.e-15, sizex)
    y_range = numpy.arange(ymin-sizex, ymax+sizey+1.e-15, sizey)
    z_range = numpy.arange(zmin-sizez, zmax+sizez+1.e-15, sizez)

    nx=x_range.shape[0]
    ny=y_range.shape[0]
    nz=z_range.shape[0]


    # Create the vertices.
    x, y, z = numpy.meshgrid(x_range, y_range, z_range, indexing="ij")
    nodes = numpy.array([x, y, z]).T.reshape(-1, 3)

    
    temp_v0 = numpy.add.outer(numpy.array(range(1,nx-2)), nx * numpy.array(range(2,ny-1)))
    v0 = numpy.add.outer(temp_v0, nx * ny * numpy.array(range(1,nz-2))).T.flatten()
    print v0
    temp_v1 = numpy.add.outer(numpy.array(range(0,nx-3)), nx * numpy.array(range(3,ny)))
    v1 = numpy.add.outer(temp_v1, nx * ny * numpy.array(range(0,nz-3))).T.flatten()
    print v1
    temp_v2 = numpy.add.outer(numpy.array(range(0,nx-3)), nx * numpy.array(range(2,ny-1)))
    v2 = numpy.add.outer(temp_v2, nx * ny * numpy.array(range(0,nz-3))).T.flatten()
    print v2
    temp_v3 = numpy.add.outer(numpy.array(range(0,nx-3)), nx * numpy.array(range(1,ny-2)))
    v3 = numpy.add.outer(temp_v3, nx * ny * numpy.array(range(0,nz-3))).T.flatten() 
    print v3
    temp_v4 = numpy.add.outer(numpy.array(range(0,nx-3)), nx * numpy.array(range(0,ny-3)))
    v4 = numpy.add.outer(temp_v4, nx * ny * numpy.array(range(0,nz-3))).T.flatten() 
    print v4

  
    group0 = numpy.repeat([v0],8,axis=0)
    group1 = numpy.repeat([v1],16,axis=0)
    group2 = numpy.repeat([v2],12,axis=0)
    group3 = numpy.repeat([v3],12,axis=0)
    group4 = numpy.repeat([v4],16,axis=0)
    
    elem=numpy.concatenate((group0,group1,group2,group3,group4), axis=0).transpose()

    #First group
    elem[:,1] +=1
    elem[:,2] +=nx*ny+1
    elem[:,3] +=nx*ny
    elem[:,4] += -nx
    elem[:,5] += -nx+1
    elem[:,6] += -nx+1+nx*ny
    elem[:,7] += -nx+nx*ny

    #Second group
    elem[:,8] +=0
    elem[:,9] +=1
    elem[:,10] +=2
    elem[:,11] +=3
    elem[:,12] += nx*ny
    elem[:,13] += nx*ny+1
    elem[:,14] += nx*ny+2
    elem[:,15] += nx*ny+3
    elem[:,16] += 2*nx*ny
    elem[:,17] += 2*nx*ny+1
    elem[:,18] += 2*nx*ny+2
    elem[:,19] += 2*nx*ny+3
    elem[:,20] += 3*nx*ny
    elem[:,21] += 3*nx*ny+1
    elem[:,22] += 3*nx*ny+2
    elem[:,23] += 3*nx*ny+3

    #Third group
    elem[:,24] +=0
    elem[:,25] +=1
    elem[:,26] +=2
    elem[:,27] +=3
    elem[:,28] += nx*ny
    elem[:,29] += nx*ny+3
    elem[:,30] += 2*nx*ny
    elem[:,31] += 2*nx*ny+3
    elem[:,32] += 3*nx*ny
    elem[:,33] += 3*nx*ny+1
    elem[:,34] += 3*nx*ny+2
    elem[:,35] += 3*nx*ny+3

    #Fourth group
    elem[:,36] +=0
    elem[:,37] +=1
    elem[:,38] +=2
    elem[:,39] +=3
    elem[:,40] += nx*ny
    elem[:,41] += nx*ny+3
    elem[:,42] += 2*nx*ny
    elem[:,43] += 2*nx*ny+3
    elem[:,44] += 3*nx*ny
    elem[:,45] += 3*nx*ny+1
    elem[:,46] += 3*nx*ny+2
    elem[:,47] += 3*nx*ny+3

    #Fifth group
    elem[:,48] +=0
    elem[:,49] +=1
    elem[:,50] +=2
    elem[:,51] +=3
    elem[:,52] += nx*ny
    elem[:,53] += nx*ny+1
    elem[:,54] += nx*ny+2
    elem[:,55] += nx*ny+3
    elem[:,56] += 2*nx*ny
    elem[:,57] += 2*nx*ny+1
    elem[:,58] += 2*nx*ny+2
    elem[:,59] += 2*nx*ny+3
    elem[:,60] += 3*nx*ny
    elem[:,61] += 3*nx*ny+1
    elem[:,62] += 3*nx*ny+2
    elem[:,63] += 3*nx*ny+3


    return nodes, elem

def save_mesh(nodes, mesh, name):
    mesh_file = name+".txt"
    f_m = open(mesh_file, "w")

    head = '#! elementShape hexahedron\n#! elementNumPoints {}\n{} {} \n'.format(
                                 elem.shape[1], nodes.shape[0], elem.shape[0])
    f_m.write(head)
    numpy.savetxt(f_m, nodes, fmt="%.3f", delimiter="\t")
    numpy.savetxt(f_m, elem, fmt="%i", delimiter="\t")
    f_m.close()



def cube_particle(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, zmin=0.0, zmax=1.0, size=1.):


    # Generate suitable ranges for parametrization
    x_range = numpy.arange(xmin+0.5*size, xmax, size)
    y_range = numpy.arange(ymin+0.5*size, ymax, size)
    z_range = numpy.arange(zmin+0.5*size, zmax, size)

    # Create the vertices.
    x, y, z = numpy.meshgrid(x_range, y_range, z_range, indexing="ij")
    particles = numpy.array([x, y, z]).T.reshape(-1, 3)
    
    return particles








#nodes, elem = cube_mesh(xmin=0.0, xmax=10.0, ymin=0.0, ymax=10.0, zmin=0.0, zmax=10.0, sizex=0.5, sizey=0.5, sizez=0.5)


nodes,elem = cube_mesh_gimp(xmin=1.0, xmax=9.0, ymin=1.0, ymax=9.0, zmin=1.0, zmax=9.0, sizex=1, sizey=1, sizez=1)
save_mesh(nodes, elem, "gimp_mesh")

print numpy.where(nodes[:,2]<1.01)



# particles=cube_particle(xmin=3, xmax=7, ymin=3, ymax=7, zmin=6, zmax=9, size=0.25)
# particle_file = "particles.txt"
# f_p = open(particle_file, "w")
# head = '{}\n'.format(particles.shape[0])
# f_p.write(head)
# numpy.savetxt(f_p, particles, fmt="%.7f", delimiter="\t")
# f_p.close()
# print "number", particles.shape[0]
# print particles