#!/usr/bin/env python3

def DAfromTopWdth(TopWdth):
    return (TopWdth/2.44) ** 2.941176470588235

def CSA(DA):
    return 0.75 * DA ** 0.53

def cross_section_area_BlckBrn(TopWdth):
    '''(Top Width of Trapezoidal Channel)'''
    # This function calculates the cross section area from Topwidth using Blackburn et al. equations
    cs_area = 0.75 * ((TopWdth / 2.44) ** (1.0 / 0.34)) ** 0.53

    return cs_area