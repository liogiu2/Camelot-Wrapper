(define (domain CamelotDomain)
    (:requirements :typing :negative-preconditions :universal-preconditions)


    (:types
        general location
        character forniture item - general
    )

    (:constants

    )
    ;TODO: include the fact that a forniture needs to be inside a place and items can be in a forniture. migth need to change some actions effects and preconditions (draw)
    (:predicates
        (at ?o - general ?l - location)
        (equip ?i - item ?c - character)
        (adjacent ?r - location ?r1 - location)
        (bleeding ?character - character)
        (spell-hit ?character - character)
        (open ?forniture)
        (dead ?character - character)
        (kneeling ?character)
        (can_open ?forniture) ;needs to be setted in places.json
    )

    ; Camelot Action:
    ; Parameters:
    ; Preconditions:
    ; Effects: 
    (:action move
        :parameters (?who - character
            ?from ?to - location)
        :precondition (and (at ?who ?from) 
            (not (dead ?who)) 
            (adjacent ?from ?to)
        )
        :effect (and (at ?who ?to)
            (not (at ?who ?from))
        )
    )
    
    ; Camelot Action: Attack with hit parameter true
    ; Parameters:
    ;               ?who ?whom character involved in the action
    ;               ?room location where the character have to be
    ; Preconditions:
    ;               ?who ?whom at the same location
    ;               ?who ?whom NOT dead
    ; Effects: 
    ;               ?whom is bleeding
    (:action attack-true-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) 
            (at ?whom ?room) 
            (not (dead ?who)) 
            (not (dead ?whom))
        )
        :effect (and 
            (bleeding ?whom) 
        ) 
    )
    
    ; Camelot Action: Attack with hit parameter false
    ; Parameters:
    ;               ?who ?whom character involved in the action
    ;               ?room location where the character have to be
    ; Preconditions:
    ;               ?who ?whom at the same location
    ;               ?who ?whom NOT dead
    ; Effects: 
    ;               None
    (:action attack-false-hit
        :parameters (?who ?whom - character ?room - location)
        :precondition (and (at ?who ?room) 
            (at ?whom ?room) 
            (not (dead ?who)) 
            (not (dead ?whom))
        )
        :effect (and ) 
    )

    ; Camelot Action: Bash
    ; Note: example of action that doesn't make sense to represent
    ; Parameters:
    ;               ?who character involved in the action
    ;               ?where location of the action
    ;               ?forniture forniture involved in the action
    ; Preconditions:
    ;               ?who ?forniture are in the same location
    ;               ?who is NOT dead
    ; Effects: 
    ;               None
    (:action bash 
        :parameters (?who - character ?where - location ?forniture - forniture)
        :precondition (and (at ?who ?where) 
            (at ?forniture ?where) 
            (not (dead ?who))
        )
        :effect (and )
    )

    ; Camelot Action: Cast without any target
    ; Parameters:
    ;               ?caster character involved in the action
    ; Preconditions:
    ;               ?caster is NOT dead
    ; Effects: 
    ;               None
    (:action cast-no-target
        :parameters (?caster - character)
        :precondition (and (not (dead ?caster)))
        :effect (and )
    )

    ; Camelot Action: Cast with target
    ; Parameters:
    ;               ?caster ?target characters involved in the action
    ;               ?location location of the action
    ; Preconditions:
    ;               ?caster ?target are NOT dead
    ;               ?caster ?target are at the same location
    ; Effects: 
    ;               None
    (:action cast-with-target
        :parameters (?caster ?target - character ?location - location)
        :precondition (and (at ?caster ?location) 
            (at ?target ?location) 
            (not (dead ?caster)) 
            (not (dead ?target))
        )
        :effect (and (at ?caster ?location) 
            (at ?target ?location) 
            (spell-hit ?target)
        )
    )
    
    		
    ; Camelot Action: Clap
    ; Parameters:
    ;               ?clapper character involved in the action
    ; Preconditions:
    ;               ?clapper is NOT dead
    ; Effects:
    ;               None
    (:action clap
        :parameters (?clapper - character)
        :precondition (and (not (dead ?clapper)))
        :effect (and )
    )

    ; Camelot Action: CloseFurniture
    ; Parameters:
    ;               ?c character involved in the action
    ;               ?f forniture to close
    ;               ?l location of forniture and character
    ; Preconditions:
    ;               ?c ?f at the same location
    ;               ?c is NOT dead
    ;               ?f is open
    ; Effects: 
    ;               ?f is NOT open
    (:action closefurniture
        :parameters (?c - character ?f - forniture ?r - location)
        :precondition (and (at ?c ?r) 
            (at ?f ?r) 
            (not (dead ?c)) 
            (open ?f)
        )
        :effect (and (not (open ?f)))
    )
	
    ; Camelot Action: Dance
    ; Parameters:
    ;               ?dancer character involved in the action
    ; Preconditions:
    ;               ?dancer is NOT dead
    ; Effects:
    ;               None
    (:action dance
        :parameters (?dancer - character)
        :precondition (and (not (dead ?dancer)))
        :effect (and )
    )

    ; Camelot Action: DanceTogether
    ; Parameters:
    ;               ?d ?d1 characters involved in the action
    ;               ?l location of the action
    ; Preconditions:
    ;               ?d ?d1 at the same location
    ;               ?d ?d1 are NOT dead
    ; Effects:
    ;               None
    (:action dancetogether
        :parameters (?d ?d1 - character ?l - location)
        :precondition (and (at ?d ?l) 
            (at ?d1 ?l) 
            (not (dead ?d)) 
            (not (dead ?d1))
        )
        :effect (and )
    )
		
    ; Camelot Action: Die
    ; Parameters:
    ;               ?c character involved in the action
    ; Preconditions:
    ;               ?c is NOT dead
    ; Effects:
    ;               ?c is dead
    (:action die
        :parameters (?c - character)
        :precondition (and (not (dead ?c)))
        :effect (and (dead ?c))
    )
    		
    ; Camelot Action: Draw
    ; Parameters:
    ;               ?c character involved in the action
    ;               ?i item involved in the action
    ;               ?l location involved in the action
    ; Preconditions:
    ;               ?c is NOT dead
    ;               ?c ?i are at the same location
    ;               ?i is NOT equipped to any other character
    ; Effects:
    ;               ?c has equipped ?i
    ;               ?i is NOT at ?l MIGTH NEED TO BE CHANGED
    (:action draw
        :parameters (?c - character ?i - item ?l - location)
        :precondition (and (not (dead ?c)) 
            (at ?c ?l) 
            (at ?i ?l) 
            (forall (?character - character) 
                (not(equip ?i ?character))
            )
        )
        :effect (and (equip ?i ?c) (not (at ?i ?l)))
    )
    		
    ; Camelot Action: Drink
    ; Parameters:
    ;               ?c character involved in the action
    ;               ?i item involved in the action
    ;               ?l location involved in the action
    ; Preconditions:
    ;               ?c is NOT dead
    ;               ?c ?i are at the same location
    ; Effects:
    ;               None
    (:action drink
        :parameters (?c - character ?i - item ?l - location)
        :precondition (and (not (dead ?c)) 
            (at ?c ?l) 
            (at ?i ?l) 
        )
        :effect (and )
    )
    		
    ; Camelot Action: Enter
    ; Parameters:
    ;               ?c character involved in the action
    ;               ?l location involved in the action
    ; Preconditions:
    ;               ?c is NOT dead
    ;               ?c is NOT at location
    ; Effects:
    ;               ?c is at location
    (:action enter
        :parameters (?c - character ?l - location)
        :precondition (and (not (dead ?c)) 
            (not (at ?c ?l))
        )
        :effect (and (at ?c ?l))
    )
    
    ; Camelot Action: Exit
    ; Parameters:
    ;               ?character is the character involved in the action.
    ;               ?location location to exit
    ; Preconditions:
    ;               ?character is NOT dead
    ;               ?character is at location to exit
    ; Effects: 
    ;               ?character is NOT in the location it previously was
    (:action exit
        :parameters (?c - character ?l - location)
        :precondition (and (not (dead ?c)) 
            (at ?c ?l)
        )
        :effect (and (not (at ?c ?l)))
    )

    ; Camelot Action: Give
    ; Parameters: 
    ;               ?giver ?receiver are the characters involved in the action.
    ;               ?item is the item that is exchanged.
    ;               ?location is used to check that the characters are in the same location.
    ; Preconditions:
    ;               ?giver ?receiver are NOT dead.
    ;               ?giver is equipped with the item.
    ;               ?giver ?receiver are in the same location
    ; Effects: 
    ;               ?giver does NOT have the item equipped anymore
    ;               ?receiver equips the item
    (:action give
        :parameters (?giver ?receiver - character ?item - item ?l - location)
        :precondition (and (not (dead ?giver) 
            (not (dead ?receiver)) 
            (equip ?item ?giver) 
            (at ?giver ?l) 
            (at ?receiver ?l))
        )
        :effect (and (not (equip ?item ?giver)) (equip ?item ?receiver))
    )
    		
    ; Camelot Action: Kneel
    ; Parameters:
    ;               ?character is the character involved in the action.
    ; Preconditions:
    ;               ?character is NOT kneeling
    ;               ?character is NOT dead
    ; Effects:
    ;               ?character is kneeling
    (:action kneel
        :parameters (?character - character)
        :precondition (and (not (kneeling ?character)) 
            (not(dead ?character))
        )
        :effect (and (kneeling ?character))
    )

    		
    ; Camelot Action: OpenFurniture
    ; Parameters:
    ;               ?character is the character involved in the action.
    ;               ?forniture is the forniture to be opened
    ;               ?location location of character and forniture
    ; Preconditions:
    ;               ?character is NOT dead
    ;               ?character ?forniture at the same location
    ;               ?forniture is NOT open
    ;               ?forniture can be opened
    ; Effects:
    ;               ?forniture is open
    (:action openfurniture
        :parameters (?character - character ?forniture - forniture ?location - location)
        :precondition (and (not(dead ?character))
            (at ?forniture ?location) 
            (at ?character ?location) 
            (not(open ?forniture)) 
            (can_open ?forniture)
        )
        :effect (and (open ?forniture))
    )
    
    		
    ; Camelot Action: Pickup
    ; Parameters:
    ;               ?character character involved in the action
    ;               ?forniture forniture involved in the action
    ;               ?location location involved in the action
    ;               ?item item involved in the action
    ; Preconditions:
    ;               ?character is NOT dead
    ;               ?forniture ?character are at the same location
    ;               ?forniture is open -- REWORK: what about a table?
    ; Effects:
    ;               
    (:action pickup
        :parameters (?character - character ?forniture - forniture ?location - location ?item - item)
        :precondition (and 
            (not(dead ?character)) 
            (at ?forniture ?location) 
            (at ?character ?location) 
            (open ?forniture) 
            (forall (?characters - character) 
                (not(equip ?item ?characters)))
        )
        :effect (and )
    )
    
    
)