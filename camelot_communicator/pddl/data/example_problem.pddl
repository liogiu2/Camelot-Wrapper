(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        AlchemyShop - location 
        Bridge - location
        bob - player
        luca - character
        AlchemyShop.Chest - furniture
        AlchemyShop.Door - entrypoint
        Bridge.SouthEnd - entrypoint
        RedKey - item
    )
    
    (:init
        (in bob AlchemyShop)
        (in luca AlchemyShop)
        (at bob AlchemyShop.Door)
        (at AlchemyShop.Chest AlchemyShop)
        (adjacent AlchemyShop.Door Bridge.SouthEnd) 
        (adjacent Bridge.SouthEnd AlchemyShop.Door)
        (stored RedKey AlchemyShop.Chest)
        (can_open AlchemyShop.Chest)
        (alive bob)
        (alive luca)
    )
    
    (:goal
        (and(equip RedKey bob)
        (at bob Bridge))
        
    )
        
)