(define (domain CamelotDomain)
    (:requirements :typing :negative-preconditions :universal-preconditions)


    (:types
        general other
        position item character - general
        furniture entrypoint location - position
        player - character
    )

    ;TODO: include the fact that a furniture needs to be inside a place and items can be in a furniture. migth need to change some actions effects and preconditions (draw)
    (:predicates
        (at ?o - general ?l - position)
        (in ?o - general ?l - location)
        (equip ?i - item ?c - character)
        (adjacent ?r ?r1 - entrypoint)
        (bleeding ?character - character)
        (spell-hit ?character - character)
        (is_open ?furniture - furniture)
        (alive ?character - character)
        (kneeling ?character - character)
        (can_open ?furniture - furniture) 
        (can_close ?furniture - furniture) 
        (has_surface ?furniture - furniture)
        (stored ?item - item ?furniture - furniture)
        (has_item_in_pocket ?character - character ?item - item)
    )

    ; Camelot Action: 
    ; Parameters:
    ; Preconditions:
    ; Effects: 
    ; Example: move-between-location(luca, Blacksmith, AlchemyShop, Blacksmith.Door, AlchemyShop.Door)
    (:action move-between-location
        :parameters (?who - character ?from ?to - location ?entryfrom ?entryto - entrypoint)
        :precondition (and (in ?who ?from) 
            (alive ?who)
            (adjacent ?entryfrom ?entryto)
            (at ?who ?entryfrom)
        )
        :effect (and (in ?who ?to)
            (not (in ?who ?from))
            (not (at ?who ?entryfrom))
            (at ?who ?entryto)
        )
    )

    ; Camelot Action: 
    ; Parameters:
    ; Preconditions:
    ; Effects: 
    (:action move-within-location
        :parameters (?who -character ?to - position ?loc - location)
        :precondition (and (at ?to ?loc) 
            (alive ?who)
        )
        :effect (and (at ?who ?to)
        )
    )
    
    ; Camelot Action: Attack with hit parameter true
    ; Parameters:
    ;               who whom character involved in the action
    ;               room position where the character have to be
    ; Preconditions:
    ;               who whom at the same position
    ;               who whom NOT dead
    ; Effects: 
    ;               whom is bleeding
    (:action attack-true-hit
        :parameters (?who ?whom - character ?room - position)
        :precondition (and (at ?who ?room) 
            (at ?whom ?room) 
            (alive ?who) 
            (not (alive ?whom))
        )
        :effect (and 
            (bleeding ?whom) 
        ) 
    )
    
    ; Camelot Action: Attack with hit parameter false
    ; Parameters:
    ;               who whom character involved in the action
    ;               room position where the character have to be
    ; Preconditions:
    ;               who whom at the same position
    ;               who whom NOT dead
    ; Effects: 
    ;               None
    (:action attack-false-hit
        :parameters (?who ?whom - character ?room - position)
        :precondition (and (at ?who ?room) 
            (at ?whom ?room) 
            (alive ?who) 
            (alive ?whom)
        )
        :effect (and ) 
    )

    ; Camelot Action: Bash
    ; Note: example of action that doesn't make sense to represent
    ; Parameters:
    ;               who character involved in the action
    ;               where position of the action
    ;               furniture furniture involved in the action
    ; Preconditions:
    ;               who furniture are in the same position
    ;               who is NOT dead
    ; Effects: 
    ;               None
    (:action bash 
        :parameters (?who - character ?where - position ?furniture - furniture)
        :precondition (and (at ?who ?where) 
            (at ?furniture ?where) 
            (alive ?who)
        )
        :effect (and )
    )

    ; Camelot Action: Cast without any target
    ; Parameters:
    ;               caster character involved in the action
    ; Preconditions:
    ;               caster is NOT dead
    ; Effects: 
    ;               None
    (:action cast-no-target
        :parameters (?caster - character)
        :precondition (and (alive ?caster))
        :effect (and )
    )

    ; Camelot Action: Cast with target
    ; Parameters:
    ;               caster target characters involved in the action
    ;               position position of the action
    ; Preconditions:
    ;               caster target are NOT dead
    ;               caster target are at the same position
    ; Effects: 
    ;               None
    (:action cast-with-target
        :parameters (?caster ?target - character ?position - position)
        :precondition (and (at ?caster ?position) 
            (at ?target ?position) 
            (alive ?caster) 
            (alive ?target)
        )
        :effect (and (at ?caster ?position) 
            (at ?target ?position) 
            (spell-hit ?target)
        )
    )
    
    		
    ; Camelot Action: Clap
    ; Parameters:
    ;               clapper character involved in the action
    ; Preconditions:
    ;               clapper is NOT dead
    ; Effects:
    ;               None
    (:action clap
        :parameters (?clapper - character)
        :precondition (and (alive ?clapper))
        :effect (and )
    )

    ; Camelot Action: CloseFurniture
    ; Parameters:
    ;               c character involved in the action
    ;               f furniture to close
    ;               l position of furniture and character
    ; Preconditions:
    ;               c f at the same position
    ;               c is NOT dead
    ;              f is is_open
    ; Effects: 
    ;               f is NOT is_open
    (:action closefurniture
        :parameters (?c - character ?f - furniture ?r - position)
        :precondition (and (at ?c ?r) 
            (at ?f ?r) 
            (alive ?c)
            (is_open ?f)
        )
        :effect (and (not (is_open ?f)))
    )
	
    ; Camelot Action: Dance
    ; Parameters:
    ;               dancer character involved in the action
    ; Preconditions:
    ;               dancer is NOT dead
    ; Effects:
    ;               None
    (:action dance
        :parameters (?dancer - character)
        :precondition (and (alive ?dancer))
        :effect (and )
    )

    ; Camelot Action: DanceTogether
    ; Parameters:
    ;               d d1 characters involved in the action
    ;               l position of the action
    ; Preconditions:
    ;               d d1 at the same position
    ;              d d1 are NOT dead
    ; Effects:
    ;               None
    (:action dancetogether
        :parameters (?d ?d1 - character ?l - position)
        :precondition (and (at ?d ?l) 
            (at ?d1 ?l) 
            (alive ?d)
            (alive ?d1)
        )
        :effect (and )
    )
		
    ; Camelot Action: Die
    ; Parameters:
    ;               c character involved in the action
    ; Preconditions:
    ;               c is NOT dead
    ; Effects:
    ;               c is dead
    (:action die
        :parameters (?c - character)
        :precondition (and (alive ?c))
        :effect (and (not(alive ?c)))
    )
    		
    ; Camelot Action: Draw
    ; Note: Camelot allow the action Draw even if the object is not in the current position. The animation looks like che character is drawing a sward, but it can be used for any objects.
    ; Parameters:
    ;               c character involved in the action
    ;               i item involved in the action
    ;               l position involved in the action
    ; Preconditions:
    ;               c is NOT dead
    ;               i is NOT equipped to any other character
    ; Effects:
    ;               c has equipped i
    ;               i is NOT at l MIGTH NEED TO BE CHANGED
    (:action draw
        :parameters (?c - character ?i - item ?l - position)
        :precondition (and (alive ?c)
            (at ?c ?l) 
            (forall (?character - character) 
                (not(equip ?i ?character))
            )
        )
        :effect (and (equip ?i ?c) (not (at ?i ?l)))
    )
    		
    ; Camelot Action: Drink
    ; Parameters:
    ;               c character involved in the action
    ;               i item involved in the action
    ;               l position involved in the action
    ; Preconditions:
    ;               c is NOT dead
    ;               c i are at the same position
    ; Effects:
    ;               None
    (:action drink
        :parameters (?c - character ?i - item ?l - position)
        :precondition (and (alive ?c) 
            (at ?c ?l) 
            (at ?i ?l) 
        )
        :effect (and )
    )
    		
    ; Camelot Action: Enter
    ; Parameters:
    ;               c character involved in the action
    ;               l position involved in the action
    ; Preconditions:
    ;               c is NOT dead
    ;               c is NOT at position
    ; Effects:
    ;               c is at position
    (:action enter
        :parameters (?c - character ?l - position)
        :precondition (and (alive ?c)
            (not (at ?c ?l))
        )
        :effect (and (at ?c ?l))
    )
    
    ; Camelot Action: Exit
    ; Parameters:
    ;               character is the character involved in the action.
    ;              position position to exit
    ; Preconditions:
    ;               character is NOT dead
    ;               character is at position to exit
    ; Effects: 
    ;               character is NOT in the position it previously was
    (:action exit
        :parameters (?c - character ?l - position)
        :precondition (and (alive ?c)
            (at ?c ?l)
        )
        :effect (and (not (at ?c ?l)))
    )

    ; Camelot Action: Give
    ; Parameters: 
    ;               giver receiver are the characters involved in the action.
    ;               item is the item that is exchanged.
    ;               position is used to check that the characters are in the same position.
    ; Preconditions:
    ;               giver ?receiver are NOT dead.
    ;               giver is equipped with the item.
    ;               giver ?receiver are in the same position
    ; Effects: 
    ;               giver does NOT have the item equipped anymore
    ;               receiver equips the item
    (:action give
        :parameters (?giver ?receiver - character ?item - item ?l - location)
        :precondition (and (alive ?giver) 
            (alive ?receiver)
            (equip ?item ?giver) 
            (in ?giver ?l) 
            (in ?receiver ?l)
        )
        :effect (and (not (equip ?item ?giver)) (equip ?item ?receiver))
    )
    		
    ; Camelot Action: Kneel
    ; Parameters:
    ;               character is the character involved in the action.
    ; Preconditions:
    ;               character is NOT kneeling
    ;               character is NOT dead
    ; Effects:
    ;               character is kneeling
    (:action kneel
        :parameters (?character - character)
        :precondition (and (not (kneeling ?character)) 
            (alive ?character)
        )
        :effect (and (kneeling ?character))
    )

    		
    ; Camelot Action: OpenFurniture
    ; Parameters:
    ;               character is the character involved in the action.
    ;               furniture is the furniture to be opened
    ;               position position of character and furniture
    ; Preconditions:
    ;               character is NOT dead
    ;               character furniture at the same position
    ;               furniture is NOT is_open
    ;               furniture can be opened
    ; Effects:
    ;               furniture is is_open
    (:action openfurniture
        :parameters (?character - character ?furniture - furniture ?position - location)
        :precondition (and (alive ?character)
            (in ?character ?position) 
            (at ?furniture ?position)
            (not(is_open ?furniture)) 
            (can_open ?furniture)
        )
        :effect (and (is_open ?furniture))
    )
    
    		
    ; Camelot Action: Pickup
    ; Parameters:
    ;               character character involved in the action
    ;               furniture furniture involved in the action
    ;               position position involved in the action
    ;               item item involved in the action
    ; Preconditions:
    ;               character is NOT dead
    ;               furniture character are at the same position
    ;               item is stored in funiture
    ;               no other character has the item equipped 
    ;               if the furniture is a table then it needs to have a surface (and the item is on the surface). 
    ;               if the forniture doesn't have a surface then the furniture must be open 
    ;               If an item is on the floor (missing)
    ; Effects:
    ;               item is NOT stored in furniture
    ;               item is equipped by the character

    (:action pickup
        :parameters (?character - character ?furniture - furniture ?position - position ?item - item)
        :precondition ( 
            and 
                (alive ?character)
                (at ?furniture ?position) 
                (at ?character ?position) 
                (stored ?item ?furniture)
                (or
                    (has_surface ?furniture)
                    (and 
                        (can_open ?furniture)
                        (is_open ?furniture)
                    )
                )
            
        )
        :effect (and (not (stored ?item ?furniture)) (equip ?item ?character))
    )

    		
    ; Camelot Action: Pocket
    ; Parameters:
    ;               
    ; Preconditions:
    ;               
    ; Effects:
    ;               
    (:action pocket
        :parameters (?character - character ?item - item)
        :precondition (and 
            (alive ?character)
            (equip ?item ?character)
        )
        :effect (and 
            (not (equip ?item ?character))
            (has_item_in_pocket ?character ?item)
        )
    )

    (:action unpocket
        :parameters (?character - character ?item - item)
        :precondition (and 
            (alive ?character)
            (has_item_in_pocket ?character ?item)
        )
        :effect (and 
            (not (has_item_in_pocket ?character ?item))
            (equip ?item ?character)
        )
    )

    (:action revive
        :parameters (?character - character)
        :precondition (and 
            (not (alive ?character))
        )
        :effect (and 
            (alive ?character)
        )
    )
    
    (:action instantiate_object_in_furniture
        :parameters (?obj - item ?into - location ?furniture - furniture)
        :precondition ( and 
            (at ?furniture ?into))
        :effect (and
            (in ?obj ?into)
            (stored ?obj ?furniture) )
    )
    
    
)