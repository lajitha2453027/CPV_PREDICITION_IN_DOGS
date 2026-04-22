import numpy as np

def predict_cpv(symptoms):

    # symptoms list like [1,0,1,1,0,0]
    total_yes = sum(symptoms)
    total_symptoms = len(symptoms)

    # All YES
    if total_yes == total_symptoms:
        return "DANGER – CPV POSITIVE"

    # Average YES (3 or 4 yes)
    elif total_yes >= 3:
        return "WARNING – Possible CPV"

    # Low or no YES
    else:
        return "SAFE – No CPV Detected"
