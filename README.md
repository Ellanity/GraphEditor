# GraphEditor

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
| graph check complete       | id*            | print if graph is complete       |
| graph make complete        | id*            | add edges to make graph complete |
| vertex find by content     | content        | find in current graph vertex     |
| find min path              | v1 v2          | print min path between vertexes  |
|____________________________!________________!__________________________________|
| * - optional                                                                   |
|________________________________________________________________________________|
```
Copyright © 2021 Paplauski Eldar

<contacts: eldarpoplauski111@gmail.com>