## The script of the game goes in this file.

## Declare characters used by this game. The color argument colorizes the name
## of the character.

init python:
    config.use_cpickle = False
    import json
    import time
    global level 
    global buggyProg
    
    level = 1
    f = renpy.file("BuggyProgram.json")
    program = json.load(f)
    buggyProg = program["program3"]
    code_section = 0

    global errorMsgs
    f = renpy.file("ErrorMessages.json")
    errorMsgs = json.load(f)
    errorMsgs = errorMsgs["error_msg"]

    global stress
    global time_limit
    global the_time
    global time_penalty
    global lines_per_section
    global section_count
    global remaining
    global status
    global errorMsg
    status = ""
    errorMsg = ""
    remaining = 0

    lines_per_section = 4
    section_count = 1
    time_penalty = 0
    time_limit = 600 ## in seconds
    stress = 0
    base_stress_modifier = 2
    stress_per_bug = 10
    break_modifier = 35 ## amount of stress removed by taking a break
    break_duration = 30 ## time penalty in seconds
    action_duration = 3 ## time that an action takes in seconds


    def load_level():
        global level
        global buggyProg
        global section_count
        global code_section
        global stress
        global time_limit
        global remaining
        global status
        status = "playing"
        buggyProg = program["program" + str(level)]
        section_count = 1
        code_section = 0
        stress = 0 
        time_limit += (600 - remaining)
        
    
    def modify_stress():
        global stress
        stress = stress + base_stress_modifier
        if stress > 100:
            stress = 100
        check_wl_status

    def countdown(st, at, length=0.0):
            global time_penalty
            global remaining
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
                check_wl_status()
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

    def action_time_penalty(extra_time=0):
        global time_penalty
        time_penalty += (action_duration + extra_time)

    def replace_code():
        if "fixes" in  buggyProg[code_section]:
            
            x = 0
            while x != 2:
                x, fixid = ui.interact()

            oldCode = str(buggyProg[code_section]["code"])
            olderr = str(buggyProg[code_section]["err_msg"])

            buggyProg[code_section]["code"] = buggyProg[code_section]["fixes"][fixid]["option"]
            buggyProg[code_section]["err_msg"] = buggyProg[code_section]["fixes"][fixid]["err_msg"]

            buggyProg[code_section]["fixes"][fixid]["option"] = oldCode
            buggyProg[code_section]["fixes"][fixid]["err_msg"] = olderr

        else:
            modify_stress()
        ## after a code change it is possible that win conditions have been met

    def test_code():
        global errorMsg

        errorIndices = []
        for line in buggyProg[0: (section_count * lines_per_section)]:
            if "err_msg" in line:
                errorIndices.append(line["err_msg"])
        create_error_msg(errorIndices)

        check_wl_status()


    def create_error_msg(indices):
        global errorMsg
        global errorMsgs
        global stress
        errorMsg = ""

        ################### DEBUG OUTPUT TEST #####################
        global status
        errorMsg = status + "\n"
        ###########################################################

        for i in indices:
            if i != None:
                temp = errorMsgs[i]
                delayIndex = 0
                if "delayed" in temp:
                    delayIndex = ""
                    readFlag = False
                    
                    for x in temp:
                        if x == "[":
                            readFlag = True
                            continue
                        if x == "]":
                            break
                        if readFlag:
                            delayIndex += x
                            
                    temp = temp.replace("[" + delayIndex + "]" ,"")    
                    if delayIndex == "": 
                        delayIndex = len(buggyProg)
                    else: 
                        delayIndex = int(delayIndex)
                    
                if "delayed" not in temp: 
                    errorMsg += temp + "\n"
                    stress += stress_per_bug                ## stress is modified here because there is already a loop checking None vs error indices
                    
                elif "delayed" in temp:
                    if delayIndex <= (section_count * lines_per_section):
                        errorMsg += temp.replace("delayed", "") + "\n"

        if errorMsg == "":
            errorMsg = "No compile time errors"

    def check_wl_status():
        ##      win    check if all of the code is displayed
        ##             check if all of the errors are fixed
        ##      loss   check if time has run out
        ##             check if stress has reached 100

        global remaining
        global status

        status = "playing"
        if section_count*lines_per_section >= len(buggyProg):
            tag = True
            for line in buggyProg:
                if line["err_msg"] != None:
                    tag = False
            if tag:
                status = "win"
                renpy.call("transition1")


        if stress >= 100 or remaining <= 0:
            status = "lose"

        ##renpy.call("transition1")

