(define (domain CamelotDomain)
    (:requirements :typing)


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
        (spell-hit ?character - character)
    )

    (:action move
        :parameters (?who - character
            ?from ?to - location)
        :precondition (at ?who ?from)
        :effect (and (at ?who ?to)
            (not (at ?who ?from))))
    
    (:action attack-true-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) (at ?whom ?room))
        :effect (and (at ?who ?room) (at ?whom ?room) (bleeding ?whom) ) 
    )
    
    (:action attack-false-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) (at ?whom ?room))
        :effect (and (at ?who ?room) (at ?whom ?room)) 
    )

    (:action bash
        :parameters (?who - character ?where - location ?forniture - forniture)
        :precondition (and (at ?who ?where) (at ?forniture ?where))
        :effect (and(at ?who ?where) (at ?forniture ?where))
    )

    (:action cast-no-target
        :parameters (?caster - character)
        :precondition (and )
        :effect (and )
    )

    (:action cast-with-target
        :parameters (?caster - character ?target - character ?location - location)
        :precondition (and (at ?caster ?location) (at ?target ?location))
        :effect (and (at ?caster ?location) (at ?target ?location) (spell-hit ?target))
    )
    
    
    
)