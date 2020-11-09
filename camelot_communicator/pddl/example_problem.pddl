(define (problem example)
    (:domain domainExample)
    
    (:objects
        alchemyShop - room
        blackSmith - room
        bob - character
        chest - forniture
        table - forniture
        key - item
    )
    
    (:init
        (at bob alchemyShop)
        (at chest alchemyShop)
        (at table blackSmith)
        (adjacent alchemyShop blackSmith) 
        (adjacent blackSmith alchemyShop)
    )
    
    (:goal
        (at bob blackSmith))
        
)