## The script of the game goes in this file.

## Declare characters used by this game. The color argument colorizes the name
## of the character.

init python:
    config.use_cpickle = False
    import json
    import time 
    f = renpy.file("BuggyProgram.json")
    program = json.load(f)
    buggyProg = program["program1"]
    code_section = 0 ## ??
    
    global stress
    global time_limit
    global the_time
    global time_penalty
    global lines_per_section
    global section_count
    
    lines_per_section = 4
    section_count = 1
    time_penalty = 0
    time_limit = 5 ## in minutes 
    stress = 0
    base_stress_modifier = 5
    break_modifier = 35
    break_duration = 10 ## time penalty in seconds 
    
    
    def modify_stress():
        global stress
        stress = stress + base_stress_modifier
        if stress > 100:
            stress = 100
        
    def take_break():
        global stress
        global time_penalty
        stress = stress - break_modifier
        time_penalty += break_duration
        if stress < 0: 
            stress = 0
            
    def countdown(st, at, length=0.0):
            global time_penalty
            remaining = length - st - time_penalty
            min = int(remaining/60)
            sec = int(remaining % 60)
            
            secstr = str(sec)
            if sec <= 9:
                secstr = "0" + secstr
            timestr = str(min) + ":" + secstr
            
            if remaining > 2.0:
                return Text(timestr, color="#fff", size=72), 1
            elif remaining > 0.0:
                return Text(timestr, color="#f00", size=72), 1
            else:
                return anim.Blink(Text(timestr, color="#f00", size=72)), None


define e = Character('eileen')

style code_button:
    xmaximum 1500
    ymaximum 700

screen code:
    ##global section_count 
    ##global lines_per_section
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
            for i, section in enumerate(buggyProg[0:section_count * lines_per_section]):
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
    vbox:
    ## might want to make an imagebutton
        textbutton "Take a break" pos(80,890) action Jump("take_break")
        
label take_break:
    $take_break()
    
screen onscreen_timer:
    vbox:
        pos(30, 30)
        image DynamicDisplayable(countdown,length=70)
        
screen programmer_options:
    vbox:
        textbutton "Keep Coding" pos(800,830) xmaximum 300 action Jump("keep_coding")
        textbutton "Debug Code" pos(1100,780) xmaximum 300
        
label keep_coding:
    python:
        global section_count
        global lines_per_section
        section_count += 1

label start:
    ## Show a background. This uses a placeholder by default, but you can add a
    ## file (named either "bg room.png" or "bg room.jpg") to the images
    ## directory to show it.
    
    show screen programmer_options
    show screen onscreen_timer
    show screen stress_bar
    
            
    
    jump view_code

    return








