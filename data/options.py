opcoesDic = {
    "goOurBase" : ["getResourcesBase", "defend", "goMid"],
    "goMid" : ["goOurBase", "fight", "getResourcesMid", "goEnemyBase"],
    "goEnemyBase" : ["goMid", "breakNexus", "fight", "stealResources"]
}