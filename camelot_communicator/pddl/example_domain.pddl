(define (domain CamelotDomain)
    (:requirements :typing :negative-preconditions :universal-preconditions)


    (:types
        character forniture item - object
        location
        drink - item
    )

    (:constants

    )

    (:predicates
        (at ?o - object ?l - location)
        (equip ?i - item ?c - character)
        (adjacent ?r - room ?r1 - room)
        (bleeding ?character - character)
        (spell-hit ?character - character)
        (open ?forniture)
        (dead ?character - character)
    )

    (:action move
        :parameters (?who - character
            ?from ?to - location)
        :precondition (and (at ?who ?from) (not (dead ?who)))
        :effect (and (at ?who ?to)
            (not (at ?who ?from))))
    
    (:action attack-true-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) (at ?whom ?room) (not (dead ?who)) (not (dead ?whom)))
        :effect (and (at ?who ?room) (at ?whom ?room) (bleeding ?whom) ) 
    )
    
    (:action attack-false-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) (at ?whom ?room) (not (dead ?who)) (not (dead ?whom)))
        :effect (and (at ?who ?room) (at ?whom ?room)) 
    )

    (:action bash
        :parameters (?who - character ?where - location ?forniture - forniture)
        :precondition (and (at ?who ?where) (at ?forniture ?where) (not (dead ?who)))
        :effect (and(at ?who ?where) (at ?forniture ?where))
    )

    (:action cast-no-target
        :parameters (?caster - character)
        :precondition (and (not (dead ?caster)))
        :effect (and )
    )

    (:action cast-with-target
        :parameters (?caster ?target - character ?location - location)
        :precondition (and (at ?caster ?location) (at ?target ?location) (not (dead ?caster)) (not (dead ?target)))
        :effect (and (at ?caster ?location) (at ?target ?location) (spell-hit ?target))
    )
    
    (:action clap
        :parameters (?clapper - character)
        :precondition (and (not (dead ?clapper)))
        :effect (and )
    )

    (:action closeFurniture
        :parameters (?c - character ?f - forniture ?r - location)
        :precondition (and (at ?c ?r) (at ?f ?r) (not (dead ?c)))
        :effect (and (not (open ?f)) (at ?c ?r) (at ?f ?r))
    )

    (:action dance
        :parameters (?dancer - character)
        :precondition (and (not (dead ?dancer)))
        :effect (and )
    )

    (:action dancetogether
        :parameters (?d ?d1 - character ?l - location)
        :precondition (and (at ?d ?l) (at ?d1 ?l) (not (dead ?d)) (not (dead ?d1)))
        :effect (and )
    )

    (:action die
        :parameters (?c - character)
        :precondition (and )
        :effect (and (dead ?c))
    )
    ;what is the challenge we are chasing?how do you describe the environment formally before camelot can execute the actions
    (:action draw ;TOCHECK
        :parameters (?c - character ?i - item ?l - location)
        :precondition (and (not (dead ?c)) (at ?c ?l) (at ?i ?l) 
            (forall (?character - character) 
                (not(equip ?i ?character)))
            )
        :effect (and (equip ?i ?c))
    )

    (:action drink ;TOCHECK
        :parameters (?c - character ?i - item ?l - location)
        :precondition (and (not (dead ?c)) (at ?c ?l) (at ?i ?l) )
        :effect (and )
    )

    (:action enter
        :parameters (?c - character ?l - location)
        :precondition (and (not (dead ?c)) (not (at ?c ?l)))
        :effect (and (at ?c ?l))
    )
    
    (:action action_name
        :parameters ()
        :precondition (and )
        :effect (and )
    )
    
    
)