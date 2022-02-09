(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        AlchemyShop - location 
        Blacksmith - location
        bob - player
        luca - character
        AlchemyShop.Chest - furniture
        AlchemyShop.Door - entrypoint
        Blacksmith.Door - entrypoint
        RedKey - item
    )
    
    (:init
        (in bob AlchemyShop)
        (in luca Blacksmith)
        (at bob AlchemyShop.Door)
        (at AlchemyShop.Chest AlchemyShop)
        (adjacent AlchemyShop.Door Blacksmith.Door) 
        (adjacent Blacksmith.Door AlchemyShop.Door)
        (stored RedKey AlchemyShop.Chest)
        (can_open AlchemyShop.Chest)
        (alive bob)
        (alive luca)
    )
    
    (:goal
        (and(equip RedKey bob)
        (at bob Blacksmith))
        
    )
        
)