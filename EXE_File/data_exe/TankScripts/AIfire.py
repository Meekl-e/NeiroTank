




def check_fire(Tankmap):

    Tankmap = [[-1 if char == 'B' else char for char in inner_list] for inner_list in Tankmap]

    center = len(Tankmap)//2
    sides = {"right":0, "left":0, "down":0, "up":0}
    for numberSide in ["right", "left", "down", "up"]:
        for sideIndex in range(1,center):
            if numberSide == "right":

                if Tankmap[center-1][center+sideIndex] > 0 or Tankmap[center+1][center+sideIndex] > 0 or Tankmap[center][center+sideIndex] > 0:
                    sides[numberSide]+=1
            elif numberSide == "left":

                if Tankmap[center-1][center-sideIndex] > 0 or Tankmap[center+1][center-sideIndex] > 0 or Tankmap[center][center-sideIndex] > 0:
                    sides[numberSide]+=1
            elif numberSide == "up":

                if Tankmap[center-sideIndex][center-1] > 0 or Tankmap[center-sideIndex][center+1] > 0 or Tankmap[center-sideIndex][center] > 0:
                    sides[numberSide]+=1
            elif numberSide == "down":

                if Tankmap[center+sideIndex][center-1] > 0 or Tankmap[center+sideIndex][center+1] > 0 or Tankmap[center+sideIndex][center] >0:
                    sides[numberSide]+=1
    if all(map(lambda x:x==0, sides.values())):
        return "None"
    m = max(sides, key=lambda x:sides[x])
    return m
