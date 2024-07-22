# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:05:43 2024

@author: cassi
"""

flower_dict = {
    'firecracker penstemon': 'penstemon eatonni',
    'old man of the mountain': 'Tetraneuris grandiflora',
    'Magnolia': 'Magnolia',
    'black eyed susan': 'rudbeckia fulgida',
    'mountain bluebells': 'mertensia ciliata',
    'tall bluebells': 'mertensia paniculata',
    'prairie bluebells': 'mertensia lanceolata',
    'desert bluebell': 'phacelia campanularia',
    'virginian bluebells': 'mertensia virginica',
    'water bluebell': 'ruellia squarrosa',
    'english bluebells': 'hyacinthoides non-scripta',
    'spanish bluebells': 'hyacinthoides hispanica',
    'indian paintbrush': 'castilleja coccinea',
    'butterfly weed': 'asclepias tuberosa',
    'wallflower': 'erysimum capitalum',
    'Nippon Daisy': 'nipponanthemum nipponicum',
    'crown daisy': 'glebionis coronaria',
    'oopsy daisy': 'calendula officinalis',
    'golden shrub daisy': 'euryops pectinatus',
    'seaside daisy': 'erigeron glaucus',
    'painted daisy': 'chrysanthemum carinatum',
    'engelmann daisy': 'engelmannia peristenia',
    'columbine': 'aquilegia',
    'Aster': 'Aster',
    'sulfur buckwheat': 'eriogonum umbellatum',
    'emory barrel cactus': 'ferocactus emoryi',
    'fishhook barrel cactus': 'ferocactus wislizenii',
    'blue barrel cactus': 'ferocactus glaucescens',
    'goldern barrel cactus': 'echinocactus grusonii',
    'african milk barrel': 'euphorbia horrida',
    'mexican lime cactus': 'ferocactus pilosus',
    'scarlet hedgehog cactus': 'echinocereus coccineus',
    'monkshood': 'aconitum carmichaelii',
    'mount cook buttercup': 'ranunculus lyallii',
    'persian buttercup': 'ranunculus asiaticus',
    'grass leaved buttercup': 'ranunculus gramineus',
    'california buttercup': 'ranunculus californicus',
    'daffodil': 'narcissus',
    'common sunflower': 'helianthus annuus',
    'seaside woolly sunflower': 'eriophyllum staechadifolium',
    'false sunflower': 'heliopsis helianthoides',
    'ten-petaled sunflower': 'helianthus decapetalus',
    'stiff sunflower': 'helianthus pauciflorus',
    'nuttall sunflower': 'helianthus nuttallii',
    'swamp sunflower': 'helianthus angustifolius',
    'tickseed sunflower': 'bidens aristosa',
    'beach sunflower': 'helianthus debilis',
    'woodland sunflower': 'helianhus divaricatus',
    'willow leaved sunflower': 'helianthus salicifolius',
    'ashy sunflower': 'helianthus mollis',
    'sawtooth sunflower': 'healianthus grosseserratus'
    }

# dictionary of flowers with their latin name as the key and common english name as the value
latin_flowers = dict(zip(flower_dict.values(), flower_dict.keys()))


# enumerate contents of key-values in dictionary   
lfd = dict(enumerate(latin_flowers.items()))
for item in lfd.items():
    print(item)
    
# list all keys
print('KEYS: ', latin_flowers.keys())

# list all values
print('VALUES: ', latin_flowers.values())

# change value associated with a key
'''
print('original value: ', latin_flowers['penstemon eatonni'])
latin_flowers['penstemon eatonni'] = 'Eaton Beardtongue'
print('new value: ', latin_flowers['penstemon eatonni'])
'''

print(type(lfd[0])) 
print('original value: ', lfd[0][1])
key = lfd[0][0] # save the key from the enumerated dictionary
latin_flowers[key] = 'Eaton Beardtongue' # change the value associated with the key in the non-enumerated dictionary
print('new value: ', latin_flowers[key])
print(latin_flowers)
lfd = dict(enumerate(latin_flowers.items())) # rewrite the enumerated dictionary to update the changed value
print(lfd)



# How could this program operate in a distributed environment where the dictionary is spread across a cluster of nodes?

'''
This program could operate in a distributed environment with a MapReduce system. The keys and the index of each 
key value pair (which were created when enumerating the dictionary, latin_flowers) allows the data to be sorted onto 
different nodes. For example, node1 coud have the first n values, node2 the next n values, etc. using the index.
Alternatively, the keys could be sorted alphabetically and node1 could have all keys that start with "a", node2 all 
keys that start with "b", etc. Sorted key-value pairs would allow for quick lookup of requested values.
'''

# What would be the limitations of this architecture?
'''
Limitations of this program in a distributed system:
* The data is saved in two separate dictionaries (latin_flowers and lfd). This takes twice the memory, 
which is expensive for large datasets.
* Also, every time a single value is changed, the enumerated dictionary (lfd) is completely rewritten. 
This is because each item in lfd is a tuple, which cannot be modified. Therefore, the value is changed 
in the non-enumerated dictionary (latin_flowers) and then the entire dictionary is resaved in the variable lfd.

Limitations of MapReduce architecture include the following: 
* multi-iteration processes use a lot of computing resources because of the two phases, map and reduce.
* Load balancing, especially for nodes with different processing power/memory capacities.
* Wait time between mapping and reducing. The reduce function waits until all of the mapping is finished, which can 
increase idle time.
* Hard to manage continuous data streams. MapReduce is built for batch processing, so it needs everything to be stored
in the distributed file system, which is unrealistic with the Internet of Things.
* Hardware changes: most computers have multiple processors, but MapReduce works serially on each node. Cloud computing 
allows for different groups of clusters to all work on the same task. MapReduce assumes it only has one cluster to work with.
* Ensuring data privacy protection: In the cloud, multiple users use the same clusters, which MapReduce didn't anticipate.
* Power consumption  
'''

# Is there a threshold for the amount of data and the overhead of operating on a cluster?
'''
The threshold for the amount of data operating in a cluster is the combined memory/storage capacity of each node in the
cluster. You can increase the number of nodes in a cluster to process more data. However, overhead increases as the size 
of the cluster increases. The nodes need to communicate with each other for job scheduling, delegating tasks, finding 
specific values, shuffling, sorting, etc. With more nodes in the system, the more overhead communication that occurs. I 
don't know if there is a specific threshold for overhead when operating on a cluster, and it is specific to the algorithms
running, the hardware used, etc., but it is reasonable that some calculations have too much data for current systems to compute.'
'''

# References
'''
Li, R., Hu, H., Li, H., Wu, Y., & Yang, J. (2016/08//). MapReduce Parallel Programming Model: A State-of-the-Art Survey.
     International Journal of Parallel Programming, 44(4), 832-866. https://doi.org/10.1007/s10766-015-0395-0

Alchemist, T. (2010, August 23). Answer to “What is the computational complexity of the MapReduce overhead.” 
    Stack Overflow. https://stackoverflow.com/a/3548021
'''