## The script of the game goes in this file.

## Declare characters used by this game. The color argument colorizes the name
## of the character.

init python:
    config.use_cpickle = False
    import json
    f = renpy.file("BuggyProgram.json")
    program = json.load(f)
    buggyProg = program["program1"]
    code_section = 0



define e = Character('eileen')
## The game starts here.

style code_button:
    xmaximum 1000
    ymaximum 400

screen code_view:
    frame:
        xpadding 10
        ypadding 10
        xalign 1.0
        yalign 0.0
        xmaximum 900
        ymaximum 800

        viewport:
            draggable False
            mousewheel True
            scrollbars "vertical"
            side_xalign 1

            has vbox
            for i, section in enumerate(buggyProg):
                $code = section["code"]
                #text "{a=start}[code]{/a}"
                textbutton "[code]":
                    style "code_button"
                    action Return(i)
            #for i in range(0, 20):
            #     textbutton "button [i]" action Return(i)

screen bug_fix_menu:
    frame:
        vbox:
            $choices = buggyProg[code_section]["fixes"]
            for ch in choices:
                textbutton "{color=#ffff}[ch]{/color}"

label fix_code:
    show screen bug_fix_menu

label start:
    ## Show a background. This uses a placeholder by default, but you can add a
    ## file (named either "bg room.png" or "bg room.jpg") to the images
    ## directory to show it.

    scene bg room

    ## This shows a character sprite. A placeholder is used, but you can replace
    ## it by adding a file named "eileen happy.png" to the images directory.

    show eileen vhappy

    ## These display lines of dialogue.

    e "Welcome to the Debugging Trail"

    show screen code_view
    $code_section = ui.interact()
    jump fix_code

    return
