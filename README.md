# GraphEditor

Interaction via the command line
```
,____________________________,________________,__________________________________,
|      Command title         |   Arguments    |          Description             |
|____________________________|________________|__________________________________|
| # ## common                |                |                                  |
| render                     |  -             | display current graph 	         |
|____________________________|________________|__________________________________|
| # ## graph                 |                | commands for work with graph’s   |
| graph create               | id             | create graph in store            |
| graph choose               | id             | set graph as current             |
| graph delete               | id*            | delete graph from store          |
| graph rename               | id id_new      | rename graph                     |
| graph reset color          | id*            | rename graph                     |
| graph export               | id*            | save graph in file               |
| graph import               | file_name      | upload graph from file           |
| graph print in store       | -              | print all graphs ids from store  |
| graph print current        | -              | print current graph id           |
|____________________________|________________|__________________________________|
| # ## vertex                |                | commands for current graph       |
| vertex create              | id content x y | create vertex                    |
| vertex delete              | id             | delete vertex                    |
| vertex paint               | id r g b       | set color for vertex             |
| vertex content             | id content     | set for vertex with id content   |
| vertex rename              | id id_new      | rename vertex                    |
|____________________________|________________|__________________________________|
| # ## edge                  |                | commands for current graph       |
| edge create                | id v1 v2 True  | create edge, True if oriented    |
| edge delete                | id             | delete edge                      |
| edge paint                 | id r g b       | set color for edge               |
| edge rename                | id id_new      | rename edge                      |
| edge change oriented state | id             | change oriented state            |
|____________________________|________________|__________________________________|
| # ## additional            |                | events for lab                   |
| incidence matrix           | id*            | print incidence matrix           |
| find min path              | v1 v2          | print min path between vertexes  |
| graph check complete       | id*            | print if graph is complete       |
| graph make complete        | id*            | add edges to make graph complete |
| graph make circle          | id*            | shape of the graph becomes round |
| graph rename all vertexes  | id*            | names all vertices in order      |
| graph rename all edges     | id*            | names all edges in order         |
| vertex find by content     | content        | find in current graph vertex     |
|____________________________|________________|__________________________________|
| * - optional                                                                   |
|________________________________________________________________________________|
```
Interaction via window 
```
,________________________________________________________________________________,
|    Hotkey    |                        What does it do                          |
|______________|_________________________________________________________________|
| RMB          | - if pressed in an empty space, moves the camera                |
|              | - if a vertex is clicked, moves the vertex                      |
|              | - double-clicking on an empty space creates a vertex            |
|              | - buttons clicks                                                |
|______________|_________________________________________________________________|
| LMB          | - if a vertex or edge is clicked, shows info                    |
|______________|_________________________________________________________________|
| Mouse Wheel  | - change camera scale                                           |
|              | - scrolls through the graphs in the storage                     |
|______________|_________________________________________________________________|
| LCTRL + RMB  | - creates subgraph from choosed vertexes                        |
|              | - if you select a vertex of a subgraph and move it, the entire  |
|              | subgraph will move                                              |
|______________|_________________________________________________________________|
| LSHIFT       | - allows you to select a subgraph by selecting an area          |
|______________|_________________________________________________________________|
| I + RMB      | - changing vertex id (to stop vertex name input click ENTER)    |
|______________|_________________________________________________________________|
| DEL          | - deleting selected vertexes and edges                          |
|______________|_________________________________________________________________|
| E            | - creates edges between selected vertexes                       |
|______________|_________________________________________________________________|
| N            | - changes the orientation status of the selected edges          |
|______________|_________________________________________________________________|
| O            | - changes the orientation direction of the selected edges       |
|______________|_________________________________________________________________|
```

Copyright © 2021 Paplauski Eldar

<contacts: eldarpoplauski111@gmail.com>