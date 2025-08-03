import json
import os

BASE_DIR = os.path.dirname(__file__)
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback_log.json") #feedback_log automatically created
WEIGHTS_FILE = os.path.join(BASE_DIR,"weights.json")

def store_feedback(input_song, rating, weights):
    feedback_entry={
        "song": input_song,
        "rating":rating,
        "weights":weights
    }
    
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE,"r") as f:
            data = json.load(f)
    else:
        data=[]
    
    data.append(feedback_entry)
    with open(FEEDBACK_FILE,"w") as f:
        json.dump(data,f,indent=4)
        
def update_weight_from_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        print("no feedback file found, skipping weight update")
        return
    with open(FEEDBACK_FILE,"r") as f:
        feedback_data =json.load(f)
        
    if not os.path.exists(WEIGHTS_FILE):
        print("no weights file found")
        return
    
    with open(WEIGHTS_FILE,"r") as f:
        weights_dict =json.load(f)
        
    feature_score_totals ={key:0.0 for key in weights_dict}
    count = 0
    
    
    for entry in feedback_data:
        rating = entry["rating"]
        weights_used = entry["weights"]
        for feat, weight in weights_used.items():
            feature_score_totals[feat] +=weight*(rating-3)
        count +=1
        
    if count>0:
        for feat in weights_dict:
            weights_dict[feat] += 0.01 *feature_score_totals[feat]/count
            weights_dict[feat] =max(0.01, min(1.0,weights_dict[feat]))
            
        with open(WEIGHTS_FILE,"w") as f:
            json.dump(weights_dict,f,indent=4)
        print("weights updated successfully")        