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
    )
    
    (:init
        (in bob AlchemyShop)
        (in luca Blacksmith)
        (at luca Blacksmith.Door)
        (at bob AlchemyShop.Door)
        (at AlchemyShop.Chest AlchemyShop)
        (adjacent AlchemyShop.Door Blacksmith.Door) 
        (adjacent Blacksmith.Door AlchemyShop.Door)
        (can_open AlchemyShop.Chest)
        (alive bob)
        (alive luca)
    )
    
    (:goal
        (and
        (at bob Blacksmith))
        
    )
        
)