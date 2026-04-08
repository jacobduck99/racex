
class GearCoaching:
    def __init__(self, fast_gear, ref_gear):
        self.fast_gear = fast_gear
        self.ref_gear = ref_gear

    def coaching_gear_tips(self):
        if self.fast_gear == self.ref_gear:
            return "Your gear is the same as your fastest lap"
        elif self.fast_gear > self.ref_gear:
            return  f"Your gear is {self.ref_gear} where fastest lap is {self.fast_gear} go up gears to match it"
        else: 
            return f"Your gear is {self.ref_gear} where fastest lap is {self.fast_gear} go down gears to match it"



