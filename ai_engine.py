class AIEngine:

    def __init__(self):

        self.weight = {
            "technical":30,
            "fundamental":25,
            "chip":20,
            "news":15,
            "market":10
        }

    def total_score(self,data):

        score=0

        detail={}

        for key,w in self.weight.items():

            s=data.get(key,0)

            detail[key]=s

            score+=s*w/100

        return {

            "total":round(score),

            "detail":detail

        }


if __name__=="__main__":

    ai=AIEngine()

    result=ai.total_score({

        "technical":80,

        "fundamental":90,

        "chip":75,

        "news":60,

        "market":70

    })

    print(result)

