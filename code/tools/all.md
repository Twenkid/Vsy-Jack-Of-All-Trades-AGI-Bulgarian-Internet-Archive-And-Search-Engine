# Vsy * Вседържец 
## Tools 

Backup, file transfer, Petak I etc.:

rsync  

https://www.tecmint.com/rsync-local-remote-file-synchronization-commands/

graphs, voxels, kd-trees; pybind  ... C++, Py

nanoflann (kd-tree), networks(py) bonxai (voxel)


**Graphs**

28.2.2026+

**nanoflann**

* C++, KD-Trees, nearest neighbour

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

C++ graphs: headers only etc.: 

* https://github.com/haasdo95/graphlite
* https://github.com/ZigRazor/CXXGraph  --  Directed and undirected graphs; ✅ Dijkstra, A*, BFS, DFS; ✅ Zero dependencies; ✅ C++17 and above
* https://github.com/luk036/xnetwork-cpp/  .... https://luk036.github.io/xnetwork-cpp/
* https://github.com/haasdo95/graphlite  ... find a node by value
* boost ..  https://www.boost.org/doc/libs/latest/libs/graph/doc/index.html

...
**Networkx** 

- Python

https://networkx.org/en/

https://networkx.org/documentation/stable/tutorial.html

https://networkx.org/nx-guides/index.html

https://networkx.org/nx-guides/content/algorithms/lca/LCA.html

https://networkx.org/nx-guides/content/algorithms/isomorphism/isomorphism.html#vf2

* Accelerators: https://rapids.ai/nx-cugraph/

  pip install nx-cugraph-cu13 --extra-index-url https://pypi.nvidia.com

NX_CUGRAPH_AUTOCONFIG=True

python n1.py

Colab:

%env NX_CUGRAPH_AUTOCONFIG=True
import networkx

  etc.
```
import networkx as nx
import pandas as pd

url = "https://data.rapids.ai/cugraph/datasets/cit-Patents.csv"
df = pd.read_csv(url, sep=" ", names=["src", "dst"], dtype="int32")
G = nx.from_pandas_edgelist(df, source="src", target="dst")

%time result = nx.betweenness_centrality(G, k=10)
user@machine:/# ipython demo.ipy

CPU times: user 7min 36s, sys: 5.22 s, total: 7min 41s
Wall time: 7min 41s
user@machine:/# NX_CUGRAPH_AUTOCONFIG=True ipython demo.ipy

CPU times: user 4.14 s, sys: 1.13 s, total: 5.27 s
Wall time: 5.32 s
*NetworkX 3.4.1, nx-cugraph 24.10, CPU: Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz 45GB RAM, GPU: NVIDIA Quadro RTX 8000 50GB RAM
```
https://github.com/networkx/nx-parallel  
(pip install nx-parallel ... v0.2! in the repo 0.4 - .config ... - not like in the example) 10.3.2026

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
