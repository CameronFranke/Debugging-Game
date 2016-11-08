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

screen stress_bar:
    bar:
        pos (100, 800)
        xysize (500, 70)

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

label replace_code(fixid=0):
    $fixid = ui.interact()
    python: 
        temp = str(buggyProg[code_section]["code"])
        buggyProg[code_section]["code"] = buggyProg[code_section]["fixes"][fixid]
        buggyProg[code_section]["fixes"][fixid] = str(temp)
    
        
    

label fix_code:
    $code_section = ui.interact()
    show screen fix_menu
    jump replace_code
    
    
label view_code:
    hide fix_code
    show screen code
    jump fix_code

screen stress_bar:
    bar:
        pos (100, 800)
        xysize (500, 70)
     
label start:
    ## Show a background. This uses a placeholder by default, but you can add a
    ## file (named either "bg room.png" or "bg room.jpg") to the images
    ## directory to show it.

    show screen stress_bar

    jump view_code

    return
