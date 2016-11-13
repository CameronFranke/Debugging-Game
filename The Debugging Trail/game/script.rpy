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

    def keep_coding():
        global section_count
        section_count += 1

    def take_break():
        global stress
        global time_penalty
        stress = stress - break_modifier
        time_penalty += break_duration
        if stress < 0:
            stress = 0

init:
    define e = Character('eileen')
    image bg office = "office.jpg"

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
            for i, section in enumerate(buggyProg[0: section_count * lines_per_section]):
                $code = section["code"]
                textbutton "[code]" style "code_line" action Return(i)

screen fix_menu:
     frame:
        xalign 0.0
        yalign 0.5
        vbox:
            $choices = buggyProg[code_section]
            if "fixes" in choices:
                $s = choices["fixes"]
                for i, ch in enumerate(s):
                    $code = ch["option"]
                    textbutton "[code]" style "code_line" action [Hide("fix_menu"), Return(i)]


label replace_code():
    python:
        if buggyProg[code_section]["fixes"]:
            fixid = ui.interact()
            temp = str(buggyProg[code_section]["code"])
            buggyProg[code_section]["code"] = buggyProg[code_section]["fixes"][fixid]["option"]
            buggyProg[code_section]["fixes"][fixid]["option"] = str(temp)
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
    vbox:
        pos (30, 950)
        spacing 10
        bar:
            range 100
            value stress
            xysize (350, 50)

        textbutton "Take a break":
            style "game_button"
            text_style "game_button_text"
            action Function(take_break)

screen onscreen_timer:
    vbox:
        pos(30, 30)
        image DynamicDisplayable(countdown,length=70)

screen programmer_options:
    hbox:
        xalign 0.5
        ypos 950
        spacing 10
        textbutton "Keep Coding":
            style "game_button"
            text_style "game_button_text"

        textbutton "Debug Code":
            style "game_button"
            text_style "game_button_text"
            action Function(keep_coding)

label start:
    ## Show a background. This uses a placeholder by default, but you can add a
    ## file (named either "bg room.png" or "bg room.jpg") to the images
    ## directory to show it.
    scene bg office

    show screen programmer_options
    show screen onscreen_timer
    show screen stress_bar

    jump view_code

    return
