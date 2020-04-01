#include <Eigen/Dense>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>

//Written by Christopher Wilkes, Cambridge University.

using Eigen::MatrixXd;
int main()
{

  // how many elements in each direction
  const unsigned xlen = 23;
  const unsigned ylen = 23;
  const unsigned zlen = 23;

  //Length of each element (global)
  double spacing = 0.5;

  std::vector<std::map<unsigned, std::array<double, 3>>> vertices_1;
  std::vector<std::map<unsigned, std::array<double, 3>>> vertices_2;
  std::vector<std::map<unsigned, std::array<double, 3>>> vertices_3;

  std::map<unsigned, std::array<double, 3>> vertex;

  unsigned id = 0;

  // starting coordinates

  double xorigin = -0.5;
  double xcoord = xorigin;

  double ycoord = -0.5;
  double yorigin = -0.5;

  double zorigin = -0.5;
  double zcoord = -0.5;

  unsigned counter = 0;
  unsigned size = 0;

  //! Output file
  std::string vertifilename = "vertices.txt";
  std::fstream verfile;
  verfile.open(vertifilename, std::ios::out);

  for (unsigned x = 0; x < xlen; ++x)
  {
    for (unsigned y = 0; y < ylen; ++y)
    {
      for (unsigned z = 0; z < zlen; ++z)
      {

        std::array<double, 3> coord = {xcoord, ycoord, zcoord};
        vertex.insert(std::make_pair(id, coord));

        size += 1;

        if (vertices_1.size() < 1000)
        {
          vertices_1.push_back(vertex);
        }
        else
        {

          //----------------------------------------
          if (verfile.is_open())
          {
            for (auto const &vert : vertices_1)
            {
              // std::vector<Eigen::Matrix<double, 1, 3>> output;

              for (auto const &x : vert)
              {
                if (x.first == counter)
                {
                  verfile << x.second[0] // string's value
                          << '\t' << x.second[1] << '\t' << x.second[2] << '\n';
                  ++counter;
                }
              }
            }
            //----------------------------------------
            vertices_1.clear();
          }
        }

        ++id;
        zcoord += spacing;
      }
      zcoord = zorigin;
      ycoord += spacing;
    }
    ycoord = yorigin;
    xcoord += spacing;
  }

  if (verfile.is_open())
  {
    //! Write velocities in x,y,z directions
    for (auto const &vert : vertices_1)
    {

      // std::vector<Eigen::Matrix<double, 1, 3>> output;

      for (auto const &x : vert)
      {
        if (x.first == counter)
        {
          verfile << x.second[0] // string's value
                  << '\t' << x.second[1] << '\t' << x.second[2] << '\n';
          ++counter;
        }
      }

      // auto test = vert.;
      // verfile << test << '\n';
    }
    verfile.close();
  }

  std::cout << "Checkpoint 1" << '\n';

  std::vector<Eigen::Matrix<double, 1, 64>> elements;

  //  Eigen::Matrix<int, rows, rows, cols> mesh;
  int mesh[xlen][ylen][zlen];
  Eigen::Matrix<double, 1, 64> element;

  int indices = 0;

  //(rows - 1)

  for (unsigned x = 0; x < xlen; ++x)
  {
    for (unsigned y = 0; y < ylen; ++y)
    {
      for (unsigned z = 0; z < zlen; ++z)
      {
        mesh[x][y][z] = indices;
        // std::cout << mesh[x][y][z] << ":" << x << "," << y << "," << z <<
        // '\n';

        ++indices;
      }
    }
  }

  std::cout << "Checkpoint 2" << '\n';

  for (unsigned x = 0; x < xlen; ++x)
  {
    for (unsigned y = 0; y < ylen; ++y)
    {
      for (unsigned z = 0; z < zlen; ++z)
      {

        // std::cout << mesh[x][y][z] << ":" << x << "," << y << "," << z <<
        // '\n';

        // check is not on boundaxy of mesh
        if ((x > 0) && (x < (xlen - 1)))
        {
          if ((y > 0) && (y < (ylen - 1)))
          {
            if ((z > 0) && (z < (zlen - 1)))
            {
              // yheyk if xows above and to the side to genexate a GIMP
              if (y > 1 && (zlen - z) > 2 && (xlen - x) > 2)
              {

                element << mesh[x][y][z],      // 0
                    mesh[x + 1][y][z],         // 1
                    mesh[x + 1][y][z + 1],     // 2
                    mesh[x][y][z + 1],         // 3
                    mesh[x][y - 1][z],         // 4
                    mesh[x + 1][y - 1][z],     // 5
                    mesh[x + 1][y - 1][z + 1], // 6
                    mesh[x][y - 1][z + 1],     // 7
                    mesh[x - 1][y + 1][z - 1], // 8
                    mesh[x][y + 1][z - 1],     // 9
                    mesh[x + 1][y + 1][z - 1], // 10
                    mesh[x + 2][y + 1][z - 1], // 11
                    mesh[x - 1][y + 1][z],     // 12
                    mesh[x][y + 1][z],         // 13
                    mesh[x + 1][y + 1][z],     // 14
                    mesh[x + 2][y + 1][z],     // 15
                    mesh[x - 1][y + 1][z + 1], // 16
                    mesh[x][y + 1][z + 1],     // 17
                    mesh[x + 1][y + 1][z + 1], // 18
                    mesh[x + 2][y + 1][z + 1], // 19
                    mesh[x - 1][y + 1][z + 2], // 20
                    mesh[x][y + 1][z + 2],     // 21
                    mesh[x + 1][y + 1][z + 2], // 22
                    mesh[x + 2][y + 1][z + 2], // 23
                    mesh[x - 1][y][z - 1],     // 24
                    mesh[x][y][z - 1],         // 25
                    mesh[x + 1][y][z - 1],     // 26
                    mesh[x + 2][y][z - 1],     // 27
                    mesh[x - 1][y][z],         // 28
                    mesh[x + 2][y][z],         // 29
                    mesh[x - 1][y][z + 1],     // 30
                    mesh[x + 2][y][z + 1],     // 31
                    mesh[x - 1][y][z + 2],     // 32
                    mesh[x][y][z + 2],         // 33
                    mesh[x + 1][y][z + 2],     // 34
                    mesh[x + 2][y][z + 2],     // 35
                    mesh[x - 1][y - 1][z - 1], // 36
                    mesh[x][y - 1][z - 1],     // 37
                    mesh[x + 1][y - 1][z - 1], // 39
                    mesh[x + 2][y - 1][z - 1], // 39
                    mesh[x - 1][y - 1][z],     // 40
                    mesh[x + 2][y - 1][z],     // 41
                    mesh[x - 1][y - 1][z + 1], // 42
                    mesh[x + 2][y - 1][z + 1], // 43
                    mesh[x - 1][y - 1][z + 2], // 44
                    mesh[x][y - 1][z + 2],     // 45
                    mesh[x + 1][y - 1][z + 2], // 46
                    mesh[x + 2][y - 1][z + 2], // 47
                    mesh[x - 1][y - 2][z - 1], // 48
                    mesh[x][y - 2][z - 1],     // 49
                    mesh[x + 1][y - 2][z - 1], // 50
                    mesh[x + 2][y - 2][z - 1], // 51
                    mesh[x - 1][y - 2][z],     // 52
                    mesh[x][y - 2][z],         // 53
                    mesh[x + 1][y - 2][z],     // 54
                    mesh[x + 2][y - 2][z],     // 55
                    mesh[x - 1][y - 2][z + 1], // 56
                    mesh[x][y - 2][z + 1],     // 57
                    mesh[x + 1][y - 2][z + 1], // 58
                    mesh[x + 2][y - 2][z + 1], // 59
                    mesh[x - 1][y - 2][z + 2], // 60
                    mesh[x][y - 2][z + 2],     // 61
                    mesh[x + 1][y - 2][z + 2], // 62
                    mesh[x + 2][y - 2][z + 2]; // 63

                // std::cout << x << "," << y << "," << z << '\n';
                // std::cout << mesh[x][y][z] << '\n';

                elements.push_back(element);
              }
            }
          }
        }
      }
    }
  }

  std::cout << "Checkpoint 3" << '\n';

  /*  mesh(r, c), mesh(r, c + 1), mesh(r - 1, c + 1),
       mesh(r - 1, c), mesh(r + 1, c - 1), mesh(r + 1, c),
       mesh(r + 1, c + 1), mesh(r + 1, c + 2), mesh(r, c + 2),
       mesh(r - 1, c + 2), mesh(r - 2, c + 2), mesh(r - 2, c + 1),
       mesh(r - 2, c), mesh(r - 2, c - 1), mesh(r - 1, c - 1),
       mesh(r, c - 1);/*




    /*  std::vector<Eigen::Matrix<double, 1, 4>> qelements;
      Eigen::Matrix<double, 1, 4> qelement;

      for (unsigned r = 0; r < rows; ++r) {
        for (unsigned c = 0; c < cols; ++c) {

          // check is not on boundary of mesh
          if ((r > 0)) {
            if (c < (mesh.cols() - 1)) {

              qelement << mesh(r, c), mesh(r, c + 1), mesh(r - 1, c + 1),
                  mesh(r - 1, c);

              qelements.push_back(qelement);
            }
          }
        }
      }*/

  // std::cout << mesh << '\n';
  std::cout << "elements  " << elements.size() << '\n';

  double vertices_total =
      vertices_1.size() + vertices_2.size() + vertices_3.size();

  std::cout << "vertices  " << size << '\n';

  //! Output file
  std::string elefilename = "elements.txt";
  std::fstream elefile;
  elefile.open(elefilename, std::ios::out);

  if (elefile.is_open())
  {
    //! Write velocities in x,y,z directions
    for (auto const &eles : elements)
    {
      elefile << eles << '\n';
    }
    elefile.close();
  }

  std::cout << "Checkpoint 4" << '\n';

  /* //! Output file
   std::string qelefilename = "qelements.txt";
   std::fstream qelefile;
   qelefile.open(qelefilename, std::ios::out);

   if (qelefile.is_open()) {
       //! Write velocities in x,y,z directions
       for (auto const& qeles : qelements) {
           qelefile << qeles << '\n';
       }
       qelefile.close();
   }*/

  /* verfile << "Point(" << x.first << ")={"
                    << x.second(0) // string's value
                    << "," << x.second(1) << "," << x.second(2) << ",1.0};"
                    << '\n';

                    */
}
