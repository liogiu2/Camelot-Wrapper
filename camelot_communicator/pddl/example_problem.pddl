(define (problem example)
    (:domain CamelotDomain)
    
    (:objects
        alchemyShop - location
        blackSmith - location
        bob - character
        luca - character
        chest - forniture
        table - forniture
        key - item
    )
    
    (:init
        (at bob alchemyShop)
        (at luca alchemyShop)
        (at chest alchemyShop)
        (at table blackSmith)
        (adjacent alchemyShop blackSmith) 
        (adjacent blackSmith alchemyShop)
        (at key alchemyShop)
        (equip key luca)
    )
    
    (:goal
        (and(equip key bob)
        (at bob blackSmith))
        
    )
        
)