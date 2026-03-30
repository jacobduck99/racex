
def brake_coaching(corners):
    for fast_braking in corners:
        print("corners", fast_braking.fast)
        for ref_braking in corners:
            print("corners ref", ref_braking.ref)
