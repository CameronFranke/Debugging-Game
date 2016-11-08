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
    global stress
    stress = 0
    base_stress_modifier = 1
    
    def modify_stress():
        global stress
        stress = stress + base_stress_modifier


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
                        action [Hide("fix_menu"), Return(i)]


label replace_code():
    python:
        if "fixes" in buggyProg[code_section]:
            fixid = ui.interact()
            temp = str(buggyProg[code_section]["code"])
            buggyProg[code_section]["code"] = buggyProg[code_section]["fixes"][fixid]
            buggyProg[code_section]["fixes"][fixid] = str(temp)
        else:
            modify_stress()

label fix_code:
    
    $code_section = ui.interact()
    show screen fix_menu
    jump replace_code


label view_code:
    hide fix_code
    show screen code
    jump fix_code

screen stress_bar:
    python:
        ui.bar(range=100, value=stress, pos=(30, 830), xysize=(350, 50))



label start:
    ## Show a background. This uses a placeholder by default, but you can add a
    ## file (named either "bg room.png" or "bg room.jpg") to the images
    ## directory to show it.

    
    show screen stress_bar

    jump view_code

    return
