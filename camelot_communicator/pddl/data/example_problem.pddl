(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        alchemyShop - location
        blackSmith - location
        bob - player
        luca - character
        AlchemyShop.Chest - furniture
        blackSmith.table - furniture
        RedKey - item
    )
    
    (:init
        (at bob alchemyShop)
        (at luca alchemyShop)
        (at AlchemyShop.Chest alchemyShop)
        (at blackSmith.table blackSmith)
        (adjacent alchemyShop blackSmith) 
        (adjacent blackSmith alchemyShop)
        (stored RedKey AlchemyShop.Chest)
        (can_open AlchemyShop.Chest)
    )
    
    (:goal
        (and(equip RedKey bob)
        (at bob blackSmith))
        
    )
        
)