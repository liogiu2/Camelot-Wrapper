(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        AlchemyShop - location 
        Tavern - location
        City - location
        bob - player
        father - character
        arnell - character
        AlchemyShop.Chest - furniture
        AlchemyShop.Door - entrypoint
        City.GreenHouseDoor - entrypoint
        City.Bench - furniture
        Tavern.Door - entrypoint
        Tavern.BackDoor - entrypoint
        Tavern.Fireplace - furniture
    )
    
    (:init
        (in bob AlchemyShop)
        (in father Tavern)
        (at father Tavern.Fireplace)
        (in arnell City)
        (at arnell City.Bench)
        (at bob AlchemyShop.Door)
        (at AlchemyShop.Chest AlchemyShop)
        (adjacent AlchemyShop.Door Tavern.BackDoor) 
        (adjacent Tavern.BackDoor AlchemyShop.Door)
        (adjacent Tavern.Door City.GreenHouseDoor) 
        (adjacent City.GreenHouseDoor Tavern.Door)
        (can_open AlchemyShop.Chest)
        (alive bob)
        (alive father)
        (alive arnell)
    )
    
    (:goal
        (and
        (at bob City))
        
    )
        
)