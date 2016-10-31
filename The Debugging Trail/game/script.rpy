## The script of the game goes in this file.

## Declare characters used by this game. The color argument colorizes the name
## of the character.

init python:
    config.use_cpickle = False
    import json


define e = Character('eileen')
## The game starts here.

screen hello:
    frame:
        xpadding 10
        ypadding 10
        xalign 1.0
        yalign 0.0
        python:
            f = renpy.file("BuggyProgram.json")
            program = json.load(f)
            code = program["program1"]
            segments = ""
            for i in range(len(code)):
                segments += code[i]["section"]

        text "[segments]"

label start:
    show screen hello
    ## Show a background. This uses a placeholder by default, but you can add a
    ## file (named either "bg room.png" or "bg room.jpg") to the images
    ## directory to show it.

    scene bg room

    ## This shows a character sprite. A placeholder is used, but you can replace
    ## it by adding a file named "eileen happy.png" to the images directory.

    show eileen vhappy

    ## These display lines of dialogue.

    e "Welcome to the Debugging Trail"
    e "Click {a=after_menu}here{/a} to jump to a special page!"
    e "The goal is to make you better debuggers"

    e "We will teach useful tips and strategies to help make debugging an easier task"

    $ text = "next phrase"
    $ e(text)

    menu:
        "What should I do?"

        "Drink coffee.":
            "I drink the coffee, and it's good to the last drop."

        "Drink tea.":
            $ drank_tea = True

            "I drink the tea, trying not to make a political statement as I do."

        "Genuflect.":
            jump genuflect_ending

    label after_menu:

        "After having my drink, I got on with my morning."

    ## This ends the game.

    return
