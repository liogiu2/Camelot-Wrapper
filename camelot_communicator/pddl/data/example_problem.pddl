(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        AlchemyShop - position
        Bridge - position
        bob - player
        luca - character
        AlchemyShop.Chest - furniture
        AlchemyShop.Door - entrypoint
        Bridge.SouthEnd - entrypoint
        RedKey - item
    )
    
    (:init
        (at bob AlchemyShop)
        (at luca AlchemyShop)
        (at AlchemyShop.Chest AlchemyShop)
        (adjacent AlchemyShop.Door Bridge.SouthEnd) 
        (adjacent Bridge.SouthEnd AlchemyShop.Door)
        (stored RedKey AlchemyShop.Chest)
        (can_open AlchemyShop.Chest)
    )
    
    (:goal
        (and(equip RedKey bob)
        (at bob Bridge))
        
    )
        
)