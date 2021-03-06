var backgroundMap = new Map(16, 16);
backgroundMap.image = game.assets['map0.gif'];
backgroundMap.loadData([
    [228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228],
    [228,228,228,196,196,196,196,196,196,196,196,196,196,196,196,196,6,6,6,196,196,196,196,196,196,196,196,196,228,228],
    [228,196,6,6,6,196,196,196,196,196,196,196,196,196,196,6,6,6,6,6,196,196,196,196,196,6,6,196,228,228],
    [228,6,6,6,6,6,196,196,196,196,196,196,196,6,6,6,6,6,6,6,196,196,196,196,6,6,6,196,228,228],
    [228,6,6,6,6,6,6,196,196,196,196,196,196,6,6,6,6,6,6,6,6,196,196,196,6,6,6,196,228,228],
    [228,6,6,6,6,6,6,196,196,6,6,6,6,6,6,211,212,213,6,6,6,196,196,196,6,6,6,196,196,228],
    [228,6,6,6,6,6,6,196,196,6,6,6,6,6,6,227,228,229,6,6,6,6,196,196,6,6,6,6,196,228],
    [228,6,6,6,6,6,6,196,196,6,6,6,6,6,6,243,244,245,6,6,6,6,196,196,6,6,6,6,196,228],
    [228,196,6,6,6,6,196,196,196,196,6,6,6,6,6,6,6,6,6,6,6,6,196,196,6,6,6,6,6,228],
    [228,196,196,6,6,6,196,196,196,196,196,6,6,6,6,6,6,6,6,6,6,6,196,196,6,6,6,6,6,228],
    [228,196,196,196,196,196,196,196,196,196,196,196,196,196,6,6,6,6,6,6,196,196,196,196,6,6,6,6,6,228],
    [228,196,196,196,196,6,6,196,196,196,196,196,196,196,6,6,6,6,6,6,196,196,196,196,196,6,6,6,6,228],
    [228,196,196,196,6,6,6,196,6,6,196,196,196,196,6,6,6,6,6,6,196,196,196,196,196,6,6,6,6,228],
    [228,196,6,6,6,6,6,6,6,6,6,196,196,196,6,6,6,6,6,6,6,6,196,196,196,196,196,6,6,228],
    [228,6,6,6,6,6,6,6,6,6,6,6,196,196,6,6,6,6,6,6,6,6,6,196,196,196,196,196,196,228],
    [228,6,6,6,6,6,6,6,6,6,6,6,196,196,6,6,6,6,6,6,6,6,6,6,6,196,196,196,196,228],
    [228,196,6,6,6,6,6,6,6,6,6,196,196,196,6,6,6,6,6,6,6,6,6,6,6,6,196,196,196,228],
    [228,196,196,6,6,6,6,6,6,6,196,196,196,196,6,6,6,6,6,6,6,6,6,6,6,196,196,196,196,228],
    [228,228,196,196,6,6,6,6,6,196,196,196,196,196,196,196,6,6,6,6,6,6,196,196,196,196,196,196,196,228],
    [228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228,228]
],[
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,7,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,7,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,7,7,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,7,7,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,6,6,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,7,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,7,7,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
]);
backgroundMap.collisionData = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,1,1,1],
    [1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1],
    [1,1,1,1,0,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];
