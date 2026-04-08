
class GearCoaching:
    def __init__(self, corners):
        self.corners = corners
        self.coaching = []

    def coaching_gear_tips(self):
        for gear in self.corners:
            fast_gear = gear.fast.gear
            ref_gear = gear.ref.gear
            sector = gear.corner_num
            if fast_gear == ref_gear:
                tip = f"Sector {sector}: Your gear is the same as your fastes sector {sector}"
            elif fast_gear > ref_gear:
                tip = f"Sector {sector}: Your gear is {ref_gear} where fastest sector {sector} is {fast_gear} go up gears to match it"
            else: 
                tip = f"Sector {sector} Your gear is {ref_gear} where fastest sector {sector} is {fast_gear} go down gears to match it"

            self.coaching.append({"Sector": sector, "gear": tip})
        print("James says", self.coaching)

        return self.coaching



