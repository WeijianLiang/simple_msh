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
 

def cube_particle(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, zmin=0.0, zmax=1.0, size=1.):


    # Generate suitable ranges for parametrization
    x_range = numpy.arange(xmin+0.5*size, xmax, size)
    y_range = numpy.arange(ymin+0.5*size, ymax, size)
    z_range = numpy.arange(zmin+0.5*size, zmax, size)

    # Create the vertices.
    x, y, z = numpy.meshgrid(x_range, y_range, z_range, indexing="ij")

    particles = numpy.array([x, y, z]).T.reshape(-1, 3)
    
    return particles



nodes, elem = cube_mesh(xmin=0.0, xmax=10.0, ymin=0.0, ymax=10.0, zmin=0.0, zmax=10.0, sizex=0.5, sizey=0.5, sizez=0.5)


mesh_file = "mesh.txt"
f_m = open(mesh_file, "w")
head = '{}\n{}\n{} {} \n'.format("#! elementShape hexahedron",
                                 "#! elementNumPoints 8", nodes.shape[0], elem.shape[0])
f_m.write(head)
numpy.savetxt(f_m, nodes, fmt="%.7f", delimiter="\t")
numpy.savetxt(f_m, elem, fmt="%i", delimiter="\t")
f_m.close()


particles=cube_particle(xmin=3, xmax=7, ymin=3, ymax=7, zmin=6, zmax=9, size=0.25)
particle_file = "particles.txt"
f_p = open(particle_file, "w")
head = '{}\n'.format(particles.shape[0])
f_p.write(head)
numpy.savetxt(f_p, particles, fmt="%.7f", delimiter="\t")
f_p.close()
# print "number", particles.shape[0]
# print particles