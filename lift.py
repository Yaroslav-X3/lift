import time
import random

generic_chance = 0.8
first_floor_chance = 0.5
#-- час, що проходить під час переміщення між поверхами (величина ОБЕРНЕНА до ШВИДКОСТІ ліфта) --
move_time = 3
idle_time = move_time*2
#-- True - вгору, False - вниз --
current = 1

s ={1: "generic",
 2: "vip",
 3: "service"}

floors = 25

class Passenger:
    def __init__(self, id_, floor, destination, status):
        self.id_ = id_
        self.floor = floor
        self.destination = destination
        self.status = s[status]

class Call:
    def __init__(self, id_, floor):
        self.id_ = id_
        self.floor = floor

def on_current_floor(pas):
    if pas.floor == current: return True
    return False
def delete_arrived(pas):
    if pas.floor != current: return True
    return False
def delete_entered(pas):
    if pas.floor != current: return True
    return False

def main():
    global current
    queue = []
    passengers_traveling = []
    subqueue = []
    subqueue_2 = []
    count = 0
    timer = 0
    direction = True
    while True:
        floor=1
        destination=1
        time.sleep(0.1)
        r=random.random()
        if r<0.5:
            r=random.random()
            f_list=list(range(25))
            #-- якщо початковий поверх - НЕ перший --
            if r>first_floor_chance:
                floor = round((r-first_floor_chance)/(1-first_floor_chance)*(floors-1)+1)
                f_list.remove(floor)
            r=random.random()
            #-- отже, початковий поверх - НЕ перший --
            if floor!=1:
                #-- початковий поверх --
                if r>first_floor_chance:
                    destination = round((r-first_floor_chance)/(1-first_floor_chance)*(floors-2)+1)
            #-- якщо початковий поверх - перший
            else:
                destination = round(r*(floors-2)+1)
            destination = f_list[destination]
            e = Passenger(count,floor,destination,1)
            count+=1
            queue.append(e)
        
        #-- якщо підчерга порожня, але вже є виклики (ліфт щойно дізнався про виклики) --
        if(not subqueue and queue):
            if(queue[0].destination>queue[0].floor): direction = True
            else: direction = False

        subqueue = list(i.floor for i in queue)
        if direction:
            for i in range(1,current):
                if i in subqueue: subqueue.remove(i)
        else:
            for i in range(current+1,floors+1):
                if i in subqueue: subqueue.remove(i)
        subqueue.extend(subqueue_2)
        subqueue=list(set(subqueue))
        subqueue.sort(reverse = not direction)
        #-- якщо ліфт перебуває на поверсі, на якому викликали --
        if subqueue and subqueue[0] == current:
            #-- якщо відлік скоро почнеться --
            if (timer+1)%move_time==0:
                #-- вивантажити пасажирів, що їдуть на цей поверх --
                passengers_traveling=list(filter(delete_arrived, passengers_traveling))
                #-- доповнити список пасажирів, що їдуть, поверхами призначення --
                subqueue.extend(list(set(i.destination for i in list(filter(on_current_floor,queue)))))
                subqueue_2.extend(list(set(i.destination for i in list(filter(on_current_floor,queue)))))
                passengers_traveling.extend(i for i in list(filter(on_current_floor,queue)))
                #-- видалити з підчерги пасажирів, що вже сіли у ліфт --
                subqueue.remove(current)
                queue=list(i for i in list(filter(delete_entered,queue)))
        #-- якщо ліфту треба рухатися до найближчого поверху --
        else:
            if timer%move_time==0:
                #-- алгоритм 1: якщо містить пасажирів
                if passengers_traveling:
                    if subqueue and direction: current+=1
                    elif subqueue: current-=1
                #-- алгоритм 2: якщо їде на перший виклик
                else:
                    if subqueue and subqueue[0]>current: current+=1
                    elif subqueue and subqueue[0]<current: current-=1
        #-- output --
        
        print('QUEUE')
        for pas in queue:
            print(f'Data: departure: {pas.floor}, destination: {pas.destination}')
        print('SUBQUEUE')
        for i in subqueue:
            print(f'Data: {i}')
        print('PASSENGERS TRAVELING')
        for i in passengers_traveling:
            print(f'Data: departure: {pas.floor}, destination: {pas.destination}')
        print('\n')
        print(f'Elevator\'s current floor: {current}')
        
        timer+=1

if __name__ == "__main__":
    main()
