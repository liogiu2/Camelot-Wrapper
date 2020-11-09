(define (domain domainExample)


    (:types
        character forniture item - object
        room - location
    )

    (:constants

    )

    (:predicates
        (at ?o - object ?l - location)
        (equip ?i - item ?c - character)
        (adjacent ?r - room ?r1 - room)
        (bleeding ?character - character)
    )

    (:action move
        :parameters (?who - character
            ?from ?to - location)
        :precondition (at ?who ?from)
        :effect (and (at ?who ?to)
            (not (at ?who ?from))))
    
    (:action attack-with-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) (at ?whom ?room))
        :effect (and (at ?who ?room) (at ?whom ?room) (bleeding ?whom) ) 
    )
    
    (:action attack-no-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) (at ?whom ?room))
        :effect (and (at ?who ?room) (at ?whom ?room)) 
    )
)