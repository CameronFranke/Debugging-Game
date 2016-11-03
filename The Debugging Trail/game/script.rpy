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
    xmaximum 1500
    ymaximum 700

screen code:
    frame:
        xalign 1.0
        yalign 0.0
        xmaximum 1500
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

screen fix_menu:
    frame:
        xalign 0.0
        yalign 0.5
        vbox:
            $choices = buggyProg[code_section]
            if "fixes" in choices:
                $s = choices["fixes"]
                for i, ch in enumerate(s):
                    textbutton "[ch]":
                        style "code_button"
                        action Return(i)

label fix_code:
    $code_section = ui.interact()
    show screen fix_menu

label view_code:
    hide fix_code
    show screen code
    jump fix_code

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
    e "The purpose of this game is to help you become a better debugger."
    e "We will show you a screen of code that contains errors. It is your job to find the bugs and fix them."
    e "When you find a bug, click on the buggy section of code and a menu will pop up showing a list of possible fixes."
    e "Pick the correct option to fix the code."

    hide eileen

    jump view_code

    return
