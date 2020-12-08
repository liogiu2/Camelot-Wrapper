(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        alchemyShop - location
        blackSmith - location
        bob - character
        luca - character
        alchemyShop.chest - furniture
        blackSmith.table - furniture
        RedKey - item
    )
    
    (:init
        (at bob alchemyShop)
        (at luca alchemyShop)
        (at alchemyShop.chest alchemyShop)
        (at blackSmith.table blackSmith)
        (adjacent alchemyShop blackSmith) 
        (adjacent blackSmith alchemyShop)
        (at RedKey alchemyShop)
        (equip RedKey luca)
        
    )
    
    (:goal
        (and(equip RedKey bob)
        (at bob blackSmith))
        
    )
        
)