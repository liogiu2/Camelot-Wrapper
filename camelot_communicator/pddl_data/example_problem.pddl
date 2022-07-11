(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        AlchemyShop - location 
        City - location
        bob - player
        luca - character
        AlchemyShop.Chest - furniture
        AlchemyShop.Door - entrypoint
        City.GreenHouseDoor - entrypoint
        City.Bench - furniture
    )
    
    (:init
        (in bob AlchemyShop)
        (in luca City)
        (at luca City.Bench)
        (at bob AlchemyShop.Door)
        (at AlchemyShop.Chest AlchemyShop)
        (adjacent AlchemyShop.Door City.GreenHouseDoor) 
        (adjacent City.GreenHouseDoor AlchemyShop.Door)
        (can_open AlchemyShop.Chest)
        (alive bob)
        (alive luca)
    )
    
    (:goal
        (and
        (at bob City))
        
    )
        
)