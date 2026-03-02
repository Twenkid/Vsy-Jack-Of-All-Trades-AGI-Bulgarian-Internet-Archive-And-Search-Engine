# Vsy * Вседържец 
## Tools 

Backup, file transfer, Petak I etc.:

rsync  

https://www.tecmint.com/rsync-local-remote-file-synchronization-commands/

graphs, voxels, kd-trees; pybind  ... C++, Py

nanoflann (kd-tree), networks(py) bonxai (voxel)

**Graphs**

28.2.2026

**nanoflann**

* KD-Trees, nearest neighbour

```
sudo apt install libnanoflann-dev
sudo apt-get install build-essential cmake libgtest-dev libeigen3-dev
mkdir build && cd build && cmake ..
make && make test
./saveload_example
./pointcloud_adaptor_example
./pointcloud_kdd_radius

-- extend the dimensions

```

See examples, utils.h, ... 


https://github.com/jlblancoc/nanoflann/blob/master/examples/utils.h

https://github.com/jlblancoc/nanoflann/blob/master/examples/KDTreeVectorOfVectorsAdaptor.h

https://github.com/jlblancoc/nanoflann/blob/master/examples/matrix_example.cpp

etc.

...

**Networkit** 

- Python, C++ backend

https://networkit.github.io/


**Bonxai**  2.3.2026

Fast, hierarchical, sparse Voxel Grid
https://github.com/jlblancoc/Bonxai 
https://github.com/jlblancoc/Bonxai/blob/main/examples/bonxai_map_playground.cpp
https://github.com/jlblancoc/Bonxai/blob/main/examples/test_serialization.cpp

#include "bonxai/bonxai.hpp"

```C++

double voxel_resolution = 0.05;
Bonxai::VoxelGrid<int> grid( voxel_resolution );

//Nothing prevents you from having more complex cell values, for instance:

Bonxai::VoxelGrid<Eigen::Vector4d> vector_grid( voxel_resolution );

//To insert values into a cell with coordinates x, y and z, use a VoxelGrid::Accessor object.
//Dense cube of cells with value 42:

// create the accessor ONCE and reuse it as much as possible

auto accessor = grid.createAccessor();

for( double x = 0; x < 1.0; x += voxel_resolution )
{
  for( double y = 0; y < 1.0; y += voxel_resolution )
  {
    for( double z = 0; z < 1.0; z += voxel_resolution )
    {
      Bonxai::CoordT coord = grid.posToCoord( x, y, z );
      accessor.setValue( coord, 42 );
    }
  }
}

// If the value of the cell has never been set, return nullptr
int* value = accessor.value( coord );
```
**binder: C++11-->Py**

https://github.com/RosettaCommons/binder