init:
    define e = Character('eileen')
    image bg office = "office.jpg"
    image bg pentagon = "Pentagon.jpg"

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
            $tabStops = 0
            for i, section in enumerate(buggyProg[0: section_count * lines_per_section]):
                $code = section["code"]

                $temp = 0
                $if code == "}": temp = 1
                $num = str(i)
                $if i <= 9: num = "  " + num
                $code = (num + ".  " + "    "*(tabStops - temp)) + code
                textbutton "[code]" style "code_line" text_style "my_font" action [Function(action_time_penalty), Return([1,i])]
                $tabStops += (code.count("{{"))
                $tabStops -= (code.count("}"))


            for x in range(tabStops):
                $pad = ""
                $if i + x + 1 <= 9: pad = "  "
                $line = pad + str(i + x + 1) + ". " + "    "*(tabStops - (x+1)) + "}"
                textbutton "[line]" style "code_line" text_style "my_font" action [Function(modify_stress), Function(action_time_penalty)]


screen fix_menu:
     frame:
        xalign 0.0
        yalign 0.5
        vbox:
            ##$action_time_penalty() ## bringing up a fixe menu takes time=action_duration
            $choices = buggyProg[code_section]
            if "fixes" in choices:
                $s = choices["fixes"]
                for i, ch in enumerate(s):
                    $code = ch["option"]
                    textbutton "[code]" style "code_line" text_style "my_font" action [Hide("fix_menu"), Function(action_time_penalty), Return([2,i])]

label fix_code:
    $x, code_section = ui.interact()
    show screen fix_menu
    $replace_code()


label view_code:
    hide fix_code
    show screen code
    call fix_code


screen stress_bar:
    vbox:
        pos (20, 850)
        spacing 10

        hbox:
            text "Stress: "
            bar:
                range 100
                value stress
                xysize (250, 50)

        textbutton "Take a break":
            style "game_button"
            text_style "game_button_text"
            action Function(take_break)
            pos(70,0)

screen onscreen_timer:
    vbox:
        pos(30, 30)
        image DynamicDisplayable(countdown,length=time_limit)

screen programmer_options:
    hbox:
        xalign 0.5
        ypos 950
        spacing 10
        textbutton "Keep Coding":
            style "game_button"
            text_style "game_button_text"
            action [Function(keep_coding), Function(action_time_penalty, extra_time=7)]

        textbutton "Debug Code":
            style "game_button"
            text_style "game_button_text"
            action [Function(test_code), Function(action_time_penalty, extra_time=7)]

screen debug_output:
    frame:
        xalign 1.0
        yalign 0.0
        xsize 1500
        ysize 150

        xpos 1920
        ypos 800

        vbox:
            text "[errorMsg]"

label fix_code:
    $x, code_section = ui.interact()
    show screen fix_menu
    $replace_code()


label view_code:
    hide fix_code
    show screen code
    jump fix_code


label start:
    #instructions to play the game

    ##e "Welcome to the Debugging Trail"

    ##e  "The world is ending"

    ## scene bg pentagon
    ## with dissolve

    ##e "It is your job to save the world by creating lifesaving programs"

    ##e "Like any programmer, you will run into bugs."

    ##e "It is essential that you fix them for human life to continue"

    jump level1


label level1:

    scene bg office
    with dissolve

    ##e "To start coding press the 'Keep Coding' button"


    ##e "The code you will write will appear on the screen, but becareful for it may contain bugs"


    ##e "To compile your code press the 'compile' button"

    ##e "To start coding, press the 'Keep Coding' button"

    ##e "The code you will write will appear on the screen, but becareful for it may contain bugs"

    ##e "To compile your code, press the 'compile' button"


    ##e "Errors will show in the debug console"


    ##e "To fix an error, you can click on each line of code to bring up a list of possible fixes to choose from"

    ##e "To fix the error you can click on each line of code to get possible fixes"


    ##e "Beware: Every action you take will cost you time, and every bug the compiler catches will cost you stress"


    ##e "If your stress gets to high or you run out of time, you lose..."

    ##e "To fix the error, you can click on each line of code to bring up a list of possible fixes to choose from"

    ##e "Beware: Every action you take will cost you time, and every bug the compiler catches will cost you stress"

    ##e "If your stress gets to high or time runs out, we all lose..."


    show screen programmer_options
    show screen onscreen_timer
    show screen stress_bar
    show screen debug_output

    jump view_code


label transition1:
    hide screen fix_code
    hide screen code
    hide screen programmer_options
    hide screen onscreen_timer
    hide screen stress_bar
    hide screen debug_output

    scene bg pentagon
    with dissolve



    e "Congratulations! you have made the world that much safer with your bug free program"

    e "However, there is still much to be done"

    jump level2


label level2:

    scene bg office
    with dissolve

    e "Welcome to level 2"

    e "Get to work!"

    python:
        global level 
        level += 1
        load_level()
    hide screen onscreen_timer
    show screen onscreen_timer
        
    show screen programmer_options
    show screen onscreen_timer
    show screen stress_bar
    show screen debug_output

    jump view_code
