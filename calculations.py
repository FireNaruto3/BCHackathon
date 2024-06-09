goodSleep = 7 #less than is bad
badBPM = 100 #greater than is bad
badBloodPressure = 140 #greater than is bad
badcholestoral = 200 #greater than is bad
badBMI = 25



def calculate(weight, height, sleep, BPM, bloodPressure, cholestoral):    
    
    accumulator = 0

    dict = { 
              
    }

    BMI = weight/height
    if(BMI > badBMI):
        dict["BMI"] = "Your BMI is risking your health"
        accumulator += 1
    else:
        dict["BMI"] = "Your BMI is fine!"
        
    if(sleep > goodSleep):
        dict["sleep"] = "You have a great sleep schedule!"
    else:
        dict["sleep"] = "You need more sleep!"
        accumulator+=1

    if(BPM > badBPM):
        dict["BPM"] = "Your BPM is risking your health!"
        accumulator+=1
    else:
        dict["BPM"] = "Your BPM is fine!"

    if(bloodPressure > badBloodPressure):
        dict["bloodPressure"] = "Your blood pressure is fine!"
    else:
        dict["bloodPressure"] = "Your blood pressure is risking your health!"
        accumulator+=1

    if(cholestoral > badcholestoral):
        dict["cholestoral"] = "Your cholestoral is fine!"
    else:
        dict["cholestoral"] = "Your cholestoral is risking your health!"
        accumulator+=1

    dict['value'] = 100-(accumulator*20)

    # if true, that means that person fails that category.
    return dict

    

    
